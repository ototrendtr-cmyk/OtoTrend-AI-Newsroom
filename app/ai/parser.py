import json
import re


def parse_json(text: str):
    """
    AI çıktısından JSON'u güvenli şekilde ayıklar.
    """

    text = text.strip()

    # ```json ... ``` bloğunu kaldır
    text = re.sub(r"^```json", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^```", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    # JSON bloğunu bul
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("AI JSON döndürmedi.")

    return json.loads(match.group())