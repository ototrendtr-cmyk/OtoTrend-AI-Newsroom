from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.database.crud import get_news_by_id

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/news/{news_id}")
def news_detail(
    request: Request,
    news_id: int,
):

    news = get_news_by_id(news_id)

    return templates.TemplateResponse(
        request=request,
        name="detail.html",
        context={
            "request": request,
            "news": news,
        },
    )