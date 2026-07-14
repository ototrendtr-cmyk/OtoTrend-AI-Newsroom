from app.database.database import SessionLocal
from app.models.source import Source

from app.database.source_crud import (
    get_all_sources,
    get_source,
    create_source,
    update_source,
    delete_source,
)


def get_enabled_sources():

    db = SessionLocal()

    try:

        return (
            db.query(Source)
            .filter(Source.enabled == True)
            .order_by(Source.priority)
            .all()
        )

    finally:

        db.close()


def list_sources():
    return get_all_sources()


def get_source_by_id(source_id: int):
    return get_source(source_id)


def create_new_source(
    name: str,
    rss_url: str,
    website: str,
    scraper: str,
):
    return create_source(
        name=name,
        rss_url=rss_url,
        website=website,
        scraper=scraper,
    )


def update_existing_source(
    source_id: int,
    name: str,
    rss_url: str,
    website: str,
    scraper: str,
    enabled: bool,
    priority: int,
):
    return update_source(
        source_id=source_id,
        name=name,
        rss_url=rss_url,
        website=website,
        scraper=scraper,
        enabled=enabled,
        priority=priority,
    )


def remove_source(source_id: int):
    return delete_source(source_id)