from fastapi import APIRouter, HTTPException, Path, File, UploadFile
from starlette.responses import StreamingResponse
from typing import List

from app.api import crud_regions, crud_files
from app.api.models import RegionDB, RegionSchema, UploadFileResponse

router = APIRouter()


# Add region in table
@router.post("/", response_model=RegionDB)
#async def create_region(payload: RegionSchema):
async def create_region(title: str, image: UploadFile = File(...)):
    region = await crud_regions.get_by_name(title)
    if not region:
        region_id = await crud_regions.post(title)
        await crud_files.upload_file(image, region_id)
        response_object = {
            "id": region_id,
            "title": title,
        }
        return response_object
    else:
        raise HTTPException(status_code=400, detail="Region already exists")


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


# Get region image by id
@router.get("/images/{id}/", response_class=StreamingResponse)
async def get_region_image_by_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return await crud_files.download_file(id)


# Get region image by name
@router.get("/images/named/{title}/", response_class=StreamingResponse)
async def get_region_image_by_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    id = list(region.values())[0]
    return await crud_files.download_file(id)


# Get all regions from table
@router.get("/all/_/", response_model=List[RegionDB])
async def get_all_regions():
    return await crud_regions.get_all()


# Get all region's images
@router.get("/images/all/_/", response_model=List[UploadFileResponse])
async def get_all_regions_images():
    return await crud_files.get_list_files()


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

    id = list(region.values())[0]
    region_id = await crud_regions.put_by_id(id, payload)
    response_object = {
        "id": region_id,
        "title": payload.title,
    }
    return response_object


# Update region image by id
@router.put("/images/{id}/")
async def update_region_image_by_id(id: int = Path(..., gt=0), image: UploadFile = File(...)):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    return await crud_files.update_file(id, image)


# Update region image by name
@router.put("/images/named/{title}/")
async def update_region_image_by_name(title: str, image: UploadFile = File(...)):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    id = list(region.values())[0]
    return await crud_files.update_file(id, image)


# Delete region by id
@router.delete("/{id}/", response_model=RegionDB)
async def delete_region_by_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    await crud_regions.delete_by_id(id)
    await crud_files.remove_file(id)
    return region


# Delete region by name
@router.delete("/named/{title}/", response_model=RegionDB)
async def delete_region_by_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    id = list(region.values())[0]
    await crud_regions.delete_by_id(id)
    await crud_files.remove_file(id)
    return region
