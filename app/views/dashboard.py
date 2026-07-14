from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from typing import Optional

from app.database.crud import (
    get_news,
)

from app.services.dashboard_service import (
    get_dashboard_data,
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def home(
    request: Request,
    q: Optional[str] = None,
    source: Optional[str] = None,
    category: Optional[str] = None,
    page: int = 1,
):

    result = get_news(
        keyword=q,
        source=source,
        category=category,
        page=page,
        page_size=20,
    )

    dashboard = get_dashboard_data()

    context = {

        "request": request,

        "news": result["items"],
        "count": result["total"],

        "page": result["page"],
        "page_size": result["page_size"],

        "q": q or "",
        "source": source or "",
        "category": category or "",

    }

    context.update(dashboard)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=context,
    )