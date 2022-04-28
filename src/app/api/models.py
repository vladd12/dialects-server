from pydantic import BaseModel, Field


# User view for region
class RegionSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=70)


# Stored region in db
class RegionDB(RegionSchema):
    id: int


# User view for dialect
class DialectSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=5, max_length=200)


# Stored dialect in db
class DialectDB(DialectSchema):
    id: int


# Stored relationship in db
class RelationshipDB(BaseModel):
    region_id: int
    dialect_id: int


# User view for uploaded file
class UploadFileResponse(BaseModel):
    bucket_name: str
    file_name: str
