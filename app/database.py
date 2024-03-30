from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

if settings.MODE == 'TEST':
    DATABASE_PARAMS = {"poolclass": NullPool}

    engine = create_async_engine(settings.get_test_database_url, **DATABASE_PARAMS)
else:
    DATABASE_PARAMS = {}
    engine = create_async_engine(settings.get_database_url,**DATABASE_PARAMS)


async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
