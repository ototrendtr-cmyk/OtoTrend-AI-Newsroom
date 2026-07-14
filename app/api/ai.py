from fastapi import APIRouter

from app.database.database import SessionLocal
from app.models.source import Source
from app.services.telegram_service import send_telegram_message

router = APIRouter(
    prefix="/api",
    tags=["AI"],
)


@router.get("/test-telegram")
def test_telegram():

    send_telegram_message("✅ OtoTrend AI Telegram test mesajı")

    return {
        "success": True,
        "message": "Telegram test mesajı gönderildi."
    }


@router.get("/health")
def health():

    db = SessionLocal()

    try:

        return {
            "status": "ok",
            "database": True,
            "sources": db.query(Source).count(),
        }

    finally:

        db.close()