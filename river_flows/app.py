from contextlib import asynccontextmanager

from fastapi import FastAPI

from river_flows.utils.db import initialize_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {
        'result': 'GOOD'
    }
