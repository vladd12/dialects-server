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
async def post_dialect(payload: DialectSchema):
    query = dialects.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)


# Add relationship in table
async def post_relationship(id_region: int, id_dialect: int):
    query = relationships.insert().values(region_id=id_region, dialect_id=id_dialect)
    return await database.execute(query=query)


# Get relationship by IDs
async def get_relationship(id_region: int, id_dialect: int):
    query = relationships.select().where(id_region == dialects.c.region_id and id_dialect == dialects.c.dialect_id)
    return await database.fetch_one(query=query)


# Get all dialects from table
async def get_all_dialects():
    query = dialects.select()
    return await database.fetch_all(query=query)


# Get all relationships from table
async def get_all_relationships():
    query = relationships.select()
    return await database.fetch_all(query=query)
