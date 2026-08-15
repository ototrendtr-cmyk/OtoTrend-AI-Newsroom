import time

from app.config import (
    OLLAMA_HOST,
    OLLAMA_KEEP_ALIVE,
    OLLAMA_MODEL,
)
import ollama


client = ollama.Client(host=OLLAMA_HOST) if OLLAMA_HOST else ollama.Client()


def warmup():
    """
    Ollama modelini belleğe yükler ve belirli süre RAM'de tutar.
    """

    print()
    print("🔥 AI Warmup başlıyor...")

    start = time.perf_counter()

    try:

        client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Ready",
                }
            ],
            keep_alive=OLLAMA_KEEP_ALIVE,
            options={
                "num_ctx": 256,
            },
        )

        elapsed = time.perf_counter() - start

        print(
            f"✅ AI Warmup tamamlandı ({elapsed:.2f} sn)"
        )

        print(
            f"🧠 Model RAM'de tutuluyor ({OLLAMA_KEEP_ALIVE})"
        )

    except Exception as e:

        print(
            f"❌ AI Warmup Hatası: {e}"
        )

    print()
