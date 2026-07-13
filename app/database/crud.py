from app.database.database import SessionLocal
from app.models.news import News


def save_news(news_list):

    db = SessionLocal()

    new_news = []

    for item in news_list:

        exists = db.query(News).filter(
            News.link == item["link"]
        ).first()

        if not exists:

            news = News(
                title=item["title"],
                link=item["link"],
                source=item["source"]
            )

            db.add(news)

            new_news.append(item)

    db.commit()

    db.close()

    return new_news


def get_all_news():

    db = SessionLocal()

    news = db.query(News).all()

    db.close()

    return news


def get_news_count():

    db = SessionLocal()

    count = db.query(News).count()

    db.close()

    return count