from sqlalchemy import desc

from app.database.database import SessionLocal
from app.models.news import News
from app.services.duplicate_service import is_similar


# ==========================================================
# HABER KAYDET
# ==========================================================

def save_news(news_list):

    db = SessionLocal()

    new_news = []

    duplicate_link = 0
    duplicate_title = 0

    try:

        # Başlıkları bir kez oku
        existing_titles = (
            db.query(News.title)
            .all()
        )

        for item in news_list:

            # Aynı link kontrolü
            exists = (
                db.query(News)
                .filter(News.link == item["link"])
                .first()
            )

            if exists:

                duplicate_link += 1

                print(
                    f"🔁 Aynı link bulundu: {item['title']}"
                )

                continue

            # Benzer başlık kontrolü
            duplicate = False

            for row in existing_titles:

                if not row[0]:
                    continue

                if is_similar(
                    item["title"],
                    row[0],
                ):
                    duplicate = True
                    break

            if duplicate:

                duplicate_title += 1

                print(
                    f"🟡 Benzer başlık bulundu: {item['title']}"
                )

                continue

            news = News(

                title=item.get("title"),

                link=item.get("link"),

                source=item.get("source"),

                author=item.get("author"),

                image_url=item.get("image_url"),

                language=item.get("language", "en"),

                published_at=item.get("published_at"),

            )

            db.add(news)

            new_news.append(news)

        print("-----------------------------------")
        print(f"Yeni Haber      : {len(new_news)}")
        print(f"Aynı Link       : {duplicate_link}")
        print(f"Benzer Başlık   : {duplicate_title}")
        print("-----------------------------------")

        db.commit()

        return new_news

    finally:

        db.close()

# ==========================================================
# HABERLER
# ==========================================================

def get_news(
    keyword=None,
    source=None,
    category=None,
    page=1,
    page_size=20,
):

    db = SessionLocal()

    try:

        query = db.query(News)

        if keyword:

            query = query.filter(
                News.title.ilike(f"%{keyword}%")
            )

        if source:

            query = query.filter(
                News.source == source
            )

        if category:

            query = query.filter(
                News.category == category
            )

        total = query.count()

        items = (
            query
            .order_by(desc(News.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {

            "total": total,

            "page": page,

            "page_size": page_size,

            "items": items,

        }

    finally:

        db.close()


# ==========================================================
# DETAY
# ==========================================================

def get_news_by_id(news_id):

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.id == news_id)
            .first()
        )

    finally:

        db.close()


# ==========================================================
# DASHBOARD
# ==========================================================

def get_news_count():

    db = SessionLocal()

    try:

        return db.query(News).count()

    finally:

        db.close()


def get_source_count():

    db = SessionLocal()

    try:

        return (
            db.query(News.source)
            .distinct()
            .count()
        )

    finally:

        db.close()


def get_ai_pending_count():

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.ai_processed == False)
            .count()
        )

    finally:

        db.close()


def get_published_count():

    db = SessionLocal()

    try:

        return (
            db.query(News)
            .filter(News.published == True)
            .count()
        )

    finally:

        db.close()


# ==========================================================
# DROPDOWNLAR
# ==========================================================

def get_sources():

    db = SessionLocal()

    try:

        rows = (
            db.query(News.source)
            .distinct()
            .order_by(News.source)
            .all()
        )

        return [r[0] for r in rows if r[0]]

    finally:

        db.close()


def get_categories():

    db = SessionLocal()

    try:

        rows = (
            db.query(News.category)
            .distinct()
            .order_by(News.category)
            .all()
        )

        return [r[0] for r in rows if r[0]]

    finally:

        db.close()