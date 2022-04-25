from app.api.models import RegionSchema
from app.db import regions, database


# Add region in table
async def post(payload: RegionSchema):
    query = regions.insert().values(title=payload.title)
    return await database.execute(query=query)


# Get region by id
async def get_by_id(id: int):
    query = regions.select().where(id == regions.c.id)
    return await database.fetch_one(query=query)


# Get region by name
async def get_by_name(title: str):
    query = regions.select().where(title == regions.c.title)
    return await database.fetch_one(query=query)


# Get all regions from table
async def get_all():
    query = regions.select()
    return await database.fetch_all(query=query)


# Update region by id
async def put(id: int, payload: RegionSchema):
    query = (
        regions.update().where(id == regions.c.id)
        .values(title=payload.title)
        .returning(regions.c.id)
    )
    return await database.execute(query=query)


# Delete region by id
async def delete_by_id(id: int):
    query = regions.delete().where(id == regions.c.id)
    return await database.execute(query=query)


# Delete region by name
async def delete_by_name(title: str):
    query = regions.delete().where(title == regions.c.title)
    return await database.execute(query=query)

