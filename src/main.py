from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database_session_manager import sessionmanager
from db.utils import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    yield
    if await sessionmanager.is_initialised():
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return "HELLO WORLD"
