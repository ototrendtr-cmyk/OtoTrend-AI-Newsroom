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


def clean_text(text: str | None) -> str:
    """
    AI'ya gönderilecek metni temizler.

    Yapılan işlemler:

    - None kontrolü
    - Script kaldırılır
    - Style kaldırılır
    - HTML tag'leri kaldırılır
    - HTML entity decode edilir
    - Unicode normalize edilir
    - Gereksiz boşluklar temizlenir
    - Maksimum karakter sınırı uygulanır
    """

    if not text:
        return ""

    # HTML entity düzelt
    text = html.unescape(text)

    # Script kaldır
    text = SCRIPT_RE.sub("", text)

    # Style kaldır
    text = STYLE_RE.sub("", text)

    # HTML tag kaldır
    text = TAG_RE.sub(" ", text)

    # Unicode normalize
    text = unicodedata.normalize(
        "NFKC",
        text,
    )

    # Fazla boşlukları temizle
    text = WHITESPACE_RE.sub(
        " ",
        text,
    ).strip()

    # Maksimum uzunluk
    if len(text) > MAX_CONTENT_LENGTH:
        text = text[:MAX_CONTENT_LENGTH]

    return text


def prompt_length(text: str) -> int:
    """
    Prompt karakter uzunluğu.
    """

    return len(text)


def prompt_size_kb(text: str) -> float:
    """
    Prompt boyutu (KB).
    """

    return round(
        len(text.encode("utf-8")) / 1024,
        2,
    )