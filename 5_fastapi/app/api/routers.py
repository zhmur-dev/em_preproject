from fastapi import APIRouter, Depends

from core.db import get_async_session
from schemas.spimextradingresults import SpimexTradingResultsDB
from sqlalchemy.ext.asyncio import AsyncSession

from crud.spimextradingresults import spimextradingresults_crud

main_router = APIRouter()

@main_router.get(
    '/',
    response_model=SpimexTradingResultsDB,
)
async def read_root(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Temporary view to show db object with id=1 at root.
    """
    return await spimextradingresults_crud.get(
        session=session,
        obj_id=1,
    )
