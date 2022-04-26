from fastapi import HTTPException
from starlette.responses import StreamingResponse
from io import BytesIO

from app.api.minio_handler import MinioHandler

# Base method for uploading files
async def upload_file(file, id):
    file_name = str(id)
    minio_client = MinioHandler().get_instance()
    if minio_client.check_file_exists(file_name=file_name):
        raise HTTPException(status_code=400, detail="File already exists")
    
    try:
        print(file_name)
        data_file = minio_client.put_object(
            file_name=file_name,
            file_data=BytesIO(file.file.read()),
            content_type=file.content_type
        )
        return data_file
    except Exception as e:
        raise HTTPException(status_code=400, detail="Can't connect to Minio")


# Base method for downloading files
async def download_file(id: int):
    file_name = str(id)
    minio_client = MinioHandler().get_instance()
    try:
        if not minio_client.check_file_exists(file_name):
            raise HTTPException(status_code=404, detail="File not found")

        file = minio_client.get_object(file_name)
        return StreamingResponse(BytesIO(file))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Can't connect to Minio")


