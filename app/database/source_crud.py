from app.database.database import SessionLocal
from app.models.source import Source


def create_source(
    name,
    rss_url,
    website=None,
    scraper="rss",
    language="en",
    country="Global",
):
    db = SessionLocal()

    try:
        exists = (
            db.query(Source)
            .filter(Source.name == name)
            .first()
        )

        if exists:
            return exists

        source = Source(
            name=name,
            rss_url=rss_url,
            website=website,
            scraper=scraper,
            language=language,
            country=country,
        )

        db.add(source)
        db.commit()
        db.refresh(source)

        return source

    finally:
        db.close()
def get_all_sources():

    db = SessionLocal()

    try:
        return (
            db.query(Source)
            .order_by(Source.name)
            .all()
        )

    finally:
        db.close()


def get_source(source_id):

    db = SessionLocal()

    try:
        return (
            db.query(Source)
            .filter(Source.id == source_id)
            .first()
        )

    finally:
        db.close()

def update_source(
    source_id,
    name,
    rss_url,
    website,
    scraper,
    enabled,
    priority,
):

    db = SessionLocal()

    try:

        source = (
            db.query(Source)
            .filter(Source.id == source_id)
            .first()
        )

        if not source:
            return None

        source.name = name
        source.rss_url = rss_url
        source.website = website
        source.scraper = scraper
        source.enabled = enabled
        source.priority = priority

        db.commit()
        db.refresh(source)

        return source

    finally:

        db.close()

def delete_source(source_id):

    db = SessionLocal()

    try:

        source = (
            db.query(Source)
            .filter(Source.id == source_id)
            .first()
        )

        if not source:
            return False

        db.delete(source)
        db.commit()

        return True

    finally:

        db.close()        