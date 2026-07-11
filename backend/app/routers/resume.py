import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.student import Student
from app.models.resume import Resume
from app.utils.file_utils import save_upload_file

router = APIRouter()

def serialize_resume(resume: Resume) -> dict:
    """Helper to serialize Resume record into camelCase and snake_case properties."""
    skills_list = []
    if resume.key_skills_json:
        try:
            skills_list = json.loads(resume.key_skills_json)
        except Exception:
            pass

    return {
        "id": resume.id,
        "resume_title": resume.resume_title,
        "resumeTitle": resume.resume_title,
        "preferred_role": resume.preferred_role or "",
        "preferredRole": resume.preferred_role or "",
        "career_objective": resume.career_objective or "",
        "careerObjective": resume.career_objective or "",
        "key_skills": skills_list,
        "keySkills": skills_list,
        "github_url": resume.github_url or "",
        "githubUrl": resume.github_url or "",
        "linkedin_url": resume.linkedin_url or "",
        "linkedinUrl": resume.linkedin_url or "",
        "portfolio_url": resume.portfolio_url or "",
        "portfolioUrl": resume.portfolio_url or "",
        "file_name": resume.file_name or "",
        "fileName": resume.file_name or "",
        "file_url": resume.file_path or "",
        "fileUrl": resume.file_path or "",
        "use_in_portfolio": resume.use_in_portfolio,
        "useInPortfolio": resume.use_in_portfolio
    }

@router.get("/{register_no}/resume")
async def get_student_resume(register_no: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieves student's active resume details."""
    student = db.query(Student).filter(Student.register_no == register_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
        
    resume = db.query(Resume).filter(Resume.student_id == student.id).first()
    if not resume:
        # Return an empty template dictionary instead of failing
        return {
            "id": 0,
            "resume_title": "",
            "resumeTitle": "",
            "preferred_role": "",
            "preferredRole": "",
            "career_objective": "",
            "careerObjective": "",
            "key_skills": [],
            "keySkills": [],
            "github_url": "",
            "githubUrl": "",
            "linkedin_url": "",
            "linkedinUrl": "",
            "portfolio_url": "",
            "portfolioUrl": "",
            "file_name": "",
            "fileName": "",
            "file_url": "",
            "fileUrl": "",
            "use_in_portfolio": False,
            "useInPortfolio": False
        }
        
    return serialize_resume(resume)

@router.post("/{register_no}/resume")
@router.put("/{register_no}/resume")
async def save_or_update_student_resume(
    register_no: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Saves or updates a student's resume. Supports file upload and metadata changes."""
    student = db.query(Student).filter(Student.register_no == register_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    if current_user.role == "student" and student.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied. Can only save own resume.")

    resume = db.query(Resume).filter(Resume.student_id == student.id).first()
    if not resume:
        resume = Resume(student_id=student.id, resume_title="Default Title")
        db.add(resume)
        db.flush()

    content_type = request.headers.get("content-type", "")

    # 1. Parse fields
    if "multipart/form-data" in content_type:
        form = await request.form()
        if "resume_title" in form:
            resume.resume_title = form.get("resume_title")
        if "preferred_role" in form:
            resume.preferred_role = form.get("preferred_role")
        if "career_objective" in form:
            resume.career_objective = form.get("career_objective")
            
        skills_raw = form.get("key_skills") or form.get("keySkills")
        if skills_raw:
            try:
                skills_list = json.loads(skills_raw)
                resume.key_skills_json = json.dumps(skills_list)
            except Exception:
                resume.key_skills_json = json.dumps([s.strip() for s in skills_raw.split(",") if s.strip()])
                
        if "github_url" in form:
            resume.github_url = form.get("github_url")
        if "linkedin_url" in form:
            resume.linkedin_url = form.get("linkedin_url")
        if "portfolio_url" in form:
            resume.portfolio_url = form.get("portfolio_url")
        if "use_in_portfolio" in form:
            resume.use_in_portfolio = str(form.get("use_in_portfolio")).lower() in ("true", "1")

        file_obj = form.get("file")
        print("FILE_OBJ:", file_obj, "TYPE:", type(file_obj))
        if file_obj and (isinstance(file_obj, UploadFile) or hasattr(file_obj, "filename")):
            if hasattr(file_obj, "file") and not isinstance(file_obj, UploadFile):
                from fastapi import UploadFile as FastAPIUploadFile
                file_obj = FastAPIUploadFile(file=file_obj.file, filename=file_obj.filename, headers=file_obj.headers)
            file_url = await save_upload_file(file_obj, "resumes")
            resume.file_name = file_obj.filename
            resume.file_path = file_url

    else:
        # JSON body
        body = await request.json()
        if "resume_title" in body:
            resume.resume_title = body.get("resume_title")
        if "preferred_role" in body:
            resume.preferred_role = body.get("preferred_role")
        if "career_objective" in body:
            resume.career_objective = body.get("career_objective")
            
        skills_raw = body.get("key_skills") or body.get("keySkills")
        if isinstance(skills_raw, list):
            resume.key_skills_json = json.dumps(skills_raw)
            
        if "github_url" in body:
            resume.github_url = body.get("github_url")
        if "linkedin_url" in body:
            resume.linkedin_url = body.get("linkedin_url")
        if "portfolio_url" in body:
            resume.portfolio_url = body.get("portfolio_url")
        if "use_in_portfolio" in body:
            resume.use_in_portfolio = bool(body.get("use_in_portfolio"))
        if "file_url" in body:
            resume.file_path = body.get("file_url")
        if "file_name" in body:
            resume.file_name = body.get("file_name")

    db.commit()
    db.refresh(resume)

    return serialize_resume(resume)
