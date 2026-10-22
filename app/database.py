from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import asyncio

# from .config import Settings
from app.config import settings

engine = create_async_engine(settings.db.url, echo=True)

session_factory = async_sessionmaker(bind=engine)
