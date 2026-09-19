from contextlib import asynccontextmanager
from fastapi import FastAPI
from repository import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    init_db()
    yield
    # Runs on shutdown (if needed)


app = FastAPI(lifespan=lifespan)