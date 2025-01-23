import traceback
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from db.database_session_manager import get_async_db_session
from importer.importer import tenderize_and_save
from models.tender import Tender, get_tenders

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("main_page.html")

tender_router = APIRouter(
    prefix="/tenders", tags=["tenders"], dependencies=[Depends(get_async_db_session)]
)


@tender_router.get("/", response_model=list[Tender])
async def get_all():
    try:
        response = HTMLResponse(template.render(tenders=await get_tenders()))
    except Exception as e:
        print(e)
        return HTMLResponse("<div>ERROR</div>")
    return response


@tender_router.post("/imports", response_model=list[Tender])
async def import_tenders():
    try:
        return await tenderize_and_save()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return {"message": "Something went wrong. Please try again later."}
