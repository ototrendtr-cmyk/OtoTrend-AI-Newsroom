import os
import secrets

from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development").lower()
IS_PRODUCTION = APP_ENV == "production"


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

# ==========================================================
# Telegram
# ==========================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Yeni bildirimlerin başlangıç anı. Boş bırakıldığında geçmiş haberler için
# toplu Telegram gönderimi yapılmaz.
TELEGRAM_NOTIFY_AFTER = os.getenv("TELEGRAM_NOTIFY_AFTER", "").strip()


def _require_env(name: str, value: str | None) -> str:
    if not value or not value.strip():
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

# Development uses a temporary key; production must receive a stable key from
# the hosting environment so users are not logged out after every restart.
SECRET_KEY = os.getenv("SECRET_KEY")
if IS_PRODUCTION:
    SECRET_KEY = _require_env("SECRET_KEY", SECRET_KEY)
elif not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(32)

RUN_SCHEDULER = env_flag("RUN_SCHEDULER", default=True)
OLLAMA_HOST = os.getenv("OLLAMA_HOST")

# ==========================================================
# Haber saklama politikası
# ==========================================================

# Haberler ilk 90 gün normal iş akışında kalır. Bu sürenin sonunda
# arşivlenir; bir yılı geçen arşiv kayıtları ise önce SQLite yedeği
# alındıktan sonra temizlenir.
NEWS_RETENTION_ENABLED = env_flag("NEWS_RETENTION_ENABLED", default=True)
NEWS_ARCHIVE_AFTER_DAYS = int(os.getenv("NEWS_ARCHIVE_AFTER_DAYS", "90"))
NEWS_DELETE_AFTER_DAYS = int(os.getenv("NEWS_DELETE_AFTER_DAYS", "365"))

if NEWS_ARCHIVE_AFTER_DAYS < 1:
    raise RuntimeError("NEWS_ARCHIVE_AFTER_DAYS en az 1 olmalıdır.")
if NEWS_DELETE_AFTER_DAYS <= NEWS_ARCHIVE_AFTER_DAYS:
    raise RuntimeError(
        "NEWS_DELETE_AFTER_DAYS, NEWS_ARCHIVE_AFTER_DAYS değerinden büyük olmalıdır."
    )

# ==========================================================
# AI Configuration
# ==========================================================

# "auto" seçildiğinde OPENAI_API_KEY varsa OpenAI, yoksa mevcut Ollama
# kurulumu kullanılır. "openai" seçimi anahtar yoksa açık bir hata verir.
AI_PROVIDER = os.getenv("AI_PROVIDER", "auto").strip().lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6").strip()
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "120"))

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
        "800",
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
        "4096",
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
        "120",
    )
)

# Instagram üretimi başlık ve açıklama alanlarını birlikte döndürür. Genel
# sohbet sınırını yükseltmeden, bu akış için yeterli ve öngörülebilir bir
# yanıt bütçesi kullanılır.
INSTAGRAM_NUM_PREDICT = int(
    os.getenv(
        "INSTAGRAM_NUM_PREDICT",
        "420",
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
