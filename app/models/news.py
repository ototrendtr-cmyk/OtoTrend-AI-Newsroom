from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Text,
)

from app.database.database import Base


class News(Base):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True)

    # Ham haber
    title = Column(Text)
    link = Column(String, unique=True)
    source = Column(String)

    # AI tarafından oluşturulacak alanlar
    translated_title = Column(Text)
    summary = Column(Text)

    instagram_title = Column(Text)
    instagram_caption = Column(Text)

    hashtags = Column(Text)
    image_prompt = Column(Text)

    # Otomatik analiz
    category = Column(String(100))
    brand = Column(String(100))
    language = Column(String(20))

    importance = Column(Integer, default=0)

    # İş akışı
    status = Column(String(30), default="new")

    published = Column(Boolean, default=False)