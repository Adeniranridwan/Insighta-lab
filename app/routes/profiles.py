from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app.models import Profile
from app.schemas import ProfileListResponse, ProfileOut

router = APIRouter()

SORT_FIELDS = {
    "age": Profile.age,
    "created_at": Profile.created_at,
    "gender_probability": Profile.gender_probability,
}

@router.get("/profiles", response_model=ProfileListResponse)
def get_profiles(
    gender: str | None = None,
    age_group: str | None = None,
    country_id: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
    min_gender_probability: float | None = None,
    min_country_probability: float | None = None,
    sort_by: str = "created_at",
    order: str = "asc",
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    if sort_by not in SORT_FIELDS:
        raise HTTPException(status_code=422, detail="Invalid query parameters")
    if order not in ("asc", "desc"):
        raise HTTPException(status_code=422, detail="Invalid query parameters")

    query = db.query(Profile)

    # Apply filters
    if gender:
        query = query.filter(Profile.gender == gender)
    if age_group:
        query = query.filter(Profile.age_group == age_group)
    if country_id:
        query = query.filter(Profile.country_id == country_id.upper())
    if min_age is not None:
        query = query.filter(Profile.age >= min_age)
    if max_age is not None:
        query = query.filter(Profile.age <= max_age)
    if min_gender_probability is not None:
        query = query.filter(Profile.gender_probability >= min_gender_probability)
    if min_country_probability is not None:
        query = query.filter(Profile.country_probability >= min_country_probability)

    # Sorting
    sort_col = SORT_FIELDS[sort_by]
    query = query.order_by(asc(sort_col) if order == "asc" else desc(sort_col))

    total = query.count()

    # Pagination
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": results,
    }