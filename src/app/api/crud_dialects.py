from app.api.models import DialectSchema
from app.db import dialects, relationships, database


# Get dialect by id
async def get_by_id(id: int):
    query = dialects.select().where(id == dialects.c.id)
    return await database.fetch_one(query=query)


# Get dialect by name
async def get_by_name(title: str):
    query = dialects.select().where(title == dialects.c.title)
    return await database.fetch_one(query=query)


# Add dialect in table
async def post(payload: DialectSchema):
    query = dialects.insert().values(title=payload.title, description = payload.description)
    return await database.execute(query=query)


