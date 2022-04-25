from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int


class RegionSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=70)


class RegionDB(RegionSchema):
    id: int


class DialectSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10, max_length=200)


class DialectDB(DialectSchema):
    id: int
