from typing import Union

from db.base import Base

from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


async def proceed_models(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
