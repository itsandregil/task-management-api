from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router
from app.core.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Task Management API",
    description="A REST API for managing personal projects and tasks.",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
