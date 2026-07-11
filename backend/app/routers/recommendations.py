from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.recommendation_service import get_student_recommendations

router = APIRouter()

@router.get("")
async def get_recommendations_alias(
    domain: str = Query("DSA"),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    """Retrieves ranked recommended students in the selected domain or overall."""
    return get_student_recommendations(db, domain, limit)

@router.get("/top")
async def get_top_recommendations(
    domain: str = Query("DSA"),
    limit: int = Query(5),
    db: Session = Depends(get_db)
):
    """Retrieves top 5 recommended students in the selected domain or overall."""
    return get_student_recommendations(db, domain, limit)
