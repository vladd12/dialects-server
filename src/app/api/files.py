from fastapi import APIRouter, HTTPException, Path, File, UploadFile
from typing import List

from app.api import crud_regions, crud_files
from app.api.models import UploadFileResponse

router = APIRouter()


# Upload file by region id
@router.post("/upload/{id}", response_model=UploadFileResponse)
async def upload_file_by_region_id(file: UploadFile = File(...), id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    return await crud_files.upload_file(file, id)


# Upload file by region name
@router.post("/upload/named/{title}", response_model=UploadFileResponse)
async def upload_file_by_region_name(title: str, file: UploadFile = File(...)):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_id = list(region.values())[0]
    return await crud_files.upload_file(file, region_id)


# Download file by region id
@router.get("/download/{id}")
async def download_file_by_region_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    return await crud_files.download_file(id)


# Download file by region name
@router.get("/download/named/{title}")
async def download_file_by_region_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_id = list(region.values())[0]
    return await crud_files.download_file(region_id)


# Get list of all files info
@router.get("/all/", response_model=List[UploadFileResponse])
async def get_all_files_info():
    return await crud_files.get_list_files()


# Remove file by region id
@router.delete("/{id}")
async def remove_file_by_region_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    return await crud_files.remove_file(id)


# Remove file by region name
@router.delete("/named/{title}")
async def remove_file_by_region_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_id = list(region.values())[0]
    return await crud_files.remove_file(region_id)


# Update file by region id
@router.put("/{id}")
async def update_file_by_region_id(id: int = Path(..., gt=0),):
    region = await crud_regions.get_by_id(id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    return await crud_files.remove_file(id)


# Update file by region name
@router.put("/named/{title}")
async def update_file_by_region_name(title: str):
    region = await crud_regions.get_by_name(title)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_id = list(region.values())[0]
    return await crud_files.remove_file(region_id)
