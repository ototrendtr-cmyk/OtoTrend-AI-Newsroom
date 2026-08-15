from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

from app.database.database import SessionLocal
from app.services.dashboard_service import get_dashboard_stats
from app.services.news_service import update_news

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard API"],
)


def require_authenticated(request: Request):
    if not request.session.get("authenticated"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/stats")
def dashboard_stats(request: Request):
    """
    Dashboard KPI verileri
    """

    require_authenticated(request)

    db = SessionLocal()

    try:
        return get_dashboard_stats(db)

    finally:
        db.close()


@router.post("/refresh", status_code=status.HTTP_202_ACCEPTED)
def refresh_news(request: Request, background_tasks: BackgroundTasks):
    require_authenticated(request)
    background_tasks.add_task(update_news)
    return {"status": "started"}
