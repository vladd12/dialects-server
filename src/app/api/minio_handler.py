import random
import os
from io import BytesIO
from datetime import timedelta
from fastapi import HTTPException
from minio import Minio


# Handle for Minio
class MinioHandler():
    __instance = None


    # Singleton method
    @staticmethod
    def get_instance():
        """ Static access method """
        if not MinioHandler.__instance:
            MinioHandler.__instance = MinioHandler()
        return MinioHandler.__instance


    # Constructor
    def __init__(self):
        self.minio_url = 'storage:9000'
        self.access_key = os.getenv("MINIO_USR")
        self.secret_key = os.getenv("MINIO_PSWD")
        self.bucket_name = os.getenv("MINIO_BUCKET")
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )
        self.make_bucket()


    # Create bucket if doesn't exist
    def make_bucket(self) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return self.bucket_name


    # Checking if file exists in bucket
    def check_file_exists(self, file_name):
        try:
            self.client.stat_object(bucket_name=self.bucket_name, object_name=file_name)
            return True
        except Exception as e:
            return False


    # Put file in bucket
    def put_file(self, file_name, file):
        result = self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=file_name,
            data=BytesIO(file.file.read()),
            content_type=file.content_type,
            length=-1,
            part_size=10 * 1024 * 1024
        )
        
        data_file = {
            'bucket_name': self.bucket_name,
            'file_name': file_name,
        }
        return data_file


    # Returns file from bucket
    def get_file(self, file_name):
        result = self.client.get_object(self.bucket_name, file_name)
        return BytesIO(result.read())


    # Remove file from bucket
    def remove_file(self, file_name):
        self.client.remove_object(self.bucket_name, file_name)


    # Update file in bucket (remove old, put new)
    def update_file(self, file_name, file):
        self.remove_file(file_name)
        self.put_file(file_name, file)
