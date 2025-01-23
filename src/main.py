import asyncio
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from db.database_session_manager import sessionmanager
from db.utils import run_migrations
from exceptions.base_exception import FutuTenderBaseException
from exceptions.database_exception import FutuTenderDatabaseException
from importer.importer import tenderize_and_save
from routers.tenders import tender_router

background_tasks = {}


async def recurring_import():
    while True:
        try:
            async with sessionmanager.session():
                await tenderize_and_save()
                await asyncio.sleep(3600)
        except Exception as e:
            print(e)
            print(traceback.format_exc())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    background_tasks["import"] = asyncio.create_task(recurring_import())
    yield
    if await sessionmanager.is_initialised():
        await sessionmanager.close()
    background_tasks.get("import").cancel()


app = FastAPI(lifespan=lifespan)
app.include_router(tender_router)


@app.get("/")
async def root():
    return "HELLO WORLD"


@app.exception_handler(FutuTenderBaseException)
async def handle_base_exception(request, exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unknown exception occurred. Please contact the developers"
        },
    )


@app.exception_handler(FutuTenderDatabaseException)
async def handle_db_exception(request, exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong. Please contact the developers"},
    )
