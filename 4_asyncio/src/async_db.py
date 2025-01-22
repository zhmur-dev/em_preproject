from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = \
    f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

# noinspection PyTypeChecker
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase): pass


# Main class
class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'
    id = Column(Integer, primary_key=True, index=True)
    exchange_product_id = Column(String)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Integer)
    total = Column(Integer)
    count = Column(Integer)
    date = Column(DateTime)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)


async def reset_database():
    """
    Async function that drops current metadata and creates them anew.
    To be used for testing and debugging purposes.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
