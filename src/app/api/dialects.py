from fastapi import APIRouter, HTTPException, Path
from typing import List

from app.api import crud_dialects, crud_regions
from app.api.models import DialectDB, DialectSchema, RelationshipDB

router = APIRouter()


# Add dialect in table by region id
@router.post("/{id}/", response_model=DialectDB, status_code=201)
async def create_dialect_by_id(payload: DialectSchema, id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    dialect_id = 0
    dialect = await crud_dialects.get_by_name(payload.title)
    if not dialect:
        dialect_id = await crud_dialects.post_dialect(payload)
    else:
        if list(dialect.values())[2] != payload.description:
            dialect_id = await crud_dialects.post_dialect(payload)
        else:
            dialect_id = list(dialect.values())[0]
    
    region_id = list(region.values())[0]
    relationship = await crud_dialects.get_relationship(region_id, dialect_id)
    if not relationship:
        await crud_dialects.post_relationship(region_id, dialect_id)
    else:
        raise HTTPException(status_code=404, detail="Already exist")
    
    response_object = {
        "id": dialect_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


# Add dialect in table by region name
@router.post("/named/{title}/", response_model=DialectDB, status_code=201)
async def create_dialect_by_name(payload: DialectSchema, title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    dialect_id = 0
    dialect = await crud_dialects.get_by_name(payload.title)
    if not dialect:
        dialect_id = await crud_dialects.post_dialect(payload)
    else:
        if list(dialect.values())[2] != payload.description:
            dialect_id = await crud_dialects.post_dialect(payload)
        else:
            dialect_id = list(dialect.values())[0]
    
    region_id = list(region.values())[0]
    relationship = await crud_dialects.get_relationship(region_id, dialect_id)
    if not relationship:
        await crud_dialects.post_relationship(region_id, dialect_id)
    else:
        raise HTTPException(status_code=404, detail="Already exist")
    
    response_object = {
        "id": dialect_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


# Get dialect by id
@router.get("/{id}/", response_model=DialectDB)
async def get_dialect_by_id(id: int = Path(..., gt=0),):
    dialect = await crud_dialects.get_by_id(id)
    if not dialect:
        raise HTTPException(status_code=404, detail="Note not found")
    return dialect


# Get dialect by name
@router.get("/named/{title}/", response_model=DialectDB)
async def get_dialect_by_name(title: str):
    dialect = await crud_dialects.get_by_name(title)
    if not dialect:
        raise HTTPException(status_code=404, detail="Note not found")
    return dialect


# Get all dialects from table
@router.get("/d/all/", response_model=List[DialectDB])
async def get_all_dialects():
    return await crud_dialects.get_all_dialects()


# Get all relationships from table
@router.get("/r/all/", response_model=List[RelationshipDB])
async def get_all_relationships():
    return await crud_dialects.get_all_relationships()
