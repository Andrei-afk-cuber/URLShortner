from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from .models import Link
from .schemas import LinkBase
from .services import encode_base62


# Create link function
async def create_link(session: AsyncSession, link: LinkBase) -> Link:
    link = Link(**jsonable_encoder(link), code="code")
    session.add(link)
    await session.flush()
    link.code = encode_base62(link.id)
    await session.commit()
    return link


# Get link function
async def get_link_by_code(session: AsyncSession, code: str):
    link = await session.scalar(select(Link).where(Link.code == code))
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return link


# Clicks update
async def update_clicks(session: AsyncSession, link_id: int):
    link = await session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    link.clicks += 1
    await session.commit()
    await session.refresh(link)
    return link