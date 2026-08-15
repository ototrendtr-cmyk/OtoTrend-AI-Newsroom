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


# ==========================================================
# Authentication Helper
# ==========================================================

def check_auth(request: Request):

    if not request.session.get("authenticated"):

        return RedirectResponse(
            url="/login",
            status_code=303,
        )

    return None


# ==========================================================
# Source List
# ==========================================================

@router.get("/sources")
def sources_page(request: Request):

    auth = check_auth(request)

    if auth:
        return auth

    sources = list_sources()

    return templates.TemplateResponse(
        request=request,
        name="sources/list.html",
        context={
            "request": request,
            "sources": sources,
        },
    )


# ==========================================================
# New Source
# ==========================================================

@router.get("/sources/new")
def new_source_page(request: Request):

    auth = check_auth(request)

    if auth:
        return auth

    return templates.TemplateResponse(
        request=request,
        name="sources/form.html",
        context={
            "request": request,
        },
    )


@router.post("/sources/new")
def create_source_page(
    request: Request,
    name: str = Form(...),
    rss_url: str = Form(...),
    website: str = Form(""),
    scraper: str = Form(...),
):

    auth = check_auth(request)

    if auth:
        return auth

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


# ==========================================================
# Edit Source
# ==========================================================

@router.get("/sources/{source_id}/edit")
def edit_source_page(
    request: Request,
    source_id: int,
):

    auth = check_auth(request)

    if auth:
        return auth

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
    request: Request,
    source_id: int,
    name: str = Form(...),
    rss_url: str = Form(...),
    website: str = Form(""),
    scraper: str = Form(...),
    priority: int = Form(1),
    enabled: str | None = Form(None),
):

    auth = check_auth(request)

    if auth:
        return auth

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


# ==========================================================
# Delete Source
# ==========================================================

@router.post("/sources/{source_id}/delete")
def delete_source_page(
    request: Request,
    source_id: int,
):

    auth = check_auth(request)

    if auth:
        return auth

    remove_source(source_id)

    return RedirectResponse(
        url="/sources",
        status_code=303,
    )


# ==========================================================
# Enabled Sources Test
# ==========================================================

@router.get("/test-enabled-sources")
def test_enabled_sources(request: Request):

    auth = check_auth(request)

    if auth:
        return auth

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