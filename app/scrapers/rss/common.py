import feedparser

def read_rss(url, source_name, limit=10):

    print(f"OKUNAN KAYNAK: {source_name}")

    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:limit]:
        haber = {
            "title": item.title,
            "link": item.link,
            "source": source_name
        }

        print(haber)   # <<< bunu ekle

        news.append(haber)

    return news