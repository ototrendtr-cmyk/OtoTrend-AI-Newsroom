from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.source_service import (
    list_sources,
    get_source_by_id,
    create_new_source,
    update_existing_source,
    remove_source,
    get_enabled_sources,
)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/sources")
def sources_page(request: Request):

    sources = list_sources()

    return templates.TemplateResponse(
        request=request,
        name="sources/list.html",
        context={
            "request": request,
            "sources": sources,
        },
    )


@router.get("/sources/new")
def new_source_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="sources/form.html",
        context={
            "request": request,
        },
    )


@router.post("/sources/new")
def create_source_page(
    name: str = Form(...),
    rss_url: str = Form(...),
    website: str = Form(""),
    scraper: str = Form(...),
):

    create_new_source(
        name=name,
        rss_url=rss_url,
        website=website,
        scraper=scraper,
    )

    return RedirectResponse(
        url="/sources",
        status_code=303,
    )


@router.get("/sources/{source_id}/edit")
def edit_source_page(
    request: Request,
    source_id: int,
):

    source = get_source_by_id(source_id)

    if source is None:

        return RedirectResponse(
            url="/sources",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="sources/edit.html",
        context={
            "request": request,
            "source": source,
        },
    )


@router.post("/sources/{source_id}/edit")
def edit_source(
    source_id: int,
    name: str = Form(...),
    rss_url: str = Form(...),
    website: str = Form(""),
    scraper: str = Form(...),
    priority: int = Form(1),
    enabled: str | None = Form(None),
):

    update_existing_source(
        source_id=source_id,
        name=name,
        rss_url=rss_url,
        website=website,
        scraper=scraper,
        enabled=enabled is not None,
        priority=priority,
    )

    return RedirectResponse(
        url="/sources",
        status_code=303,
    )


@router.post("/sources/{source_id}/delete")
def delete_source_page(source_id: int):

    remove_source(source_id)

    return RedirectResponse(
        url="/sources",
        status_code=303,
    )


@router.get("/test-enabled-sources")
def test_enabled_sources():

    sources = get_enabled_sources()

    return [
        {
            "id": source.id,
            "name": source.name,
            "scraper": source.scraper,
            "priority": source.priority,
            "enabled": source.enabled,
        }
        for source in sources
    ]