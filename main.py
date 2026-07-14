from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.database import Base, engine

from app.scheduler.news_scheduler import start_scheduler

# Views
from app.views.dashboard import router as dashboard_router
from app.views.news import router as news_router
from app.views.sources import router as source_router

# API
from app.api.news import router as api_news_router
from app.api.source import router as api_source_router
from app.api.ai import router as ai_router

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 OtoTrend AI başlatılıyor...")

    start_scheduler()

    yield

    print("🛑 OtoTrend AI durduruldu.")


app = FastAPI(

    title="OtoTrend AI CMS",

    version="2.1.0",

    lifespan=lifespan,

)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

# Views
app.include_router(dashboard_router)
app.include_router(news_router)
app.include_router(source_router)


# API
app.include_router(api_news_router)
app.include_router(api_source_router)
app.include_router(ai_router)