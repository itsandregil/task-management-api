from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .core.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Task Management API",
    description="A REST API for managing personal projects and tasks.",
    lifespan=lifespan,
)


@app.get("/")
def redirect_root_to_docs():
    return RedirectResponse("/docs/")
