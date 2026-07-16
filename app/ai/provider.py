import ollama

from app.config import (
    OLLAMA_KEEP_ALIVE,
    OLLAMA_MODEL,
    OLLAMA_NUM_CTX,
    OLLAMA_NUM_PREDICT,
    OLLAMA_TEMPERATURE,
    OLLAMA_TOP_K,
    OLLAMA_TOP_P,
)


def chat(prompt: str) -> str:

    response = ollama.chat(

        model=OLLAMA_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        keep_alive=OLLAMA_KEEP_ALIVE,

        options={

            "num_ctx": OLLAMA_NUM_CTX,

            "temperature": OLLAMA_TEMPERATURE,

            "num_predict": OLLAMA_NUM_PREDICT,

            "top_k": OLLAMA_TOP_K,

            "top_p": OLLAMA_TOP_P,

        },

    )

    return response.message.content.strip()