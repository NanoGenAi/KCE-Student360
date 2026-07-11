from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class ProjectCreate(BaseModel):
    title: str
    description: str
    tech_stack: str  # Can be string or list, handled in parsing
    role: Optional[str] = None
    github_link: Optional[str] = None
    live_demo_link: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    student_id: int
    title: str
    description: str
    tech_stack: str
    role: Optional[str] = None
    github_link: Optional[str] = None
    live_demo_link: Optional[str] = None
    proof_file: Optional[str] = None
    status: str
    mentor_feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CertificationCreate(BaseModel):
    title: str
    issuer: str
    credential_id: Optional[str] = None
    issue_date: date
    expiry_date: Optional[date] = None
    certificate_link: Optional[str] = None

class CertificationResponse(BaseModel):
    id: int
    student_id: int
    title: str
    issuer: str
    credential_id: Optional[str] = None
    issue_date: date
    expiry_date: Optional[date] = None
    certificate_link: Optional[str] = None
    proof_file: Optional[str] = None
    status: str
    mentor_feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AchievementCreate(BaseModel):
    title: str
    achievement_type: str
    organization: str
    description: str
    achievement_date: date
    proof_link: Optional[str] = None

class AchievementResponse(BaseModel):
    id: int
    student_id: int
    title: str
    achievement_type: str
    organization: str
    description: str
    achievement_date: date
    proof_link: Optional[str] = None
    proof_file: Optional[str] = None
    status: str
    mentor_feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class MentorReviewRequest(BaseModel):
    item_type: Optional[str] = None
    itemType: Optional[str] = None
    id: int
    status: str
    feedback: Optional[str] = None

class ApprovalItemResponse(BaseModel):
    id: int
    item_type: str
    itemType: str
    type: str  # Capitalized for frontend: Project, Certification, Achievement
    title: str
    description: str
    student_id: int
    studentId: int
    student_name: str
    studentName: str
    register_no: str
    registerNo: str
    status: str
    created_at: datetime
    submitted_date: str  # Formatted YYYY-MM-DD
    proof_link: Optional[str] = None
    proof_file: Optional[str] = None
    feedback: Optional[str] = None
    mentor_feedback: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
