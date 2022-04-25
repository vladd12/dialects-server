from fastapi import APIRouter, HTTPException, Path
from typing import List

from app.api import crud_dialects
from app.api.models import DialectDB, DialectSchema

router = APIRouter()


# Add dialect in table
@router.post("/", response_model=RegionDB, status_code=201)
async def create_dialect(payload: RegionSchema):
    dialect_id = await crud_dialects.post(payload)
    response_object = {
        "id": region_id,
        "title": payload.title,
    }
    return response_object


# Get dialect by id
@router.get("/{id}/", response_model=RegionDB)
async def get_dialect_by_id(id: int = Path(..., gt=0),):
    dialect = await crud_dialects.get_by_id(id)
    if not dialect:
        raise HTTPException(status_code=404, detail="Note not found")
    return dialect


# Get dialect by name
@router.get("/named/{title}/", response_model=RegionDB)
async def get_dialect_by_name(title: str):
    dialect = await crud_dialects.get_by_name(title)
    if not dialect:
        raise HTTPException(status_code=404, detail="Note not found")
    return dialect
