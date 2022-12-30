from typing import Union

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, scoped_session

from config import db_username, db_psw, db_port, db_host, db_name

postgres_url = URL.create(
    "postgresql+asyncpg",
    username=db_username,
    password=db_psw,
    host=db_host,
    database=db_name,
    port=db_port
)

async_engine = create_async_engine(url=postgres_url, echo=True, pool_pre_ping=True)
async_session = scoped_session(sessionmaker(bind=async_engine, class_=AsyncSession))

async def proceed_schemas(engine: AsyncEngine, Base) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

