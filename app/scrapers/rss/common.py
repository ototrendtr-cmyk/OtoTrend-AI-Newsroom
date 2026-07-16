import feedparser


def read_rss(url, source_name, limit=10):

    print(f"OKUNAN KAYNAK: {source_name}")

    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:limit]:

        haber = {

            "title": item.get("title"),

            "description": item.get("summary"),

            "content": (
                item.content[0].value
                if hasattr(item, "content") and item.content
                else None
            ),

            "link": item.get("link"),

            "source": source_name,

            "author": item.get("author"),

            "published_at": item.get("published"),

            "language": feed.feed.get("language"),

        }

        news.append(haber)

    return news