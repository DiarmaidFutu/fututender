from fastapi import APIRouter

from models.tender import Tender

tender_router = APIRouter()


@tender_router.get("/tenders", response_model=list[Tender])
async def get_tenders():
    return []
