from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.news_service import update_news

scheduler = BackgroundScheduler()


def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(
        update_news,
        "interval",
        minutes=1,
        id="news_job",
        replace_existing=True,
        next_run_time=datetime.now(),  # Uygulama açılır açılmaz ilk tarama
    )

    scheduler.start()

    print("⏰ Scheduler başlatıldı. (1 dakikada bir)")