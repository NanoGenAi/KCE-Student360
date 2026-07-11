import json
from datetime import date, datetime
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.profile import StudentAbout, UserProfile
from app.models.resume import Resume
from app.models.score import StudentAnalytics, AssessmentScore
from app.models.submission import StudentProject, StudentCertification, StudentAchievement
from app.models.portfolio import PortfolioCustomization
from app.models.ai_summary import AISummary

DEFAULT_HEADLINE = "AI & DS Student | Java Full Stack Developer | Aspiring AI Engineer"
DEFAULT_ABOUT_ME = (
    "I am Shahul, an Artificial Intelligence and Data Science student at Karpagam College of Engineering. "
    "I am passionate about building useful software solutions that combine AI, full stack development, "
    "and real-world problem solving."
)
DEFAULT_CAREER_OBJ = (
    "To build a strong career as an AI Engineer and Java Full Stack Developer by using my knowledge in "
    "Artificial Intelligence, Data Science, and software development to create innovative, practical, "
    "and impactful solutions."
)
DEFAULT_SKILLS = [
    "AI & Data Science", "Java", "React", "Full Stack Development", 
    "Python", "DSA", "DBMS", "FastAPI", "PostgreSQL"
]

def to_dict(obj):
    if not obj:
        return {}
    d = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        if isinstance(val, (date, datetime)):
            d[col.name] = val.isoformat()
        else:
            d[col.name] = val
    return d

