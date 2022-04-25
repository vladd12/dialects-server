from fastapi import APIRouter, HTTPException, Path
from typing import List

from app.api import crud_regions
from app.api.models import RegionDB, RegionSchema

router = APIRouter()


# Add region in table
@router.post("/", response_model=RegionDB, status_code=201)
async def create_region(payload: RegionSchema):
    region_id = await crud_regions.post(payload)
    response_object = {
        "id": region_id,
        "title": payload.title,
    }
    return response_object


# Get region by id
@router.get("/{id}/", response_model=RegionDB)
async def get_region_by_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


# Get region by name
@router.get("/named/{title}/", response_model=RegionDB)
async def get_region_by_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


# Get all regions from table
@router.get("/", response_model=List[RegionDB])
async def get_all_regions():
    return await crud_regions.get_all()


# Update region by id
@router.put("/{id}/", response_model=RegionDB)
async def update_region_by_id(payload: RegionSchema, id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_id = await crud_regions.put_by_id(id, payload)
    response_object = {
        "id": region_id,
        "title": payload.title,
    }
    return response_object


# Update region by name
@router.put("/named/{title}/", response_model=RegionDB)
async def update_region_by_name(payload: RegionSchema, title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_id = await crud_regions.put_by_name(title, payload)
    response_object = {
        "id": region_id,
        "title": payload.title,
    }
    return response_object


# Delete region by id
@router.delete("/{id}/", response_model=RegionDB)
async def delete_region_by_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    await crud_regions.delete_by_id(id)
    return region


# Delete region by name
@router.delete("/named/{title}/", response_model=RegionDB)
async def delete_region_by_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    await crud_regions.delete_by_name(title)
    return region
