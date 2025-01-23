import traceback
from fastapi import APIRouter, Depends

from db.database_session_manager import get_async_db_session
from importer.importer import tenderize_and_save
from models.tender import Tender, get_tenders

tender_router = APIRouter(
    prefix="/tenders", tags=["tenders"], dependencies=[Depends(get_async_db_session)]
)


@tender_router.get("/", response_model=list[Tender])
async def get_all():
    return await get_tenders()


@tender_router.post("/imports", response_model=list[Tender])
async def import_tenders():
    try:
        return await tenderize_and_save()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return {"message": "Something went wrong. Please try again later."}
