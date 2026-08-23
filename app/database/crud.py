import logging
from datetime import datetime, UTC
from email.utils import parsedate_to_datetime

from sqlalchemy import desc, or_

from app.database.database import SessionLocal
from app.models.news import News
from app.services.duplicate_service import is_similar

logger = logging.getLogger(__name__)


VALID_STATUS = {
    "new",
    "ai_pending",
    "ai_processed",
    "ai_skipped",
    "ai_ready",
    "editor_review",
    "instagram_draft",
    "instagram_ready",
    "scheduled",
    "published",
    "archived",
    "deleted",
    "ai_error",
}
def validate_status(status: str) -> None:
    """
    Validate workflow status.
    """
    if status not in VALID_STATUS:
        raise ValueError(f"Geçersiz status: {status}")

def parse_published_at(
    value: str | datetime | None,
) -> datetime | None:
    if not value:
        return None

    if isinstance(value, datetime):
        return value

    try:
        return parsedate_to_datetime(value)
    except Exception:
        return None


# ==========================================================
# HABER KAYDET
# ==========================================================

def save_news(
    news_list: list[dict],
) -> list[News]:

    db = SessionLocal()

    new_news = []

    duplicate_link = 0

    try:

        for item in news_list:

            title = item.get("title")

            link = item.get("link")


            if not title:
                continue


            # Link duplicate kontrolü
            exists = None

            if link:

                exists = (
                    db.query(News)
                    .filter(
                        News.link == link
                    )
                    .first()
                )


            if exists:

                duplicate_link += 1

                logger.info(
                    "Duplicate link: %s",
                    title,
                )

                continue



            news = News(

                title=title,

                translated_title=item.get(
                    "title_tr"
                ),

                summary=item.get(
                    "summary_tr"
                ),

                content=(
                    item.get("content")
                    or item.get("description")
                ),

                link=link,

                source=item.get(
                    "source"
                ),

                author=item.get(
                    "author"
                ),

                image_url=item.get(
                    "image_url"
                ),

                language=item.get(
                    "language",
                    "en",
                ),

                published_at=parse_published_at(
                    item.get(
                        "published_at"
                    )
                ),


                # Workflow başlangıcı

                status="new",

                ai_processed=False,

                published=False,

            )


            db.add(news)

            new_news.append(news)


        db.commit()


        logger.info(
            "News import completed | New=%s | DuplicateLink=%s",
            len(new_news),
            duplicate_link,
        )


        return new_news


    except Exception:

        db.rollback()

        logger.exception(
            "Save news failed. Incoming news count=%d",
            len(news_list),
        )

        raise


    finally:

        db.close()


# ==========================================================
# HABERLER
# ==========================================================

def get_news(
    keyword=None,
    source=None,
    category=None,
    status=None,
    page=1,
    page_size=20,
):

    db = SessionLocal()

    try:

        query = db.query(News)

        if keyword:
            escaped_keyword = (
                keyword
                .replace("\\", "\\\\")
                .replace("%", "\\%")
                .replace("_", "\\_")
            )
            search_pattern = f"%{escaped_keyword}%"

            query = query.filter(
                or_(
                    News.title.ilike(search_pattern, escape="\\"),
                    News.translated_title.ilike(search_pattern, escape="\\"),
                    News.source.ilike(search_pattern, escape="\\"),
                )
            )

        if source:
            query = query.filter(
                News.source == source
            )

        if category:
            query = query.filter(
                News.category == category
            )

        if status:
            query = query.filter(
                News.status == status
            )

        total = query.count()
        total_pages = max(1, (total + page_size - 1) // page_size)
        page = min(max(page, 1), total_pages)

        items = (
            query
            .order_by(desc(News.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "items": items,
        }

    finally:

        db.close()


# ==========================================================
# DETAY
# ==========================================================

def get_news_by_id(
    news_id: int,
) -> News | None:

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.id == news_id)
            .first()
        )

    finally:

        db.close()

# ==========================================================
# EDITOR
# ==========================================================

def update_news_editor(
    news_id: int,
    translated_title: str,
    summary: str,
    category: str,
    brand: str,
    importance: int,
    editor_note: str,
):

    db = SessionLocal()

    try:

        news = (
            db.query(News)
            .filter(News.id == news_id)
            .first()
        )

        if news is None:
            return None

        news.translated_title = translated_title
        news.summary = summary
        news.category = category
        news.brand = brand
        news.importance = importance
        news.editor_note = editor_note
        news.updated_at = datetime.now(UTC)

        if news.status == "ai_ready":
            news.status = "editor_review"

        db.commit()
        db.refresh(news)

        return news

    except Exception:
        db.rollback()
        logger.exception(
            "Editor update failed. News ID=%s",
            news_id,
        )

        raise

    finally:

        db.close()


# ==========================================================
# INSTAGRAM
# ==========================================================

def update_instagram_content(
    news_id: int,
    instagram_title: str,
    instagram_caption: str,
    hashtags: str,
    image_prompt: str,
):

    db = SessionLocal()

    try:

        news = (
            db.query(News)
            .filter(News.id == news_id)
            .first()
        )

        if news is None:
            return None

        news.instagram_title = instagram_title
        news.instagram_caption = instagram_caption
        news.hashtags = hashtags
        news.image_prompt = image_prompt
        news.updated_at = datetime.utcnow()
        news.status = "instagram_draft"

        db.commit()
        db.refresh(news)

        return news

    except Exception:
        db.rollback()
        logger.exception(
            "Instagram content update failed. News ID=%s",
            news_id,
        )

        raise

    finally:

        db.close()


# ==========================================================
# STATUS
# ==========================================================

def update_news_status(
    news_id: int,
    status: str,
):

    validate_status(status)

    db = SessionLocal()

    try:

        news = (
            db.query(News)
            .filter(News.id == news_id)
            .first()
        )

        if news is None:
            return None

        news.status = status
        news.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(news)

        return news

    except Exception:
        db.rollback()
        logger.exception(
            "Status update failed. News ID=%s",
            news_id,
        )

        raise

    finally:

        db.close()

# ==========================================================
# DASHBOARD
# ==========================================================

def get_news_count():

    db = SessionLocal()

    try:

        return db.query(News).count()

    finally:

        db.close()


def get_source_count():

    db = SessionLocal()

    try:

        return (
            db.query(News.source)
            .distinct()
            .count()
        )

    finally:

        db.close()


def get_ai_pending_count():

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(
                News.ai_processed == False,
                News.status.in_(("new", "ai_pending", "ai_error")),
            )
            .count()
        )

    finally:

        db.close()


