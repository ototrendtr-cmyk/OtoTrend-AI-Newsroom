from app.database.crud import (
    get_news_count,
    get_source_count,
    get_ai_pending_count,
    get_published_count,
    get_sources,
    get_categories,
)


def get_dashboard_data():

    return {

        "news_count": get_news_count(),

        "source_count": get_source_count(),

        "pending_count": get_ai_pending_count(),

        "published_count": get_published_count(),

        "sources": get_sources(),

        "categories": get_categories(),

    }