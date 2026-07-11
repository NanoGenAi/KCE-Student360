from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.score import AssessmentScore, StudentAnalytics
from app.models.submission import StudentProject, StudentCertification
from app.models.student import Student

def recalculate_student_analytics(db: Session, student_id: int):
    """
    Recalculates all performance metrics and placement readiness for a student
    and saves/updates their StudentAnalytics record.
    """
    # 1. Fetch all scores for the student, sorted by assessment_date ascending
    scores = db.query(AssessmentScore).filter(
        AssessmentScore.student_id == student_id
    ).order_by(AssessmentScore.assessment_date.asc()).all()

    # Get student reference (to update CGPA if needed or check)
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None

    # Fetch existing analytics or create a new one
    analytics = db.query(StudentAnalytics).filter(
        StudentAnalytics.student_id == student_id
    ).first()
    if not analytics:
        analytics = StudentAnalytics(student_id=student_id)
        db.add(analytics)

    # If no scores exist yet, apply defaults
    if not scores:
        analytics.overall_score = 0.0
        analytics.dsa_average = 0.0
        analytics.dbms_average = 0.0
        analytics.fullstack_average = 0.0
        analytics.aptitude_average = 0.0
        analytics.coding_average = 0.0
        analytics.academic_average = 0.0
        analytics.technical_average = 0.0
        analytics.strongest_domain = None
        analytics.weakest_domain = None
        analytics.total_assessments = 0
        analytics.latest_score = 0.0
        analytics.best_score = 0.0
        analytics.average_test_score = 0.0
        analytics.improvement_trend = "Stable"
        
        # Calculate readiness based only on project/certification counts
        proj_count = db.query(StudentProject).filter(
            StudentProject.student_id == student_id, StudentProject.status == "Approved"
        ).count()
        cert_count = db.query(StudentCertification).filter(
            StudentCertification.student_id == student_id, StudentCertification.status == "Approved"
        ).count()
        
        proj_contrib = 100.0 if proj_count >= 2 else (75.0 if proj_count == 1 else 50.0)
        cert_contrib = 100.0 if cert_count >= 2 else (75.0 if cert_count == 1 else 50.0)
        
        readiness = (proj_contrib * 0.10) + (cert_contrib * 0.10)
        analytics.placement_readiness_score = round(readiness, 2)
        analytics.placement_readiness_level = "Needs Training"
        db.flush()
        return analytics

    # 2. Calculate category averages
    categories = ["DSA", "DBMS", "FullStack", "Aptitude", "Coding", "Academic", "Technical"]
    category_scores = {cat: [] for cat in categories}
    percentages = []

    for score in scores:
        percentages.append(score.percentage)
        if score.category in category_scores:
            category_scores[score.category].append(score.percentage)

    averages = {}
    for cat in categories:
        cat_list = category_scores[cat]
        averages[cat] = round(sum(cat_list) / len(cat_list), 2) if cat_list else 0.0

    # Save averages
    analytics.dsa_average = averages["DSA"]
    analytics.dbms_average = averages["DBMS"]
    analytics.fullstack_average = averages["FullStack"]
    analytics.aptitude_average = averages["Aptitude"]
    analytics.coding_average = averages["Coding"]
    analytics.academic_average = averages["Academic"]
    analytics.technical_average = averages["Technical"]

    # 3. Overall score (average of available domain averages, do not count missing as zero)
    active_averages = [avg for cat, avg in averages.items() if len(category_scores[cat]) > 0]
    overall_score = round(sum(active_averages) / len(active_averages), 2) if active_averages else 0.0
    analytics.overall_score = overall_score

    # 4. Strongest & Weakest domain
    active_domain_map = {cat: avg for cat, avg in averages.items() if len(category_scores[cat]) > 0}
    if active_domain_map:
        analytics.strongest_domain = max(active_domain_map, key=active_domain_map.get)
        analytics.weakest_domain = min(active_domain_map, key=active_domain_map.get)
    else:
        analytics.strongest_domain = None
        analytics.weakest_domain = None

    # 5. Total assessments
    analytics.total_assessments = len(scores)

    # 6. Latest score (most recent assessment percentage)
    analytics.latest_score = scores[-1].percentage

    # 7. Best score (highest percentage in history)
    analytics.best_score = max(percentages)

    # 8. Average test score (average of all assessment percentages)
    analytics.average_test_score = round(sum(percentages) / len(percentages), 2)

    # 9. Improvement trend (Compare latest 3 assessments with previous 3)
    if len(percentages) >= 6:
        latest_3_avg = sum(percentages[-3:]) / 3.0
        prev_3_avg = sum(percentages[-6:-3]) / 3.0
        diff = latest_3_avg - prev_3_avg
        if diff >= 3.0:
            analytics.improvement_trend = "Improving"
        elif diff < -3.0:
            analytics.improvement_trend = "Needs Attention"
        else:
            analytics.improvement_trend = "Stable"
    else:
        analytics.improvement_trend = "Stable"

    # 10. Placement readiness
    # Fetch approved counts
    proj_count = db.query(StudentProject).filter(
        StudentProject.student_id == student_id, StudentProject.status == "Approved"
    ).count()
    cert_count = db.query(StudentCertification).filter(
        StudentCertification.student_id == student_id, StudentCertification.status == "Approved"
    ).count()

    proj_contrib = 100.0 if proj_count >= 2 else (75.0 if proj_count == 1 else 50.0)
    cert_contrib = 100.0 if cert_count >= 2 else (75.0 if cert_count == 1 else 50.0)

    # readiness = overall * 0.3 + coding * 0.2 + aptitude * 0.15 + technical * 0.15 + project * 0.1 + cert * 0.1
    readiness = (
        (overall_score * 0.30)
        + (averages["Coding"] * 0.20)
        + (averages["Aptitude"] * 0.15)
        + (averages["Technical"] * 0.15)
        + (proj_contrib * 0.10)
        + (cert_contrib * 0.10)
    )
    analytics.placement_readiness_score = round(readiness, 2)

    if readiness >= 85.0:
        analytics.placement_readiness_level = "Placement Ready"
    elif readiness >= 70.0:
        analytics.placement_readiness_level = "Almost Ready"
    else:
        analytics.placement_readiness_level = "Needs Training"

    db.flush()
    return analytics
