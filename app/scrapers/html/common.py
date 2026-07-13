import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def read_html(
    url,
    source_name,
    article_selector,
    title_selector,
    limit=10
):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    if response.status_code != 200:
        print(f"❌ {source_name}: HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    news = []

    articles = soup.select(article_selector)

    for article in articles:

        title = article.select_one(title_selector)

        if not title:
            continue

        # Linki bul
        if title.name == "a":
            link = title.get("href")
        else:
            link = article.get("href")

        if not link:
            continue

        if link.startswith("/"):
            link = urljoin(url, link)

        news.append(
            {
                "title": title.get_text(strip=True),
                "link": link,
                "source": source_name,
            }
        )

        if len(news) >= limit:
            break

    return news