from app.services.dashboard_service import (
    get_dashboard_stats,
)

from app.database.database import SessionLocal

from typing import List

from fastapi import (
    APIRouter,
    Request,
    Form,
    HTTPException,
)

from fastapi.responses import (
    RedirectResponse,
    JSONResponse,
)

from fastapi.templating import Jinja2Templates

from app.ai.worker import process_ai_news
from app.ai.instagram_pipeline import process_instagram

from app.database.crud import (
    get_news_by_id,
    update_news_editor,
    update_instagram_content,
    bulk_update_status,
    bulk_delete_news,
)

from app.services.editor_service import (
    get_editor_news,
    get_filtered_news,
    search_editor_news,
    get_brand_list,
    get_category_list,
)
from app.services.visual_source_service import (
    get_selected_visual,
    resolve_and_save_visual,
    visual_for_response,
)
from app.services.instagram_visual_service import (
    VisualRenderError,
    render_instagram_visual,
    rendered_visual_url,
)


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


# ==========================================================
# NEWS DETAIL
# ==========================================================

@router.get("/news/{news_id}")
def news_detail(
    request: Request,
    news_id: int,
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    news = get_news_by_id(news_id)

    if news is None:
        raise HTTPException(
            status_code=404,
            detail="News not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="detail.html",
        context={
            "request": request,
            "news": news,
        },
    )


# ==========================================================
# AI EDITOR PANEL
# ==========================================================

@router.get("/editor")
def editor_panel(
    request: Request,
    keyword: str = "",
    status: str = "",
    brand: str = "",
    category: str = "",
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    if keyword:

        news_list = search_editor_news(
            keyword
        )

    elif status or brand or category:

        news_list = get_filtered_news(
            status=status or None,
            brand=brand or None,
            category=category or None,
        )

    else:

        news_list = get_editor_news()

    brands = get_brand_list()

    categories = get_category_list()

    db = SessionLocal()

    try:

        stats = get_dashboard_stats(db)

    finally:

        db.close()

    return templates.TemplateResponse(
        request=request,
        name="editor.html",
        context={
            "request": request,
            "news_list": news_list,
            "brands": brands,
            "categories": categories,
            "stats": stats,
        },
    )

# ==========================================================
# BULK ACTION
# ==========================================================

@router.post("/editor/bulk")
def bulk_action(
    request: Request,
    action: str = Form(...),
    news_ids: List[int] = Form(...),
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    # ------------------------------------------------------
    # AI İşle
    # ------------------------------------------------------

    if action == "ai":

        for news_id in news_ids:
            process_ai_news(news_id)

    # ------------------------------------------------------
    # Editör İnceleme
    # ------------------------------------------------------

    elif action == "editor_review":

        bulk_update_status(
            news_ids,
            "editor_review",
        )

    # ------------------------------------------------------
    # Instagram Hazır
    # ------------------------------------------------------

    elif action == "instagram_ready":

        bulk_update_status(
            news_ids,
            "instagram_ready",
        )

    # ------------------------------------------------------
    # Planla
    # ------------------------------------------------------

    elif action == "scheduled":

        bulk_update_status(
            news_ids,
            "scheduled",
        )

    # ------------------------------------------------------
    # Yayınla
    # ------------------------------------------------------

    elif action == "published":

        bulk_update_status(
            news_ids,
            "published",
        )

    # ------------------------------------------------------
    # Arşivle
    # ------------------------------------------------------

    elif action == "archived":

        bulk_update_status(
            news_ids,
            "archived",
        )

    # ------------------------------------------------------
    # Sil
    # ------------------------------------------------------

    elif action == "delete":

        bulk_delete_news(
            news_ids,
        )

    # ------------------------------------------------------
    # AJAX kontrolü
    # ------------------------------------------------------

    is_ajax = (
        request.headers.get("X-Requested-With")
        == "XMLHttpRequest"
    )

    # ------------------------------------------------------
    # AJAX JSON cevap
    # ------------------------------------------------------

    if is_ajax:

        return JSONResponse(
            {
                "success": True,
                "action": action,
                "count": len(news_ids),
                "message": (
                    f"{len(news_ids)} haber başarıyla işlendi."
                ),
            }
        )

    # ------------------------------------------------------
    # Normal form gönderimi
    # ------------------------------------------------------

    return RedirectResponse(
        url="/editor",
        status_code=303,
    )
# ==========================================================
# AI EDITOR DETAIL
# ==========================================================

@router.get("/editor/{news_id}")
def editor_detail(
    request: Request,
    news_id: int,
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    news = get_news_by_id(news_id)

    if news is None:
        raise HTTPException(
            status_code=404,
            detail="News not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="editor_detail.html",
        context={
            "request": request,
            "news": news,
        },
    )


# ==========================================================
# EDITOR DETAIL SAVE
# ==========================================================

@router.post("/editor/{news_id}")
def save_editor(
    request: Request,
    news_id: int,

    translated_title: str = Form(...),
    summary: str = Form(...),
    category: str = Form(...),
    brand: str = Form(...),
    importance: int = Form(...),
    editor_note: str = Form(""),
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    update_news_editor(
        news_id=news_id,
        translated_title=translated_title,
        summary=summary,
        category=category,
        brand=brand,
        importance=importance,
        editor_note=editor_note,
    )

    return RedirectResponse(
        url=f"/editor/{news_id}",
        status_code=303,
    )


# ==========================================================
# AI EDITOR INLINE AJAX SAVE
# ==========================================================

@router.post("/editor/{news_id}/save")
def save_editor_inline(
    request: Request,
    news_id: int,

    translated_title: str = Form(""),
    summary: str = Form(""),

    brand: str = Form(""),
    category: str = Form(""),

    importance: int = Form(...),

    instagram_title: str = Form(""),
    instagram_caption: str = Form(""),
    hashtags: str = Form(""),
    image_prompt: str = Form(""),
):

    # ------------------------------------------------------
    # AUTH
    # ------------------------------------------------------

    if not request.session.get("authenticated"):
        return JSONResponse(
            {
                "success": False,
                "message": "Oturum geçersiz.",
            },
            status_code=401,
        )

    # ------------------------------------------------------
    # HABER KONTROLÜ
    # ------------------------------------------------------

    news = get_news_by_id(news_id)

    if news is None:
        return JSONResponse(
            {
                "success": False,
                "message": "Haber bulunamadı.",
            },
            status_code=404,
        )

    # ------------------------------------------------------
    # ÖNEM KONTROLÜ
    # ------------------------------------------------------

    if importance < 1 or importance > 10:

        return JSONResponse(
            {
                "success": False,
                "message": "Önem değeri 1 ile 10 arasında olmalıdır.",
            },
            status_code=400,
        )

    try:

        # --------------------------------------------------
        # AI / EDITOR ALANLARI
        # --------------------------------------------------

        update_news_editor(
            news_id=news_id,
            translated_title=translated_title,
            summary=summary,
            category=category,
            brand=brand,
            importance=importance,
            editor_note="",
        )

        # --------------------------------------------------
        # INSTAGRAM ALANLARI
        # --------------------------------------------------

        update_instagram_content(
            news_id=news_id,
            instagram_title=instagram_title,
            instagram_caption=instagram_caption,
            hashtags=hashtags,
            image_prompt=image_prompt,
        )

        # --------------------------------------------------
        # BAŞARILI
        # --------------------------------------------------

        return JSONResponse(
            {
                "success": True,
                "news_id": news_id,
                "message": (
                    f"Haber #{news_id} başarıyla kaydedildi."
                ),
            }
        )

    except Exception as e:

        print(
            f"❌ Editör kayıt hatası ({news_id}): {e}"
        )

        return JSONResponse(
            {
                "success": False,
                "message": (
                    "Haber kaydedilirken bir hata oluştu."
                ),
            },
            status_code=500,
        )


# ==========================================================
# INSTAGRAM EDITOR
# ==========================================================

@router.get("/instagram/{news_id}")
def instagram_editor(
    request: Request,
    news_id: int,
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    news = get_news_by_id(news_id)

    if news is None:
        raise HTTPException(
            status_code=404,
            detail="News not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="instagram_editor.html",
        context={
            "request": request,
            "news": news,
            "visual_image": visual_for_response(
                get_selected_visual(news_id)
            ),
            "rendered_image": rendered_visual_url(news_id),
        },
    )


# ==========================================================
# INSTAGRAM SAVE
# ==========================================================

@router.post("/instagram/{news_id}")
def save_instagram_editor(
    request: Request,
    news_id: int,

    instagram_title: str = Form(...),
    instagram_caption: str = Form(...),
    hashtags: str = Form(...),
    image_prompt: str = Form(...),
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    update_instagram_content(
        news_id=news_id,
        instagram_title=instagram_title,
        instagram_caption=instagram_caption,
        hashtags=hashtags,
        image_prompt=image_prompt,
    )

    return RedirectResponse(
        url=f"/instagram/{news_id}",
        status_code=303,
    )

# ==========================================================
# INSTAGRAM GÖRSEL KAYNAĞI
# ==========================================================

@router.post("/instagram/{news_id}/resolve-image")
def resolve_instagram_image(
    request: Request,
    news_id: int,
):
    """Haber için otomatik görsel adayı bulur ve kaynak kaydını saklar."""
    if not request.session.get("authenticated"):
        return JSONResponse(
            {"success": False, "message": "Oturum geçersiz."},
            status_code=401,
        )

    news = get_news_by_id(news_id)
    if news is None:
        return JSONResponse(
            {"success": False, "message": "Haber bulunamadı."},
            status_code=404,
        )

    try:
        image = resolve_and_save_visual(news)
        return JSONResponse(
            {
                "success": True,
                "news_id": news_id,
                "visual_image": visual_for_response(image),
            }
        )
    except Exception as e:
        print(f"❌ Görsel kaynak çözümleme hatası ({news_id}): {e}")
        return JSONResponse(
            {
                "success": False,
                "message": "Görsel kaynağı bulunurken bir hata oluştu.",
            },
            status_code=500,
        )


# ==========================================================
# INSTAGRAM GÖRSEL OLUŞTUR
# ==========================================================

@router.post("/instagram/{news_id}/render")
def render_instagram_image(
    request: Request,
    news_id: int,
    instagram_title: str = Form(""),
):
    """Otomatik seçilen kaynak fotoğrafından nihai Instagram görselini üretir."""
    if not request.session.get("authenticated"):
        return JSONResponse(
            {"success": False, "message": "Oturum geçersiz."},
            status_code=401,
        )

    news = get_news_by_id(news_id)
    if news is None:
        return JSONResponse(
            {"success": False, "message": "Haber bulunamadı."},
            status_code=404,
        )

    headline = instagram_title.strip() or (news.instagram_title or "").strip()
    if not headline:
        return JSONResponse(
            {
                "success": False,
                "message": "Önce Instagram başlığını oluşturun.",
            },
            status_code=400,
        )

    try:
        image = resolve_and_save_visual(news)
        if image is None:
            raise VisualRenderError(
                "Kaynak veya açık lisanslı uygun görsel bulunamadı."
            )
        rendered = render_instagram_visual(
            news_id=news_id,
            headline=headline,
            image_url=image.image_url,
        )
        return JSONResponse(
            {
                "success": True,
                "news_id": news_id,
                "message": "Instagram görseli oluşturuldu.",
                "generated_image": rendered.public_url,
                "visual_image": visual_for_response(image),
            }
        )
    except VisualRenderError as exc:
        return JSONResponse(
            {"success": False, "message": str(exc)},
            status_code=422,
        )
    except Exception as exc:
        print(f"❌ Instagram görsel üretim hatası ({news_id}): {exc}")
        return JSONResponse(
            {
                "success": False,
                "message": "Instagram görseli oluşturulurken bir hata oluştu.",
            },
            status_code=500,
        )


# ==========================================================
# INSTAGRAM AI GENERATE
# ==========================================================

@router.post("/instagram/{news_id}/generate")
def generate_instagram_ai(
    request: Request,
    news_id: int,
):

    # ------------------------------------------------------
    # AUTH
    # ------------------------------------------------------

    if not request.session.get("authenticated"):
        return JSONResponse(
            {
                "success": False,
                "message": "Oturum geçersiz.",
            },
            status_code=401,
        )

    # ------------------------------------------------------
    # HABER
    # ------------------------------------------------------

    news = get_news_by_id(news_id)

    if news is None:
        return JSONResponse(
            {
                "success": False,
                "message": "Haber bulunamadı.",
            },
            status_code=404,
        )

    # ------------------------------------------------------
    # AI İÇİN İÇERİK
    # ------------------------------------------------------

    news_text = (
        news.content
        or news.summary
        or news.translated_title
        or news.title
        or ""
    )

    if not news_text.strip():
        return JSONResponse(
            {
                "success": False,
                "message": (
                    "Instagram AI için haber içeriği bulunamadı."
                ),
            },
            status_code=400,
        )

    # ------------------------------------------------------
    # INSTAGRAM AI
    # ------------------------------------------------------

    try:

        image = resolve_and_save_visual(news)
        visual_image = visual_for_response(image)

        result, metrics = process_instagram(
            news_text,
            source_name=news.source or "Resmi kaynak",
            published_at=news.published_at or news.created_at,
            headline=news.translated_title or news.title or "",
            visual_context=visual_image["message"] or "",
        )

        # AI taslağını yalnızca tarayıcıya döndürmek yeterli değildir:
        # kullanıcı sayfayı yenilediğinde başlık, açıklama ve uygulama notu
        # kaybolmamalıdır. Başarılı üretimi hemen haber kaydına yaz.
        update_instagram_content(
            news_id=news_id,
            instagram_title=result["instagram_title"],
            instagram_caption=result["instagram_caption"],
            hashtags=result["hashtags"],
            image_prompt=result["image_prompt"],
        )

        generated_image = None
        visual_render_error = None
        if image is not None:
            try:
                generated_image = render_instagram_visual(
                    news_id=news_id,
                    headline=result["instagram_title"],
                    image_url=image.image_url,
                ).public_url
            except VisualRenderError as exc:
                visual_render_error = str(exc)

        # --------------------------------------------------
        # BAŞARILI
        # --------------------------------------------------

        return JSONResponse(
            {
                "success": True,
                "news_id": news_id,
                "message": (
                    f"Haber #{news_id} için "
                    "Instagram taslağı oluşturuldu."
                ),
                "data": {
                    "instagram_title": result.get(
                        "instagram_title",
                        "",
                    ),
                    "instagram_caption": result.get(
                        "instagram_caption",
                        "",
                    ),
                    "hashtags": result.get(
                        "hashtags",
                        "",
                    ),
                    "image_prompt": result.get(
                        "image_prompt",
                        "",
                    ),
                    "photo_direction": result.get(
                        "photo_direction",
                        "",
                    ),
                    "visual_brief": result.get(
                        "visual_brief",
                        "",
                    ),
                    "validation_notes": result.get(
                        "validation_notes",
                        [],
                    ),
                    "visual_image": visual_image,
                    "generated_image": generated_image,
                    "visual_render_error": visual_render_error,
                },
                "metrics": metrics,
            }
        )

    except Exception as e:

        print(
            f"❌ Instagram AI hatası "
            f"({news_id}): {e}"
        )

        return JSONResponse(
            {
                "success": False,
                "message": (
                    "Instagram içeriği oluşturulurken "
                    "bir hata oluştu."
                ),
                "error": str(e),
            },
            status_code=500,
        )
# ==========================================================
# SINGLE AI REPROCESS
# ==========================================================

@router.post("/editor/{news_id}/ai")
def rerun_ai(
    request: Request,
    news_id: int,
):

    if not request.session.get("authenticated"):
        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    news = get_news_by_id(news_id)

    if news is None:
        raise HTTPException(
            status_code=404,
            detail="News not found",
        )

    process_ai_news(news_id)

    return JSONResponse(
        {
            "success": True,
            "message": "İşlem başarıyla tamamlandı.",
        }
    )
