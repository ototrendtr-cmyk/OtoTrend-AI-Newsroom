from app.database.database import SessionLocal
from app.models.source import Source


def calculate_health(source: Source) -> int:
    total = source.success_count + source.error_count

    if total == 0:
        return 100

    return int((source.success_count / total) * 100)


def update_health_scores():
    db = SessionLocal()

    try:
        sources = db.query(Source).all()

        for source in sources:
            source.health_score = calculate_health(source)

        db.commit()

    finally:
        db.close()