import random
import os
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


    # Get file from bucket
    def presigned_get_file(self, file_name: str):
        # Request URL expired after one day
        url = self.client.presigned_get_file(
            bucket_name=self.bucket_name,
            object_name=file_name,
            expires=timedelta(days=1)
        )
        return url


    # Checking if file exists in bucket
    def check_file_exists(self, file_name):
        try:
            self.client.stat_object(bucket_name=self.bucket_name, object_name=file_name)
            return True
        except Exception as e:
            return False


    # Put file in bucket
    def put_object(self, file_data, file_name, content_type):
        result = self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=file_name,
            data=file_data,
            content_type=content_type,
            length=-1,
            part_size=10 * 1024 * 1024
        )
        
        url = self.presigned_get_file(file_name)
        data_file = {
            'bucket_name': self.bucket_name,
            'file_name': file_name,
            'url': url
        }
        return data_file

    #
    def get_object(self, file_name):
        result = self.client.get_object(bucket_name=self.bucket_name, object_name=file_name)
        return result.read()
