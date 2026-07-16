from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.news_service import update_news
from app.services.ai_worker import process_ai_news


scheduler = BackgroundScheduler()


def start_scheduler():

    if scheduler.running:
        return

    # ==========================================================
    # RSS Haber Toplama
    # ==========================================================

    scheduler.add_job(
        update_news,
        "interval",
        minutes=5,
        id="news_job",
        replace_existing=True,
        next_run_time=datetime.now(),
    )

    # ==========================================================
    # AI Worker
    # ==========================================================

    scheduler.add_job(
        process_ai_news,
        "interval",
        seconds=30,
        kwargs={"limit": 1},
        id="ai_job",
        replace_existing=True,
    )

    scheduler.start()

    print("⏰ Scheduler başlatıldı.")
    print("   📰 RSS Worker : 5 dakikada bir")
    print("   🤖 AI Worker  : 30 saniyede bir (1 haber)")