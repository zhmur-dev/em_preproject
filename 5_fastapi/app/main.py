from fastapi import FastAPI

from api.routers import main_router
from core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(main_router)
