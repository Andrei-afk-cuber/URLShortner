from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings

engine = create_async_engine(settings.db.url, echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


# Get session dependency
async def get_session():
    async with async_session() as session:
        yield session


session_dep = Annotated[AsyncSession, Depends(get_session)]
