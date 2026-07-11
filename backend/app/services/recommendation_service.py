from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.score import StudentAnalytics
from app.utils.domain_utils import normalize_domain

def get_student_recommendations(db: Session, domain: str, limit: int) -> list:
    """
    Ranks and retrieves top recommended students in a given domain or overall.
    Calculates strength level and returns a detailed explanation.
    """
    norm_cat = normalize_domain(domain)
    
    # 1. Base query joining Student and StudentAnalytics
    query = db.query(Student, StudentAnalytics).join(
        StudentAnalytics, Student.id == StudentAnalytics.student_id
    )

    # 2. Sort by the specific domain average or overall score
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
        # Default to Overall sorting
        norm_cat = "Overall"
        query = query.order_by(StudentAnalytics.overall_score.desc())

    results = query.limit(limit).all()
    recommendations = []

    for idx, (student, analytics) in enumerate(results):
        # Determine domain score
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

        # Strength level logic: 90+ Excellent, 80-89 Good, 70-79 Needs Improvement, Below 70 Critical
        if domain_score >= 90:
            strength_level = "Excellent"
        elif domain_score >= 80:
            strength_level = "Good"
        elif domain_score >= 70:
            strength_level = "Needs Improvement"
        else:
            strength_level = "Critical"

        # Generate reason
        if norm_cat == "Overall":
            reason = f"Secured an excellent cumulative average of {analytics.overall_score}% across all subjects."
        else:
            reason = f"Demonstrated top-tier capability in {norm_cat} with a domain score of {domain_score}%."

        recommendations.append({
            "rank": idx + 1,
            "id": student.id,
            "register_no": student.register_no,
            "registerNo": student.register_no,
            "name": student.name,
            "domain": norm_cat,
            "domain_score": domain_score,
            "domainScore": domain_score,
            "overall_score": analytics.overall_score,
            "overallScore": analytics.overall_score,
            "strength_level": strength_level,
            "strengthLevel": strength_level,
            "reason": reason
        })

    return recommendations
