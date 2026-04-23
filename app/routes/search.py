from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app.models import Profile
from app.schemas import ProfileListResponse
from app.nlp_parser import parse_nl_query

router = APIRouter()

@router.get("/profiles/search", response_model=ProfileListResponse)
def search_profiles(
    q: str = Query(..., min_length=1),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    filters = parse_nl_query(q)

    if filters is None:
        raise HTTPException(
            status_code=400,
            detail="Unable to interpret query"
        )

    query = db.query(Profile)

    if "gender" in filters:
        query = query.filter(Profile.gender == filters["gender"])
    if "age_group" in filters:
        query = query.filter(Profile.age_group == filters["age_group"])
    if "country_id" in filters:
        query = query.filter(Profile.country_id == filters["country_id"])
    if "min_age" in filters:
        query = query.filter(Profile.age >= filters["min_age"])
    if "max_age" in filters:
        query = query.filter(Profile.age <= filters["max_age"])

    total = query.count()
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": results,
    }