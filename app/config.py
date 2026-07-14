import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def _require_env(name: str, value: str | None) -> str:
    if not value:
        raise RuntimeError(
            f"❌ Ortam değişkeni eksik: {name}\n"
            "Lütfen .env dosyanızı kontrol edin."
        )
    return value


TELEGRAM_BOT_TOKEN = _require_env(
    "TELEGRAM_BOT_TOKEN",
    TELEGRAM_BOT_TOKEN,
)

TELEGRAM_CHAT_ID = _require_env(
    "TELEGRAM_CHAT_ID",
    TELEGRAM_CHAT_ID,
)