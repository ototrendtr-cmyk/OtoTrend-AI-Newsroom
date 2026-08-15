import html
import re
import unicodedata

from app.config import MAX_CONTENT_LENGTH

SCRIPT_RE = re.compile(
    r"<script.*?>.*?</script>",
    re.IGNORECASE | re.DOTALL,
)

STYLE_RE = re.compile(
    r"<style.*?>.*?</style>",
    re.IGNORECASE | re.DOTALL,
)

TAG_RE = re.compile(
    r"<[^>]+>",
)

WHITESPACE_RE = re.compile(
    r"\s+",
)

# Gereksiz satırlar
NOISE_PATTERNS = [
    r"Read more.*",
    r"Continue reading.*",
    r"Originally published.*",
    r"Advertisement.*",
    r"Source:.*",
    r"All rights reserved.*",
    r"©.*",
]


def clean_text(text: str | None) -> str:
    """
    AI'ya gönderilecek metni temizler.
    """

    if not text:
        return ""

    # HTML entity
    text = html.unescape(text)

    # Script
    text = SCRIPT_RE.sub("", text)

    # Style
    text = STYLE_RE.sub("", text)

    # HTML tag
    text = TAG_RE.sub(" ", text)

    # Unicode normalize
    text = unicodedata.normalize(
        "NFKC",
        text,
    )

    # Gereksiz satırları kaldır
    for pattern in NOISE_PATTERNS:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE,
        )

    # Fazla boşluk
    text = WHITESPACE_RE.sub(
        " ",
        text,
    ).strip()

    # Maksimum karakter
    if len(text) > MAX_CONTENT_LENGTH:
        text = text[:MAX_CONTENT_LENGTH]

    return text


def prompt_length(text: str) -> int:
    return len(text)


def prompt_size_kb(text: str) -> float:
    return round(
        len(text.encode("utf-8")) / 1024,
        2,
    )


def debug_prompt(news: str, prompt: str):
    """
    Debug amaçlı prompt bilgisi.
    """

    print("--------------------------------")
    print(f"News Length   : {len(news)} karakter")
    print(f"Prompt Length : {len(prompt)} karakter")
    print(f"Prompt Size   : {prompt_size_kb(prompt)} KB")
    print("News Preview:")
    print(news[:300])
    print("--------------------------------")