from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ProfileOut(BaseModel):
    id: UUID
    name: str
    gender: str
    gender_probability: float
    age: int
    age_group: str
    country_id: str
    country_name: str
    country_probability: float
    created_at: datetime

    class Config:
        from_attributes = True

class ProfileListResponse(BaseModel):
    status: str
    page: int
    limit: int
    total: int
    data: list[ProfileOut]

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str