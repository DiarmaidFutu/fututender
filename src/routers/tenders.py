from fastapi import APIRouter, Depends

from db.database_session_manager import get_async_db_session
from models.tender import Tender, get_tenders

tender_router = APIRouter(
    prefix="/tenders", tags=["tenders"], dependencies=[Depends(get_async_db_session)]
)


@tender_router.get("/", response_model=list[Tender])
async def get_all():
    return await get_tenders()
