from sqlalchemy import Column, Integer, String

from app.database.database import Base


class News(Base):

    __tablename__ = "news"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    link = Column(String, unique=True)

    source = Column(String)