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
        raise HTTPException(status_code=404, detail="Dialect not found")
    return dialect


# Get dialect by name
@router.get("/named/{title}/", response_model=DialectDB)
async def get_dialect_by_name(title: str):
    dialect = await crud_dialects.get_by_name(title)
    if not dialect:
        raise HTTPException(status_code=404, detail="Dialect not found")
    return dialect


# Get all dialects from table
@router.get("/d/all/", response_model=List[DialectDB])
async def get_all_dialects():
    return await crud_dialects.get_all_dialects()


# Get all relationships from table
@router.get("/r/all/", response_model=List[RelationshipDB])
async def get_all_relationships():
    return await crud_dialects.get_all_relationships()


# Get all dialects by region id
@router.get("/d/all/region-id/{id}", response_model=List[DialectDB])
async def get_all_dialects_by_region_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    relationships = await crud_dialects.get_all_relationships_by_region_id(id)
    dialects = []
    for relationship in relationships:
        dialect_id = list(relationship.values())[1]
        dialect = await crud_dialects.get_by_id(dialect_id)
        if not dialect:
            raise HTTPException(status_code=404, detail="Dialect not found")
        dialects.append(dialect)
    
    return dialects


# Get all dialects by region name
@router.get("/d/all/region-name/{title}", response_model=List[DialectDB])
async def get_all_dialects_by_region_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    id = list(region.values())[0]
    relationships = await crud_dialects.get_all_relationships_by_region_id(id)
    dialects = []
    for relationship in relationships:
        dialect_id = list(relationship.values())[1]
        dialect = await crud_dialects.get_by_id(dialect_id)
        if not dialect:
            raise HTTPException(status_code=404, detail="Dialect not found")
        dialects.append(dialect)
    
    return dialects


# Update dialect by id
@router.put("/{id}/", response_model=DialectDB)
async def update_dialect_by_id(payload: DialectSchema, id: int = Path(..., gt=0),):
    dialect = await crud_dialects.get_by_id(id)
    if not dialect:
        raise HTTPException(status_code=404, detail="Dialect not found")

    dialect_id = await crud_dialects.put_by_id(id, payload)
    response_object = {
        "id": dialect_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


# Update dialect by name
@router.put("/named/{title}/", response_model=DialectDB)
async def update_dialect_by_name(payload: DialectSchema, title: str):
    dialect = await crud_dialects.get_by_name(title)
    if not dialect:
        raise HTTPException(status_code=404, detail="Dialect not found")

    dialect_id = await crud_dialects.put_by_name(title, payload)
    response_object = {
        "id": dialect_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


# Delete dialect by id
@router.delete("/{id}/", response_model=DialectDB)
async def delete_dialect_by_id(id: int = Path(..., gt=0),):
    dialect = await crud_dialects.get_by_id(id)
    if not dialect:
        raise HTTPException(status_code=404, detail="Dialect not found")

    await crud_dialects.delete_by_id(id)
    return dialect


# Delete dialect by name
@router.delete("/named/{title}/", response_model=DialectDB)
async def delete_dialect_by_name(title: str):
    dialect = await crud_dialects.get_by_name(title)
    if not dialect:
        raise HTTPException(status_code=404, detail="Dialect not found")

    await crud_dialects.delete_by_name(title)
    return dialect
