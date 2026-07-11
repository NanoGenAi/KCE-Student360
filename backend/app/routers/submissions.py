import json
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.student import Student
from app.models.submission import StudentProject, StudentCertification, StudentAchievement
from app.utils.file_utils import save_upload_file
from app.utils.response_utils import error_response, success_response

router = APIRouter()

# Helper to serialize date/datetime fields
def serialize_item(item, item_type: str) -> dict:
    d = {}
    for col in item.__table__.columns:
        val = getattr(item, col.name)
        if isinstance(val, (date, datetime)):
            d[col.name] = val.isoformat()
        else:
            d[col.name] = val
            
    # Add camelCase mappings and compatibility fields
    d["studentId"] = item.student_id
    d["student_id"] = item.student_id
    
    # Specific fields mapping
    if item_type == "project":
        # Parse tech_stack list or string
        tech_list = []
        if item.tech_stack:
            try:
                if item.tech_stack.startswith("["):
                    tech_list = json.loads(item.tech_stack)
                else:
                    tech_list = [s.strip() for s in item.tech_stack.split(",") if s.strip()]
            except Exception:
                tech_list = [item.tech_stack]
        d["tech_stack"] = tech_list
        d["techStack"] = tech_list
        d["githubLink"] = item.github_link or ""
        d["github_link"] = item.github_link or ""
        d["liveDemoLink"] = item.live_demo_link or ""
        d["live_demo_link"] = item.live_demo_link or ""
        d["proofFile"] = item.proof_file or ""
        d["proof_file"] = item.proof_file or ""
        
    elif item_type == "certification":
        d["credentialId"] = item.credential_id or ""
        d["credential_id"] = item.credential_id or ""
        d["issueDate"] = item.issue_date.isoformat() if item.issue_date else ""
        d["issue_date"] = item.issue_date.isoformat() if item.issue_date else ""
        d["expiryDate"] = item.expiry_date.isoformat() if item.expiry_date else ""
        d["expiry_date"] = item.expiry_date.isoformat() if item.expiry_date else ""
        d["certificateLink"] = item.certificate_link or ""
        d["certificate_link"] = item.certificate_link or ""
        d["proofFile"] = item.proof_file or ""
        d["proof_file"] = item.proof_file or ""
        
    elif item_type == "achievement":
        d["achievementType"] = item.achievement_type
        d["achievement_type"] = item.achievement_type
        d["achievementDate"] = item.achievement_date.isoformat() if item.achievement_date else ""
        d["achievement_date"] = item.achievement_date.isoformat() if item.achievement_date else ""
        d["proofLink"] = item.proof_link or ""
        d["proof_link"] = item.proof_link or ""
        d["proofFile"] = item.proof_file or ""
        d["proof_file"] = item.proof_file or ""

    d["mentorFeedback"] = item.mentor_feedback or ""
    d["mentor_feedback"] = item.mentor_feedback or ""
    return d

