from fastapi import APIRouter


main_router = APIRouter()

@main_router.get(
    '/'
)
async def read_root():
    return {'Hello': 'FastAPI'}
