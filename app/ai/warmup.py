import time

import ollama

from app.config import (
    OLLAMA_KEEP_ALIVE,
    OLLAMA_MODEL,
)


def warmup():
    """
    Ollama modelini belleğe yükler ve belirli süre RAM'de tutar.
    """

    print()
    print("🔥 AI Warmup başlıyor...")

    start = time.perf_counter()

    try:

        ollama.chat(
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