from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.news import News

from app.ai.pipeline import process
from app.services.ai_queue_service import review_status_for_importance
BATCH_SIZE = 3

def process_ai_news(news_id: int | None = None):

    db: Session = SessionLocal()

    try:

        # --------------------------------------------------
        # Tek haber AI tekrar üret
        # --------------------------------------------------

        if news_id is not None:

            news = (
                db.query(News)
                .filter(News.id == news_id)
                .first()
            )

            if not news:
                print(f"❌ Haber bulunamadı: {news_id}")
                return

            print(f"🔄 AI yeniden üretiliyor: {news.id}")

            # AI alanlarını sıfırla
            news.ai_processed = False

            news.translated_title = None
            news.summary = None

            news.brand = None
            news.category = None
            news.importance = None
            news.ai_attempts = 0
            news.ai_last_error = None
            news.ai_next_retry_at = None

            # Instagram içeriklerini temizle
            news.instagram_title = None
            news.instagram_caption = None
            news.hashtags = None
            news.image_prompt = None

            # Editör alanlarını sıfırla
            news.status = "ai_pending"
            news.editor_note = None

            db.commit()
            db.refresh(news)

            news_list = [news]

        # --------------------------------------------------
        # Scheduler (eski davranış)
        # --------------------------------------------------

        else:

            news_list = (
                db.query(News)
                .filter(
                    News.ai_processed == False,
                    News.status.in_(["new", "ai_pending", "ai_error"])
                )
                .order_by(News.id.asc())
                .limit(BATCH_SIZE)
                .all()
            )

        print(f"🤖 AI: {len(news_list)} haber işleniyor...")

        for news in news_list:

            try:

                result, metrics = process(news.content or news.title)

                if not result:
                    raise ValueError("AI sonucu boş döndü.")

                news.translated_title = result.get("title_tr") or news.title
                news.summary = result.get("summary_tr") or ""
                news.brand = result.get("brand")
                news.category = result.get("category")
                try:
                    news.importance = int(result.get("importance") or 0)
                except (TypeError, ValueError):
                    news.importance = 0
                news.ai_processed = True
                # Editörün bilinçli olarak yeniden işlediği bir haber, puanı
                # ne olursa olsun inceleme için hazır kabul edilir.
                news.status = (
                    "ai_ready"
                    if news_id is not None
                    else review_status_for_importance(news.importance)
                )

                db.commit()

                print(f"✅ AI işlendi: {news.id}")

            except Exception as e:

                db.rollback()

                try:

                    news.status = "ai_error"
                    news.ai_processed = False

                    db.commit()

                except Exception:

                    db.rollback()

                print(f"❌ Haber işlenemedi ({news.id}): {e}")

    finally:

        db.close()