def get_ai_ready_count():

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.status == "ai_ready")
            .count()
        )

    finally:

        db.close()


def get_published_count():

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.published == True)
            .count()
        )

    finally:

        db.close()


def get_duplicate_count():

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.is_duplicate == True)
            .count()
        )

    finally:

        db.close()

# ==========================================================
# DROPDOWNLAR
# ==========================================================

def get_sources():

    db = SessionLocal()

    try:

        rows = (
            db.query(News.source)
            .distinct()
            .order_by(News.source)
            .all()
        )

        return [row[0] for row in rows if row[0]]

    finally:

        db.close()


def get_categories():

    db = SessionLocal()

    try:

        rows = (
            db.query(News.category)
            .distinct()
            .order_by(News.category)
            .all()
        )

        return [row[0] for row in rows if row[0]]

    finally:

        db.close()

def get_brands():

    db = SessionLocal()

    try:

        rows = (
            db.query(News.brand)
            .distinct()
            .order_by(News.brand)
            .all()
        )

        return [row[0] for row in rows if row[0]]

    finally:

        db.close()

# ==========================================================
# EDITOR LIST
# ==========================================================

def get_editor_news(
    limit: int = 100,
) -> list[News]:

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .order_by(desc(News.created_at))
            .limit(limit)
            .all()
        )

    finally:

        db.close()


def get_news_by_status(
    status: str,
    limit: int = 100,
) -> list[News]:

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.status == status)
            .order_by(desc(News.created_at))
            .limit(limit)
            .all()
        )

    finally:

        db.close()

# ==========================================================
# SEARCH
# ==========================================================

def search_news(
    keyword: str,
    limit: int = 100,
) -> list[News]:

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(
                News.title.ilike(f"%{keyword}%")
            )
            .order_by(desc(News.created_at))
            .limit(limit)
            .all()
        )

    finally:

        db.close()

# ==========================================================
# FILTER
# ==========================================================

def filter_news(

    status: str | None = None,
    brand: str | None = None,
    category: str | None = None,
    limit: int = 100,

):

    db = SessionLocal()

    try:

        query = db.query(News)

        if status:
            query = query.filter(
                News.status == status
            )

        if brand:
            query = query.filter(
                News.brand == brand
            )

        if category:
            query = query.filter(
                News.category == category
            )

        return (
            query
            .order_by(desc(News.created_at))
            .limit(limit)
            .all()
        )

    finally:

        db.close()

# ==========================================================
# BULK STATUS
# ==========================================================

def bulk_update_status(
    news_ids: list[int],
    status: str,
) -> int:


    validate_status(status)

    db = SessionLocal()

    try:

        rows = (
            db.query(News)
            .filter(
                News.id.in_(news_ids)
            )
            .all()
        )

        for news in rows:

            news.status = status
            news.updated_at = datetime.utcnow()

        db.commit()

        return len(rows)
    except Exception:
        db.rollback()

        logger.exception(
            "Bulk status update failed. Count=%d",
            len(news_ids),
        )

        raise

    finally:

        db.close()

# ==========================================================
# BULK DELETE
# ==========================================================

def bulk_delete_news(
    news_ids: list[int],
) -> int:

    db = SessionLocal()

    try:

        rows = (
            db.query(News)
            .filter(
                News.id.in_(news_ids)
            )
            .all()
        )

        count = len(rows)

        for news in rows:
            news.status = "deleted"
            news.updated_at = datetime.utcnow()

        db.commit()

        return count

    except Exception:
        db.rollback()
        logger.exception(
            "Bulk delete failed. Count=%d",
            len(news_ids),
        )

        raise

    finally:

        db.close()

# ==========================================================
# DASHBOARD
# ==========================================================

def get_editor_pending_count():

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(
                News.status == "editor_review"
            )
            .count()
        )

    finally:

        db.close()

# ==========================================================
# BULK AI REPROCESS
# ==========================================================

def bulk_reprocess_ai(
    news_ids: list[int],
) -> int:

    db = SessionLocal()

    try:

        rows = (
            db.query(News)
            .filter(News.id.in_(news_ids))
            .all()
        )

        for news in rows:

            news.ai_processed = False

            news.translated_title = None
            news.summary = None

            news.brand = None
            news.category = None
            news.importance = None

            news.instagram_title = None
            news.instagram_caption = None
            news.hashtags = None
            news.image_prompt = None

            news.editor_note = None

            news.status = "ai_pending"
            news.updated_at = datetime.utcnow()

        db.commit()

        return len(rows)

    except Exception:
        db.rollback()
        logger.exception(
            "Bulk AI reprocess failed. Count=%d",
            len(news_ids),
        )

        raise

    finally:

        db.close()
