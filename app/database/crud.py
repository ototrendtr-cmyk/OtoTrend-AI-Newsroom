def get_news_by_id(news_id: int):

    db = SessionLocal()

    news = (
        db.query(News)
        .filter(News.id == news_id)
        .first()
    )

    db.close()

    return news