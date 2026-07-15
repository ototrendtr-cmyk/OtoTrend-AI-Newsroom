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

from datetime import datetime


def mark_source_run(source_name: str):
    db = SessionLocal()

    try:

        source = (
            db.query(Source)
            .filter(Source.name == source_name)
            .first()
        )

        if source:
            source.last_run = datetime.utcnow()
            db.commit()

    finally:
        db.close()


def mark_source_success(source_name: str, news_count: int):

    db = SessionLocal()

    try:

        source = (
            db.query(Source)
            .filter(Source.name == source_name)
            .first()
        )

        if source:

            source.last_success = datetime.utcnow()
            source.success_count += 1
            source.total_news += news_count
            source.last_error = None

            db.commit()

    finally:
        db.close()


def mark_source_error(source_name: str, error_message: str):

    db = SessionLocal()

    try:

        source = (
            db.query(Source)
            .filter(Source.name == source_name)
            .first()
        )

        if source:

            source.error_count += 1
            source.last_error = error_message
            source.last_run = datetime.utcnow()

            db.commit()

    finally:
        db.close()        