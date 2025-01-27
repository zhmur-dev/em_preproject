import asyncio

from sqlalchemy.sql import text

from core.db import async_session


async def test_db_connection():
    async with async_session() as session:
        try:
            result = await session.execute(text('SELECT 1'))
            print(f'DB test passed! Result: {result.scalar()}')
        except Exception as e:
            print(f'DB test failed! {e}')


if __name__ == '__main__':
    asyncio.run(test_db_connection())
