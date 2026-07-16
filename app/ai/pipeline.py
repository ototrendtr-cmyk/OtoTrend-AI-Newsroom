import time

from app.ai.cleaner import clean_text, prompt_size_kb
from app.ai.provider import chat
from app.ai.parser import parse_json


PROMPT_TEMPLATE = """
Türkçe otomotiv editörü olarak aşağıdaki haberi analiz et.

Kurallar:
- title_tr: Akıcı Türkçe başlık.
- summary_tr: En fazla 2 cümle.
- brand: Sadece marka.
- model: Sadece model.
- importance: 1-10.

category sadece şu değerlerden biri olabilir:

EV
Hybrid
ICE
SUV
Sedan
Hatchback
Pickup
Battery
Charging
Software
Recall
Factory
Motorsport
Financial
Other

Sadece JSON döndür.

{{
  "title_tr":"",
  "summary_tr":"",
  "brand":"",
  "model":"",
  "category":"",
  "importance":0
}}


Haber:

{news}
"""


def process(news: str):

    metrics = {
        "prompt_time": 0.0,
        "ollama_time": 0.0,
        "parse_time": 0.0,
        "prompt_kb": 0.0,
        "response_kb": 0.0,
    }

    # ==========================================================
    # Prompt
    # ==========================================================

    start = time.perf_counter()

    news = clean_text(news)

    prompt = PROMPT_TEMPLATE.format(
        news=news,
    )

    metrics["prompt_time"] = (
        time.perf_counter() - start
    )

    metrics["prompt_kb"] = prompt_size_kb(
        prompt
    )

    # ==========================================================
    # Ollama
    # ==========================================================

    start = time.perf_counter()

    response = chat(
        prompt,
    )

    metrics["ollama_time"] = (
        time.perf_counter() - start
    )

    metrics["response_kb"] = round(
        len(
            response.encode(
                "utf-8"
            )
        )
        / 1024,
        2,
    )

    # ==========================================================
    # Parse
    # ==========================================================

    start = time.perf_counter()

    result = parse_json(
        response,
    )

    metrics["parse_time"] = (
        time.perf_counter() - start
    )

    return result, metrics