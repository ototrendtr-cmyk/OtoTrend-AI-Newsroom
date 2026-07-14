from typing import Optional

from fastapi import APIRouter

from app.database.crud import get_news, get_news_by_id

router = APIRouter(
    prefix="/api/news",
    tags=["News"],
)


@router.get("/")
def list_news(
    keyword: Optional[str] = None,
    source: Optional[str] = None,
    category: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
):
    return get_news(
        keyword=keyword,
        source=source,
        category=category,
        page=page,
        page_size=page_size,
    )


@router.get("/{news_id}")
def news_detail(news_id: int):
    return get_news_by_id(news_id)