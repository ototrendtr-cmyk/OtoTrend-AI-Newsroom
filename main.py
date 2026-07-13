from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine
from app.database.crud import get_all_news, get_news_count
from app.scheduler.news_scheduler import start_scheduler
from app.services.telegram_service import send_telegram_message

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):

    news = get_all_news()
    count = get_news_count()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "news": news,
            "count": count,
        },
    )


@app.get("/telegram-test")
def telegram_test():

    send_telegram_message(
        "🚗 OtoTrend AI\n\n✅ Telegram bağlantısı başarıyla kuruldu."
    )

    return {"status": "Mesaj gönderildi"}