from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from secrets import token_urlsafe

from src.shortener.models import ShortUrlOrm
from src.shortener.schemas import SUrl


shortener_router = APIRouter(
    tags=["Shortener"],
)


@shortener_router.post("/")
async def shortener_url(
    url: SUrl, session: AsyncSession = Depends(get_async_session)
) -> dict:
    short_url = token_urlsafe(6)
    url = url.original_url
    data = await get_url_by_orig(url, session)
    if data is not None:
        return {"status_code": 200, "info": "There is an abbreviation for this link"}
    url = ShortUrlOrm(short_url=short_url, original_url=url)
    session.add(url)
    await session.commit()
    await session.refresh(url)
    return {
        "status_code": 201,
    }


async def get_url_by_orig(url: str, session: AsyncSession) -> str | None:
    query = select(ShortUrlOrm).filter(ShortUrlOrm.original_url == url)
    data = await session.execute(query)
    url = data.first()
    if url is None:
        return None
    return url[0]


@shortener_router.get("/{url_id}")
async def get_original_url(
    url_id: int, session: AsyncSession = Depends(get_async_session)
) -> dict:
    url = await get_url_by_id(url_id, session)
    if url is None:
        return {"status_code": 404, "info": "There is no such link"}
    return {
        "status_code": 307,
        "Location": url,
    }


async def get_url_by_id(url_id: int, session: AsyncSession) -> str | None:
    query = select(ShortUrlOrm).filter(ShortUrlOrm.id == url_id)
    data = await session.execute(query)
    url = data.first()
    if url is None:
        return None
    return url[0].original_url