@router.post("/projects")
async def submit_project(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Creates a new project submission for the logged-in student."""
    if current_user.role != "student" or not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can submit projects.")
        
    student = current_user.student_profile
    content_type = request.headers.get("content-type", "")
    
    # 1. Parse fields based on Request Content-Type
    title = ""
    description = ""
    tech_stack = ""
    role = ""
    github_link = ""
    live_demo_link = ""
    file_url = None

    if "multipart/form-data" in content_type:
        form = await request.form()
        title = form.get("title", "")
        description = form.get("description", "")
        tech_stack = form.get("tech_stack", "") or form.get("techStack", "")
        role = form.get("role", "")
        github_link = form.get("github_link", "") or form.get("githubLink", "")
        live_demo_link = form.get("live_demo_link", "") or form.get("liveDemoLink", "")
        
        file_obj = form.get("file") or form.get("proof_file") or form.get("proofFile")
        if file_obj and isinstance(file_obj, UploadFile):
            file_url = await save_upload_file(file_obj, "projects")
    else:
        # JSON body
        body = await request.json()
        title = body.get("title", "")
        description = body.get("description", "")
        tech_stack_raw = body.get("tech_stack") or body.get("techStack", "")
        if isinstance(tech_stack_raw, list):
            tech_stack = json.dumps(tech_stack_raw)
        else:
            tech_stack = str(tech_stack_raw)
        role = body.get("role", "")
        github_link = body.get("github_link") or body.get("githubLink", "")
        live_demo_link = body.get("live_demo_link") or body.get("liveDemoLink", "")
        file_url = body.get("proof_file") or body.get("proofFile")

    if not title or not description:
        raise HTTPException(status_code=400, detail="Title and description are required fields.")

    # 2. Save project record
    project = StudentProject(
        student_id=student.id,
        title=title,
        description=description,
        tech_stack=tech_stack,
        role=role,
        github_link=github_link,
        live_demo_link=live_demo_link,
        proof_file=file_url,
        status="Pending"
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return serialize_item(project, "project")

@router.get("/projects/me")
async def get_my_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves all project submissions for the current logged-in student."""
    if current_user.role != "student" or not current_user.student_profile:
        return []
    student = current_user.student_profile
    projects = db.query(StudentProject).filter(StudentProject.student_id == student.id).all()
    return [serialize_item(p, "project") for p in projects]

@router.post("/certifications")
async def submit_certification(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Creates a new certification submission for the logged-in student."""
    if current_user.role != "student" or not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can submit certifications.")
        
    student = current_user.student_profile
    content_type = request.headers.get("content-type", "")
    
    title = ""
    issuer = ""
    credential_id = ""
    issue_date_str = ""
    expiry_date_str = ""
    certificate_link = ""
    file_url = None

    if "multipart/form-data" in content_type:
        form = await request.form()
        title = form.get("title", "")
        issuer = form.get("issuer", "")
        credential_id = form.get("credential_id", "") or form.get("credentialId", "")
        issue_date_str = form.get("issue_date", "") or form.get("issueDate", "")
        expiry_date_str = form.get("expiry_date", "") or form.get("expiryDate", "")
        certificate_link = form.get("certificate_link", "") or form.get("certificateLink", "")
        
        file_obj = form.get("file") or form.get("proof_file") or form.get("proofFile")
        if file_obj and isinstance(file_obj, UploadFile):
            file_url = await save_upload_file(file_obj, "certificates")
    else:
        body = await request.json()
        title = body.get("title", "")
        issuer = body.get("issuer", "")
        credential_id = body.get("credential_id") or body.get("credentialId", "")
        issue_date_str = body.get("issue_date") or body.get("issueDate", "")
        expiry_date_str = body.get("expiry_date") or body.get("expiryDate", "")
        certificate_link = body.get("certificate_link") or body.get("certificateLink", "")
        file_url = body.get("proof_file") or body.get("proofFile")

    if not title or not issuer or not issue_date_str:
        raise HTTPException(status_code=400, detail="Title, issuer, and issue date are required fields.")

    # Parse dates safely
    def parse_date(d_str):
        if not d_str:
            return None
        # Try different formats
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(d_str.split("T")[0], fmt).date()
            except ValueError:
                continue
        return None

    issue_date = parse_date(issue_date_str)
    if not issue_date:
        raise HTTPException(status_code=400, detail=f"Invalid issue_date format: '{issue_date_str}'")
        
    expiry_date = parse_date(expiry_date_str)

    cert = StudentCertification(
        student_id=student.id,
        title=title,
        issuer=issuer,
        credential_id=credential_id,
        issue_date=issue_date,
        expiry_date=expiry_date,
        certificate_link=certificate_link,
        proof_file=file_url,
        status="Pending"
    )
    
    db.add(cert)
    db.commit()
    db.refresh(cert)
    
    return serialize_item(cert, "certification")

@router.get("/certifications/me")
async def get_my_certifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves all certification submissions for the current student."""
    if current_user.role != "student" or not current_user.student_profile:
        return []
    student = current_user.student_profile
    certs = db.query(StudentCertification).filter(StudentCertification.student_id == student.id).all()
    return [serialize_item(c, "certification") for c in certs]

@router.post("/achievements")
async def submit_achievement(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Creates a new achievement submission for the logged-in student."""
    if current_user.role != "student" or not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Only students can submit achievements.")
        
    student = current_user.student_profile
    content_type = request.headers.get("content-type", "")
    
    title = ""
    achievement_type = ""
    organization = ""
    description = ""
    achievement_date_str = ""
    proof_link = ""
    file_url = None

    if "multipart/form-data" in content_type:
        form = await request.form()
        title = form.get("title", "")
        achievement_type = form.get("achievement_type", "") or form.get("achievementType", "")
        organization = form.get("organization", "")
        description = form.get("description", "")
        achievement_date_str = form.get("achievement_date", "") or form.get("achievementDate", "")
        proof_link = form.get("proof_link", "") or form.get("proofLink", "")
        
        file_obj = form.get("file") or form.get("proof_file") or form.get("proofFile")
        if file_obj and isinstance(file_obj, UploadFile):
            file_url = await save_upload_file(file_obj, "achievements")
    else:
        body = await request.json()
        title = body.get("title", "")
        achievement_type = body.get("achievement_type") or body.get("achievementType", "")
        organization = body.get("organization", "")
        description = body.get("description", "")
        achievement_date_str = body.get("achievement_date") or body.get("achievementDate", "")
        proof_link = body.get("proof_link") or body.get("proofLink", "")
        file_url = body.get("proof_file") or body.get("proofFile")

    if not title or not achievement_type or not organization or not achievement_date_str:
        raise HTTPException(status_code=400, detail="Title, type, organization, and date are required fields.")

    # Parse dates safely
    def parse_date(d_str):
        if not d_str:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(d_str.split("T")[0], fmt).date()
            except ValueError:
                continue
        return None

    achievement_date = parse_date(achievement_date_str)
    if not achievement_date:
        raise HTTPException(status_code=400, detail=f"Invalid achievement_date format: '{achievement_date_str}'")

    ach = StudentAchievement(
        student_id=student.id,
        title=title,
        achievement_type=achievement_type,
        organization=organization,
        description=description,
        achievement_date=achievement_date,
        proof_link=proof_link,
        proof_file=file_url,
        status="Pending"
    )
    
    db.add(ach)
    db.commit()
    db.refresh(ach)
    
    return serialize_item(ach, "achievement")

@router.get("/achievements/me")
async def get_my_achievements(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves all achievement submissions for the current student."""
    if current_user.role != "student" or not current_user.student_profile:
        return []
    student = current_user.student_profile
    achs = db.query(StudentAchievement).filter(StudentAchievement.student_id == student.id).all()
    return [serialize_item(a, "achievement") for a in achs]
