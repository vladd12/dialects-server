from fastapi import FastAPI

from app.api import regions, dialects, files
from app.db import engine, database, metadata

metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(regions.router, prefix="/regions", tags=["regions"])
app.include_router(dialects.router, prefix="/dialects", tags=["dialects"])
app.include_router(files.router, prefix="/files", tags=["files"])
