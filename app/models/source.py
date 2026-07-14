from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)

from app.database.database import Base


class Source(Base):

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)

    # ==========================
    # Temel Bilgiler
    # ==========================

    name = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    website = Column(Text)

    rss_url = Column(Text)

    scraper = Column(
        String(50),
        default="rss",
    )

    language = Column(
        String(20),
        default="en",
    )

    country = Column(
        String(50),
        default="Global",
    )

    # ==========================
    # Yönetim
    # ==========================

    enabled = Column(
        Boolean,
        default=True,
    )

    priority = Column(
        Integer,
        default=1,
    )

    # ==========================
    # İstatistik
    # ==========================

    total_news = Column(
        Integer,
        default=0,
    )

    success_count = Column(
        Integer,
        default=0,
    )

    error_count = Column(
        Integer,
        default=0,
    )

    last_run = Column(DateTime)

    last_success = Column(DateTime)

    last_error = Column(Text)

    # ==========================
    # Sistem
    # ==========================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )