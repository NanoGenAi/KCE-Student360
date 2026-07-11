from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.score import StudentAnalytics
from app.utils.domain_utils import normalize_domain

def get_leaderboard_data(db: Session, domain: str = "Overall") -> list:
    """
    Retrieves ranked student rankings sorted by overall_score or a specific domain score.
    Returns compatible lists matching camelCase and snake_case properties.
    """
    # 1. Base query
    query = db.query(Student, StudentAnalytics).join(
        StudentAnalytics, Student.id == StudentAnalytics.student_id
    )

    norm_cat = normalize_domain(domain)
    
    # 2. Sort by the target average score
    if norm_cat == "DSA":
        query = query.order_by(StudentAnalytics.dsa_average.desc())
    elif norm_cat == "DBMS":
        query = query.order_by(StudentAnalytics.dbms_average.desc())
    elif norm_cat == "FullStack":
        query = query.order_by(StudentAnalytics.fullstack_average.desc())
    elif norm_cat == "Aptitude":
        query = query.order_by(StudentAnalytics.aptitude_average.desc())
    elif norm_cat == "Coding":
        query = query.order_by(StudentAnalytics.coding_average.desc())
    elif norm_cat == "Academic":
        query = query.order_by(StudentAnalytics.academic_average.desc())
    elif norm_cat == "Technical":
        query = query.order_by(StudentAnalytics.technical_average.desc())
    else:
        norm_cat = "Overall"
        query = query.order_by(StudentAnalytics.overall_score.desc())

    records = query.all()
    leaderboard = []

    for idx, (student, analytics) in enumerate(records):
        # Determine the domain score
        if norm_cat == "DSA":
            domain_score = analytics.dsa_average
        elif norm_cat == "DBMS":
            domain_score = analytics.dbms_average
        elif norm_cat == "FullStack":
            domain_score = analytics.fullstack_average
        elif norm_cat == "Aptitude":
            domain_score = analytics.aptitude_average
        elif norm_cat == "Coding":
            domain_score = analytics.coding_average
        elif norm_cat == "Academic":
            domain_score = analytics.academic_average
        elif norm_cat == "Technical":
            domain_score = analytics.technical_average
        else:
            domain_score = analytics.overall_score

        profile_image = student.profile_image
        if not profile_image and student.user_id:
            from app.models.profile import UserProfile
            user_prof = db.query(UserProfile).filter(UserProfile.user_id == student.user_id).first()
            if user_prof:
                profile_image = user_prof.profile_image

        leaderboard.append({
            "id": student.id,
            "rank": idx + 1,
            "register_no": student.register_no,
            "registerNo": student.register_no,
            "name": student.name,
            "overall_score": analytics.overall_score,
            "overallScore": analytics.overall_score,
            "domain_score": domain_score,
            "domainScore": domain_score,
            "best_score": analytics.best_score,
            "bestScore": analytics.best_score,
            "latest_score": analytics.latest_score,
            "latestScore": analytics.latest_score,
            "strongest_domain": analytics.strongest_domain,
            "strongestDomain": analytics.strongest_domain,
            "weakest_domain": analytics.weakest_domain,
            "weakestDomain": analytics.weakest_domain,
            "profile_image": profile_image or "",
            "profileImage": profile_image or ""
        })

    return leaderboard