def get_public_portfolio(db: Session, register_no: str) -> dict:
    """
    Aggregates all profile, submissions, performance averages, resume details,
    customization configurations, and AI analytics for a public student portfolio.
    """
    student = db.query(Student).filter(Student.register_no == register_no).first()
    if not student:
        return None

    # Fetch all raw profile records
    analytics_obj = db.query(StudentAnalytics).filter(StudentAnalytics.student_id == student.id).first()
    about_obj = db.query(StudentAbout).filter(StudentAbout.student_id == student.id).first()
    resume_obj = db.query(Resume).filter(Resume.student_id == student.id).first()
    custom_obj = db.query(PortfolioCustomization).filter(PortfolioCustomization.student_id == student.id).first()
    ai_sum_obj = db.query(AISummary).filter(AISummary.student_id == student.id).first()

    # Submissions (Filter out rejected items, include pending clearly marked or approved verified)
    projects = db.query(StudentProject).filter(
        StudentProject.student_id == student.id,
        StudentProject.status != "Rejected"
    ).all()
    
    certifications = db.query(StudentCertification).filter(
        StudentCertification.student_id == student.id,
        StudentCertification.status != "Rejected"
    ).all()

    achievements = db.query(StudentAchievement).filter(
        StudentAchievement.student_id == student.id,
        StudentAchievement.status != "Rejected"
    ).all()

    scores = db.query(AssessmentScore).filter(
        AssessmentScore.student_id == student.id
    ).order_by(AssessmentScore.assessment_date.desc()).all()

    # 1. Resolve profile image priority: Student.profile_image -> UserProfile.profile_image -> None fallback
    profile_image = student.profile_image
    if not profile_image:
        user_prof = db.query(UserProfile).filter(UserProfile.user_id == student.user_id).first()
        if user_prof:
            profile_image = user_prof.profile_image
            
    # 2. Resolve About Me Priority: Customization -> Resume -> StudentAbout -> Default fallback
    headline = None
    about_me = None
    career_objective = None
    skills = None
    github_url = None
    linkedin_url = None

    # Customization Layer (Priority 1)
    if custom_obj:
        if custom_obj.headline:
            headline = custom_obj.headline
        if custom_obj.about_me:
            about_me = custom_obj.about_me
        if custom_obj.career_objective:
            career_objective = custom_obj.career_objective
        if custom_obj.skills_json:
            try:
                skills = json.loads(custom_obj.skills_json)
            except Exception:
                pass
        if custom_obj.github_url:
            github_url = custom_obj.github_url
        if custom_obj.linkedin_url:
            linkedin_url = custom_obj.linkedin_url

    # Resume Layer (Priority 2)
    if resume_obj:
        if not headline and (resume_obj.preferred_role or resume_obj.resume_title):
            headline = resume_obj.preferred_role or resume_obj.resume_title
        if not career_objective and resume_obj.career_objective:
            career_objective = resume_obj.career_objective
        if not about_me and resume_obj.career_objective:
            about_me = resume_obj.career_objective
        if not skills and resume_obj.key_skills_json:
            try:
                skills = json.loads(resume_obj.key_skills_json)
            except Exception:
                pass
        if not github_url and resume_obj.github_url:
            github_url = resume_obj.github_url
        if not linkedin_url and resume_obj.linkedin_url:
            linkedin_url = resume_obj.linkedin_url

    # StudentAbout Layer (Priority 3)
    if about_obj:
        if not headline and about_obj.headline:
            headline = about_obj.headline
        if not about_me and about_obj.about_me:
            about_me = about_obj.about_me
        if not career_objective and about_obj.career_objective:
            career_objective = about_obj.career_objective
        if not skills and about_obj.skills_json:
            try:
                skills = json.loads(about_obj.skills_json)
            except Exception:
                pass

    # Defaults fallback
    if not headline:
        headline = DEFAULT_HEADLINE
    if not about_me:
        about_me = DEFAULT_ABOUT_ME
    if not career_objective:
        career_objective = DEFAULT_CAREER_OBJ
    if not skills:
        skills = DEFAULT_SKILLS
    if not github_url:
        github_url = ""
    if not linkedin_url:
        linkedin_url = ""

    # 3. Format Student section
    student_dict = {
        "id": student.id,
        "register_no": student.register_no,
        "registerNo": student.register_no,
        "name": student.name,
        "email": student.email,
        "phone": student.phone or "",
        "department": student.department,
        "year": student.year,
        "section": student.section,
        "batch": student.batch,
        "cgpa": student.cgpa,
        "profile_image": profile_image or "",
        "profileImage": profile_image or "",
    }

    # 4. Format Resume validation
    resume_dict = None
    # Include resume only if use_in_portfolio is true and not forbidden by customization
    show_resume = True
    if custom_obj and hasattr(custom_obj, "resume_visibility"):
        show_resume = custom_obj.resume_visibility

    if resume_obj:
        resume_skills = []
        if resume_obj.key_skills_json:
            try:
                resume_skills = json.loads(resume_obj.key_skills_json)
            except Exception:
                pass
        resume_dict = {
            "id": resume_obj.id,
            "resume_title": resume_obj.resume_title,
            "resumeTitle": resume_obj.resume_title,
            "title": resume_obj.resume_title,
            "preferred_role": resume_obj.preferred_role or "",
            "preferredRole": resume_obj.preferred_role or "",
            "primary_role": resume_obj.preferred_role or "",
            "primaryRole": resume_obj.preferred_role or "",
            "career_objective": resume_obj.career_objective or "",
            "careerObjective": resume_obj.career_objective or "",
            "key_skills": resume_skills,
            "keySkills": resume_skills,
            "skills_json": resume_obj.key_skills_json,
            "skillsJson": resume_obj.key_skills_json,
            "file_name": resume_obj.file_name or "",
            "fileName": resume_obj.file_name or "",
            "file_url": resume_obj.file_path or "",
            "fileUrl": resume_obj.file_path or "",
            "file_path": resume_obj.file_path or "",
            "filePath": resume_obj.file_path or "",
            "resume_url": resume_obj.file_path or "",
            "resumeUrl": resume_obj.file_path or "",
            "github_url": resume_obj.github_url or "",
            "linkedin_url": resume_obj.linkedin_url or "",
            "portfolio_url": resume_obj.portfolio_url or "",
            "use_in_portfolio": bool(resume_obj.use_in_portfolio and show_resume),
            "useInPortfolio": bool(resume_obj.use_in_portfolio and show_resume),
            "uploaded_at": resume_obj.updated_at.isoformat() if resume_obj.updated_at else "",
            "updated_at": resume_obj.updated_at.isoformat() if resume_obj.updated_at else "",
            "updatedAt": resume_obj.updated_at.isoformat() if resume_obj.updated_at else ""
        }

    # 5. Format Customizations details
    custom_dict = {}
    if custom_obj:
        custom_skills = []
        if custom_obj.skills_json:
            try:
                custom_skills = json.loads(custom_obj.skills_json)
            except Exception:
                pass
                
        custom_visibility = {
            "showProjects": True,
            "showCertifications": True,
            "showAchievements": True,
            "showAcademicHighlights": True,
            "showContactLinks": True,
            "showResume": True
        }
        if custom_obj.section_visibility_json:
            try:
                custom_visibility = json.loads(custom_obj.section_visibility_json)
            except Exception:
                pass

        custom_dict = {
            "headline": custom_obj.headline or "",
            "about_me": custom_obj.about_me or "",
            "aboutMe": custom_obj.about_me or "",
            "career_objective": custom_obj.career_objective or "",
            "careerObjective": custom_obj.career_objective or "",
            "skills": custom_skills,
            "github_url": custom_obj.github_url or "",
            "githubUrl": custom_obj.github_url or "",
            "linkedin_url": custom_obj.linkedin_url or "",
            "linkedinUrl": custom_obj.linkedin_url or "",
            "email": custom_obj.email or "",
            "phone": custom_obj.phone or "",
            "location": custom_obj.location or "",
            "theme": custom_obj.theme or "Dark Minimal",
            "section_visibility_json": custom_visibility,
            "sectionVisibility": custom_visibility,
            "resume_visibility": custom_obj.resume_visibility,
            "resumeVisibility": custom_obj.resume_visibility
        }

    # 6. Format Performance dictionary
    performance_dict = {}
    if analytics_obj:
        domain_scores = {
            "DSA": analytics_obj.dsa_average,
            "DBMS": analytics_obj.dbms_average,
            "FullStack": analytics_obj.fullstack_average,
            "Aptitude": analytics_obj.aptitude_average,
            "Coding": analytics_obj.coding_average,
            "Academic": analytics_obj.academic_average,
            "Technical": analytics_obj.technical_average
        }

        score_history = []
        for sc in scores:
            iso_date = sc.assessment_date.date().isoformat()
            score_history.append({
                "id": sc.id,
                "date": iso_date,
                "assessment_date": iso_date,
                "assessmentDate": iso_date,
                "assessment_name": sc.assessment_name,
                "assessmentName": sc.assessment_name,
                "category": sc.category,
                "score": sc.score,
                "max_marks": sc.max_marks,
                "maxMarks": sc.max_marks,
                "percentage": sc.percentage
            })

        performance_dict = {
            "overall_score": analytics_obj.overall_score,
            "overallScore": analytics_obj.overall_score,
            "domain_scores": domain_scores,
            "domainScores": domain_scores,
            "strongest_domain": analytics_obj.strongest_domain,
            "weakest_domain": analytics_obj.weakest_domain,
            "score_history": score_history,
            "scoreHistory": score_history
        }

    # 7. Format Submissions lists
    serialized_projects = []
    for p in projects:
        pd = to_dict(p)
        tech_list = []
        if p.tech_stack:
            try:
                if p.tech_stack.startswith("["):
                    tech_list = json.loads(p.tech_stack)
                else:
                    tech_list = [s.strip() for s in p.tech_stack.split(",") if s.strip()]
            except Exception:
                tech_list = [p.tech_stack]
        pd["tech_stack"] = tech_list
        pd["techStack"] = tech_list
        pd["proofFile"] = p.proof_file or ""
        pd["proof_file"] = p.proof_file or ""
        pd["githubLink"] = p.github_link or ""
        pd["github_link"] = p.github_link or ""
        pd["liveDemoLink"] = p.live_demo_link or ""
        pd["live_demo_link"] = p.live_demo_link or ""
        pd["mentorFeedback"] = p.mentor_feedback or ""
        pd["mentor_feedback"] = p.mentor_feedback or ""
        serialized_projects.append(pd)

    serialized_certs = []
    for c in certifications:
        cd = to_dict(c)
        cd["proofFile"] = c.proof_file or ""
        cd["proof_file"] = c.proof_file or ""
        cd["certificateLink"] = c.certificate_link or ""
        cd["certificate_link"] = c.certificate_link or ""
        cd["credentialId"] = c.credential_id or ""
        cd["credential_id"] = c.credential_id or ""
        cd["mentorFeedback"] = c.mentor_feedback or ""
        cd["mentor_feedback"] = c.mentor_feedback or ""
        serialized_certs.append(cd)

    serialized_achs = []
    for a in achievements:
        ad = to_dict(a)
        ad["proofFile"] = a.proof_file or ""
        ad["proof_file"] = a.proof_file or ""
        ad["proofLink"] = a.proof_link or ""
        ad["proof_link"] = a.proof_link or ""
        ad["achievementType"] = a.achievement_type
        ad["achievement_type"] = a.achievement_type
        ad["mentorFeedback"] = a.mentor_feedback or ""
        ad["mentor_feedback"] = a.mentor_feedback or ""
        serialized_achs.append(ad)

    # AI Summary
    ai_sum_dict = {}
    if ai_sum_obj:
        ai_sum_dict = {
            "summary": ai_sum_obj.summary,
            "strengths": json.loads(ai_sum_obj.strengths_json) if ai_sum_obj.strengths_json else [],
            "weaknesses": json.loads(ai_sum_obj.weaknesses_json) if ai_sum_obj.weaknesses_json else [],
            "recommendations": json.loads(ai_sum_obj.recommendations_json) if ai_sum_obj.recommendations_json else [],
            "placement_advice": ai_sum_obj.placement_advice or ""
        }

    # Combined payload returning both flat and nested parameters
    portfolio = {
        "student": student_dict,
        "about": {
            "headline": headline,
            "about_me": about_me,
            "aboutMe": about_me,
            "career_objective": career_objective,
            "careerObjective": career_objective,
            "skills": skills
        },
        "headline": headline,
        "career_objective": career_objective,
        "careerObjective": career_objective,
        "skills": skills,
        "github_url": github_url,
        "linkedin_url": linkedin_url,
        "resume_url": resume_dict.get("file_path") if resume_dict else "",
        "has_resume": bool(resume_dict and resume_dict.get("file_path")),
        "resume": resume_dict,
        "performance": performance_dict,
        "projects": serialized_projects,
        "certifications": serialized_certs,
        "achievements": serialized_achs,
        "portfolio_customization": custom_dict,
        "portfolioCustomization": custom_dict,
        "visibility": custom_dict.get("sectionVisibility") or {
            "showProjects": True,
            "showCertifications": True,
            "showAchievements": True,
            "showAcademicHighlights": True,
            "showContactLinks": True,
            "showResume": True
        },
        "ai_summary": ai_sum_dict,
        "aiSummary": ai_sum_dict,
        "profile_image": profile_image or "",
        "profileImage": profile_image or ""
    }

    return portfolio
