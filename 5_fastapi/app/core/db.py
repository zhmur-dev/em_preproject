from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import settings


engine = create_async_engine(settings.database_url, echo=True)

# noinspection PyTypeChecker
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase): pass
