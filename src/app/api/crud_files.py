from fastapi import HTTPException, UploadFile
from starlette.responses import StreamingResponse

from app.api.minio_handler import MinioHandler
from app.api.models import UploadFileResponse

# Base method for uploading files
async def upload_file(file: UploadFile, id: int):
    file_name = str(id)
    minio_client = MinioHandler().get_instance()
    if minio_client.check_file_exists(file_name):
        raise HTTPException(status_code=400, detail="File already exists")
    
    try:
        data_file = minio_client.put_file(file_name, file)
        return data_file
    except Exception as e:
        raise HTTPException(status_code=400, detail="Can't connect to Minio")


# Base method for downloading files
async def download_file(id: int):
    file_name = str(id)
    minio_client = MinioHandler().get_instance()
    if not minio_client.check_file_exists(file_name):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        file = minio_client.get_file(file_name)
        return StreamingResponse(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Can't connect to Minio")


# Base method for removing files
async def remove_file(id: int):
    file_name = str(id)
    minio_client = MinioHandler().get_instance()
    if not minio_client.check_file_exists(file_name):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        file = minio_client.remove_file(file_name)
        return id
    except Exception as e:
        raise HTTPException(status_code=400, detail="Can't connect to Minio")


# Base method for updating files
async def update_file(id: int, file: UploadFile):
    file_name = str(id)
    minio_client = MinioHandler().get_instance()
    if not minio_client.check_file_exists(file_name):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        data_file = minio_client.update_file(file_name, file)
        return data_file
    except Exception as e:
        raise HTTPException(status_code=400, detail="Can't connect to Minio")


# Get list about names and buckets of all files
async def get_list_files():
    minio_client = MinioHandler().get_instance()
    list_files = []
    for file in minio_client.get_all_files():
        ufs = UploadFileResponse(bucket_name=file.bucket_name, file_name=file.object_name)
        list_files.append(ufs)
    return list_files
