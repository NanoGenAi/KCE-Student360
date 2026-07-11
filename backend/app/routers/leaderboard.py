from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.services.leaderboard_service import get_leaderboard_data

router = APIRouter()

@router.get("/overall")
async def get_overall_leaderboard(db: Session = Depends(get_db)):
    """Retrieves overall ranked leaderboard of student performance scores."""
    data = get_leaderboard_data(db, "Overall")
    return data

@router.get("/domain/{domain}")
async def get_domain_leaderboard(domain: str, db: Session = Depends(get_db)):
    """Retrieves domain-specific ranked leaderboard sorted by domain average."""
    data = get_leaderboard_data(db, domain)
    return data
