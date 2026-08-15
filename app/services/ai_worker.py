from datetime import UTC, datetime
from time import perf_counter

from app.ai.logger import AILogger
from app.ai.provider import OLLAMA_MODEL
from app.config import TELEGRAM_NOTIFY_AFTER
from app.ai.stats import (
    add_failure,
    add_success,
    print_summary,
)

from app.database.database import SessionLocal
from app.models.news import News

from app.ai.pipeline import process

from app.services.telegram_service import (
    send_telegram_message,
    send_telegram_photo,
)


def _should_send_telegram(news: News) -> bool:
    """Yalnızca etkinleştirmeden sonra eklenen haberleri bildirir."""
    if news.telegram_sent or not TELEGRAM_NOTIFY_AFTER:
        return False

    try:
        cutoff = datetime.fromisoformat(
            TELEGRAM_NOTIFY_AFTER.replace("Z", "+00:00")
        )
    except ValueError:
        print("⚠️ TELEGRAM_NOTIFY_AFTER geçersiz; Telegram bildirimi atlandı.")
        return False

    if cutoff.tzinfo is None:
        cutoff = cutoff.replace(tzinfo=UTC)

    created_at = news.created_at
    if created_at is None:
        return False
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)

    return created_at >= cutoff


def process_ai_news(limit: int = 1):
    """
    AI tarafından işlenmemiş haberleri işler.
    """

    # ==========================================================
    # İşlenecek Haberleri Bul
    # ==========================================================

    db = SessionLocal()

    try:

        news_ids = [

            row.id

            for row in (

                db.query(News)

                .filter(
                    News.ai_processed == False,
                    News.status.in_(["new", "ai_pending", "ai_error"]),
                )

                .order_by(News.created_at.desc())

                .limit(limit)

                .all()

            )

        ]

    finally:

        db.close()

    # İşlenecek haber yoksa sessizce çık
    if not news_ids:
        return

    print(f"🤖 AI: {len(news_ids)} haber işleniyor...")

    # ==========================================================
    # Haberleri İşle
    # ==========================================================

    for news_id in news_ids:

        db = SessionLocal()

        logger = AILogger()

        logger.set_news(news_id)

        logger.set_model(OLLAMA_MODEL)

        try:

            news = (

                db.query(News)

                .filter(News.id == news_id)

                .first()

            )

            if news is None:

                continue

            # ==================================================
            # AI Pipeline
            # ==================================================

            result, metrics = process(

                news.content or news.title

            )

            logger.set_prompt_size(

                metrics["prompt_kb"]

            )

            logger.set_prompt_time(

                metrics["prompt_time"]

            )

            logger.set_ollama_time(

                metrics["ollama_time"]

            )

            logger.set_parse_time(

                metrics["parse_time"]

            )

            # ==================================================
            # Database Güncelle
            # ==================================================

            news.translated_title = result.get(

                "title_tr"

            )

            news.summary = result.get(

                "summary_tr"

            )

            news.brand = result.get(

                "brand"

            )

            news.category = result.get(

                "category"

            )

            news.importance = result.get(

                "importance"

            )

            news.ai_processed = True

            db_start = perf_counter()

            db.commit()

            logger.set_database_time(

                perf_counter() - db_start

            )

            # ==================================================
            # Telegram Mesajı Hazırla
            # ==================================================

            message = (

                f"🚨 OtoTrend AI\n\n"

                f"📰 {news.translated_title}\n\n"

                f"📝 {news.summary}\n\n"

                f"🌍 Kaynak: {news.source}\n\n"

                f"🏷️ Marka: {news.brand}\n"

                f"📂 Kategori: {news.category}\n"

                f"⭐ Önem: {news.importance}/10\n\n"

                f"🔗 {news.link}"

            )

            # ==================================================
            # Telegram Gönder
            # ==================================================

            telegram_start = perf_counter()
            telegram_sent = False

            if _should_send_telegram(news):
                if news.image_url:
                    telegram_sent = send_telegram_photo(
                        news.image_url,
                        message,
                    )
                else:
                    telegram_sent = send_telegram_message(message)

                if telegram_sent:
                    news.telegram_sent = True
                    db.commit()
            else:
                print("ℹ️ Telegram atlandı: haber bildirim başlangıcından önce eklenmiş.")

            logger.set_telegram_time(
                perf_counter() - telegram_start
            )

            # ==================================================
            # Logger
            # ==================================================

            logger.finish()

            logger.print()

            # ==================================================
            # Statistics
            # ==================================================

            add_success(
                model=OLLAMA_MODEL,
                prompt_kb=metrics["prompt_kb"],
                response_kb=metrics["response_kb"],
                duration=logger.total_time,
            )

            print(
                f"✅ AI işlendi: {news.title}"
            )

        except Exception as e:

            db.rollback()

            add_failure()

            print()

            print("❌ AI Worker Hatası")

            print(f"📰 Haber ID : {news_id}")

            print(f"⚠️ {e}")

            print()

        finally:

            db.close()

    # ==========================================================
    # Final Statistics
    # ==========================================================

    print_summary()

    print()

    print("🤖 AI Worker tamamlandı.")

    print()
