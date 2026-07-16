import os

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# Telegram
# ==========================================================

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

# ==========================================================
# AI Configuration
# ==========================================================

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:4b",
)

AI_BATCH_SIZE = int(
    os.getenv(
        "AI_BATCH_SIZE",
        "1",
    )
)

MAX_CONTENT_LENGTH = int(
    os.getenv(
        "MAX_CONTENT_LENGTH",
        "1500",
    )
)

AI_TIMEOUT = int(
    os.getenv(
        "AI_TIMEOUT",
        "120",
    )
)

AI_LOGGING = (
    os.getenv(
        "AI_LOGGING",
        "true",
    ).lower()
    == "true"
)
OLLAMA_KEEP_ALIVE = os.getenv(
    "OLLAMA_KEEP_ALIVE",
    "30m",
)

OLLAMA_NUM_CTX = int(
    os.getenv(
        "OLLAMA_NUM_CTX",
        "2048",
    )
)

OLLAMA_TEMPERATURE = float(
    os.getenv(
        "OLLAMA_TEMPERATURE",
        "0.2",
    )
)
# ==========================================================
# Ollama Advanced Configuration
# ==========================================================

OLLAMA_NUM_PREDICT = int(
    os.getenv(
        "OLLAMA_NUM_PREDICT",
        "180",
    )
)

OLLAMA_TOP_K = int(
    os.getenv(
        "OLLAMA_TOP_K",
        "20",
    )
)

OLLAMA_TOP_P = float(
    os.getenv(
        "OLLAMA_TOP_P",
        "0.8",
    )
)