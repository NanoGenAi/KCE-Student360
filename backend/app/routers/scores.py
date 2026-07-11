from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, RoleRequired
from app.models.user import User
from app.models.student import MentorAssignment
from app.schemas.score import UploadScoresResponse
from app.services.upload_service import process_scores_excel

router = APIRouter()

@router.post("/upload", response_model=UploadScoresResponse)
async def upload_scores(
    file: UploadFile = File(...),
    current_user: User = Depends(RoleRequired(["faculty", "admin", "mentor"])),
    db: Session = Depends(get_db)
):
    """
    Uploads an Excel file containing student assessment scores.
    Validates data, inserts scores, and recalculates analytics.
    """
    allowed_student_ids = None
    if current_user.role == "mentor":
        assignments = db.query(MentorAssignment).filter(MentorAssignment.mentor_id == current_user.id).all()
        allowed_student_ids = [a.student_id for a in assignments]

    file_bytes = await file.read()
    report = process_scores_excel(db, file_bytes, current_user.id, allowed_student_ids)
    return report

from app.models.score import AssessmentScore

@router.get("/count")
async def get_scores_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the total count of assessment scores in the system."""
    count = db.query(AssessmentScore).count()
    return {"count": count}
