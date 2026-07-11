import json
import httpx
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.config import settings
from app.models.student import Student
from app.models.score import StudentAnalytics, AssessmentScore
from app.models.submission import StudentProject, StudentCertification, StudentAchievement
from app.models.profile import UserProfile
from app.models.ai_summary import AISummary

def generate_rule_based_performance_summary(
    student: Student,
    analytics: StudentAnalytics,
    scores: list,
    projects: list,
    certs: list,
    achieves: list
) -> dict:
    """
    Generates a deterministic performance summary, strengths, weaknesses, 
    recommendations, and placement advice based on database metrics.
    """
    if not analytics:
        return {
            "summary": f"{student.name} is a student in the {student.department} department. No test metrics are available yet.",
            "strengths": [],
            "weaknesses": [],
            "recommendations": ["Participate in initial assessment tests to build profile metrics."],
            "placement_advice": "Structured training is recommended as performance metrics are pending.",
            "placementAdvice": "Structured training is recommended as performance metrics are pending."
        }

    # 1. Strengths (>= 85) & Weaknesses (< 80)
    domain_map = {
        "DSA": analytics.dsa_average,
        "DBMS": analytics.dbms_average,
        "FullStack": analytics.fullstack_average,
        "Aptitude": analytics.aptitude_average,
        "Coding": analytics.coding_average,
        "Academic": analytics.academic_average,
        "Technical": analytics.technical_average
    }

    strengths = [cat for cat, score in domain_map.items() if score >= 85.0]
    weaknesses = [cat for cat, score in domain_map.items() if score < 80.0]

    # If no strengths/weaknesses fit criteria, fallback to highest and lowest
    if not strengths and domain_map:
        highest_cat = max(domain_map, key=domain_map.get)
        if domain_map[highest_cat] > 0:
            strengths = [highest_cat]
            
    if not weaknesses and domain_map:
        lowest_cat = min(domain_map, key=domain_map.get)
        if domain_map[lowest_cat] < 85.0:
            weaknesses = [lowest_cat]

    # 2. Recommendations
    recommendations = []
    weakest = analytics.weakest_domain or (min(domain_map, key=domain_map.get) if domain_map else None)

    if weakest == "DBMS":
        recommendations = [
            "Practice complex SQL joins and subqueries on platforms like LeetCode or HackerRank.",
            "Revise database normalization (1NF, 2NF, 3NF, BCNF) and transaction ACID properties.",
            "Build one database-backed project to apply database schema design concepts practically."
        ]
    elif weakest == "Aptitude":
        recommendations = [
            "Practice daily aptitude sets covering quantitative, logical, and verbal topics.",
            "Take weekly timed mock tests to improve time management and speed.",
            "Improve speed and accuracy on core concepts like percentages, ratios, and permutations."
        ]
    elif weakest == "DSA":
        recommendations = [
            "Practice fundamental data structures: arrays, strings, stacks, and linked lists.",
            "Revise core algorithms: searching, sorting, recursion, trees, and graphs.",
            "Solve coding problems consistently (at least 2-3 per day) to build problem-solving muscle."
        ]
    elif weakest == "Coding":
        recommendations = [
            "Practice timed coding contests on platforms like CodeChef, Codeforces, or LeetCode.",
            "Improve implementation speed and reduce compilation error rates.",
            "Revise syntax and libraries of your primary programming language (e.g. Java, Python, C++)."
        ]
    elif weakest == "Academic":
        recommendations = [
            "Review core subject lecture notes and text materials regularly.",
            "Improve semester exam consistency and class assessment scores.",
            "Engage in academic study groups to clarify fundamentals."
        ]
    elif weakest == "Technical":
        recommendations = [
            "Practice technical interview questions regarding core computer science concepts.",
            "Revise CS fundamentals (OS, Networks, OOPS, and System Design).",
            "Solve mock technical interviews and explain code complexity out loud."
        ]
    else:
        recommendations = [
            "Maintain consistent coding practices daily to keep problem-solving skills sharp.",
            "Build more real-world software projects to expand your repository portfolio.",
            "Practice mock interview sessions to boost behavioral and presentation skills."
        ]

    # 3. Placement Advice based on readiness level
    level = analytics.placement_readiness_level
    if level == "Placement Ready":
        placement_advice = (
            "Student is ready for placement-level preparation. Focus on advanced coding interviews, "
            "system design basics, and mock interview communication practices."
        )
    elif level == "Almost Ready":
        placement_advice = (
            f"Student is close to placement readiness (Score: {analytics.placement_readiness_score}%). "
            f"Should focus on bolstering weak domains ({', '.join(weaknesses) if weaknesses else weakest}) "
            "and completing pending certifications."
        )
    else:
        # Needs Training
        placement_advice = (
            "Student requires structured training before placement drives. Focus heavily on core subjects, "
            "solving daily coding practices, and creating fundamental resume projects."
        )

    # 4. Narrative Summary
    strong_str = ", ".join(strengths) if strengths else "various topics"
    weak_str = ", ".join(weaknesses) if weaknesses else weakest or "none"
    
    summary = (
        f"{student.name} shows strong performance in {strong_str} domains with an overall average of "
        f"{analytics.overall_score}%. "
    )
    if weaknesses:
        summary += f"However, capabilities in {weak_str} require more targeted improvement and revision."
    else:
        summary += "Consistent capabilities are demonstrated across all tested evaluation categories."

    return {
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "placement_advice": placement_advice,
        "placementAdvice": placement_advice
    }

async def generate_student_ai_summary(db: Session, student_id: int) -> dict:
    """
    Attempts to generate student summary using Ollama LLM provider.
    Falls back to deterministic rule-based generator if Ollama is unreachable.
    Saves the final generated result into the AISummary table.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return {}

    analytics = db.query(StudentAnalytics).filter(StudentAnalytics.student_id == student_id).first()
    scores = db.query(AssessmentScore).filter(AssessmentScore.student_id == student_id).all()
    projects = db.query(StudentProject).filter(StudentProject.student_id == student_id, StudentProject.status == "Approved").all()
    certs = db.query(StudentCertification).filter(StudentCertification.student_id == student_id, StudentCertification.status == "Approved").all()
    achieves = db.query(StudentAchievement).filter(StudentAchievement.student_id == student_id, StudentAchievement.status == "Approved").all()

    # Get rule-based base metrics
    rule_data = generate_rule_based_performance_summary(
        student, analytics, scores, projects, certs, achieves
    )

    # Check if Ollama provider is configured
    if settings.LLM_PROVIDER == "ollama" and analytics:
        prompt = (
            f"Generate a professional, encouraging student performance summary and placement advice in English "
            f"based on the following student performance metrics:\n"
            f"Student Name: {student.name}\n"
            f"Department: {student.department}\n"
            f"Overall average score: {analytics.overall_score}%\n"
            f"Domain averages: DSA ({analytics.dsa_average}%), DBMS ({analytics.dbms_average}%), "
            f"FullStack ({analytics.fullstack_average}%), Aptitude ({analytics.aptitude_average}%), "
            f"Coding ({analytics.coding_average}%), Academic ({analytics.academic_average}%), "
            f"Technical ({analytics.technical_average}%)\n"
            f"Strongest domain: {analytics.strongest_domain}\n"
            f"Weakest domain: {analytics.weakest_domain}\n"
            f"Approved projects count: {len(projects)}\n"
            f"Approved certifications count: {len(certs)}\n"
            f"Approved achievements count: {len(achieves)}\n"
            f"Placement Readiness Score: {analytics.placement_readiness_score} ({analytics.placement_readiness_level})\n\n"
            f"Output must be a JSON object matching this exact schema:\n"
            f'{{"summary": "...", "placement_advice": "..."}}\n'
            f"Do not include any other markdown tags or conversational prefix, only output raw JSON."
        )

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                )
                if resp.status_code == 200:
                    result = resp.json()
                    response_text = result.get("response", "").strip()
                    parsed = json.loads(response_text)
                    
                    if "summary" in parsed:
                        rule_data["summary"] = parsed["summary"]
                    if "placement_advice" in parsed:
                        rule_data["placement_advice"] = parsed["placement_advice"]
                        rule_data["placementAdvice"] = parsed["placement_advice"]
        except Exception:
            # Fallback to rule-based silently on connection errors
            pass

    # Save to AISummary table
    ai_sum = db.query(AISummary).filter(AISummary.student_id == student_id).first()
    if not ai_sum:
        ai_sum = AISummary(student_id=student_id)
        db.add(ai_sum)

    ai_sum.summary = rule_data["summary"]
    ai_sum.strengths_json = json.dumps(rule_data["strengths"])
    ai_sum.weaknesses_json = json.dumps(rule_data["weaknesses"])
    ai_sum.recommendations_json = json.dumps(rule_data["recommendations"])
    ai_sum.placement_advice = rule_data["placement_advice"]
    
    db.commit()
    db.refresh(ai_sum)

    return rule_data

def execute_faculty_query(db: Session, query_str: str) -> dict:
    """
    Parses natural language query patterns submitted by faculties/mentors
    and retrieves structured student database query outputs.
    """
    normalized_query = query_str.lower().strip()
    
    # 1. Initialize result structure
    intent = "general"
    domain = "Overall"
    limit = 10
    students_list = []
    answer = "No matching query pattern detected. Try queries like 'Top 10 DSA students' or 'Students needing attention'."

    # Helper serializer for student rankings
    def map_student_row(student: Student, analytics: StudentAnalytics, idx: int, target_domain: str = "Overall"):
        # Select target domain average
        if target_domain == "DSA":
            domain_score = analytics.dsa_average
        elif target_domain == "DBMS":
            domain_score = analytics.dbms_average
        elif target_domain == "FullStack":
            domain_score = analytics.fullstack_average
        elif target_domain == "Aptitude":
            domain_score = analytics.aptitude_average
        elif target_domain == "Coding":
            domain_score = analytics.coding_average
        elif target_domain == "Academic":
            domain_score = analytics.academic_average
        elif target_domain == "Technical":
            domain_score = analytics.technical_average
        elif target_domain == "Placement":
            domain_score = analytics.placement_readiness_score
        else:
            domain_score = analytics.overall_score

        return {
            "rank": idx + 1,
            "id": student.id,
            "register_no": student.register_no,
            "registerNo": student.register_no,
            "name": student.name,
            "score": domain_score,
            "overall_score": analytics.overall_score,
            "overallScore": analytics.overall_score,
            "domain_score": domain_score,
            "domainScore": domain_score,
            "strongest_domain": analytics.strongest_domain,
            "strongestDomain": analytics.strongest_domain,
            "weakest_domain": analytics.weakest_domain,
            "weakestDomain": analytics.weakest_domain,
            "placement_readiness_score": analytics.placement_readiness_score,
            "placementReadinessScore": analytics.placement_readiness_score,
            "placement_readiness_level": analytics.placement_readiness_level,
            "placementReadinessLevel": analytics.placement_readiness_level,
            "profile_image": student.profile_image or "",
            "profileImage": student.profile_image or ""
        }

    # 2. Check query intent mappings
    # Leaderboard Domain topper queries
    domains_check = {
        "dsa": "DSA",
        "dbms": "DBMS",
        "fullstack": "FullStack",
        "full stack": "FullStack",
        "aptitude": "Aptitude",
        "coding": "Coding",
        "academic": "Academic",
        "technical": "Technical"
    }

    # Match Domain Top 10
    matched_domain = None
    for pattern, d_name in domains_check.items():
        if f"top 10 {pattern}" in normalized_query or f"top 10 {pattern} students" in normalized_query:
            matched_domain = d_name
            break

    if matched_domain:
        intent = "leaderboard"
        domain = matched_domain
        limit = 10
        
        # Query sorting by selected domain score
        query = db.query(Student, StudentAnalytics).join(
            StudentAnalytics, Student.id == StudentAnalytics.student_id
        )
        if matched_domain == "DSA":
            query = query.order_by(StudentAnalytics.dsa_average.desc())
        elif matched_domain == "DBMS":
            query = query.order_by(StudentAnalytics.dbms_average.desc())
        elif matched_domain == "FullStack":
            query = query.order_by(StudentAnalytics.fullstack_average.desc())
        elif matched_domain == "Aptitude":
            query = query.order_by(StudentAnalytics.aptitude_average.desc())
        elif matched_domain == "Coding":
            query = query.order_by(StudentAnalytics.coding_average.desc())
        elif matched_domain == "Academic":
            query = query.order_by(StudentAnalytics.academic_average.desc())
        elif matched_domain == "Technical":
            query = query.order_by(StudentAnalytics.technical_average.desc())

        results = query.limit(limit).all()
        students_list = [map_student_row(s, a, i, matched_domain) for i, (s, a) in enumerate(results)]
        answer = f"Here are the top 10 {matched_domain} students based on verified test averages."

    # Match Overall toppers
    elif "overall toppers" in normalized_query or "top 10 overall" in normalized_query:
        intent = "leaderboard"
        domain = "Overall"
        limit = 10

        query = db.query(Student, StudentAnalytics).join(
            StudentAnalytics, Student.id == StudentAnalytics.student_id
        ).order_by(StudentAnalytics.overall_score.desc()).limit(limit)
        
        results = query.all()
        students_list = [map_student_row(s, a, i, "Overall") for i, (s, a) in enumerate(results)]
        answer = "Here are the top overall student performers based on cumulative average scores."

    # Match Placement Ready
    elif "placement" in normalized_query or "ready" in normalized_query:
        intent = "placement_readiness"
        domain = "Overall"
        limit = 10

        # Retrieve students with Placement Ready status
        query = db.query(Student, StudentAnalytics).join(
            StudentAnalytics, Student.id == StudentAnalytics.student_id
        ).filter(
            StudentAnalytics.placement_readiness_level == "Placement Ready"
        ).order_by(StudentAnalytics.placement_readiness_score.desc()).limit(limit)

        results = query.all()
        if not results:
            query = db.query(Student, StudentAnalytics).join(
                StudentAnalytics, Student.id == StudentAnalytics.student_id
            ).order_by(StudentAnalytics.placement_readiness_score.desc()).limit(limit)
            results = query.all()

        students_list = [map_student_row(s, a, i, "Placement") for i, (s, a) in enumerate(results)]
        answer = f"Here are the top students (up to {limit}) who are classified as 'Placement Ready'."

    # Match Below Average
    elif "below average" in normalized_query or "below class average" in normalized_query:
        intent = "below_average"
        domain = "Overall"
        limit = 10

        # Calculate overall class average
        avg_score = db.query(func.avg(StudentAnalytics.overall_score)).scalar()
        if avg_score is None:
            avg_score = 0.0
            
        query = db.query(Student, StudentAnalytics).join(
            StudentAnalytics, Student.id == StudentAnalytics.student_id
        ).filter(
            StudentAnalytics.overall_score < avg_score
        ).order_by(StudentAnalytics.overall_score.asc()).limit(limit)

        results = query.all()
        students_list = [map_student_row(s, a, i, "Overall") for i, (s, a) in enumerate(results)]
        answer = f"Here are students performing below the overall class average of {round(avg_score, 2)}%."

    # Match Needing Attention
    elif "needing attention" in normalized_query or "attention" in normalized_query:
        intent = "needing_attention"
        domain = "Overall"
        limit = 10

        # Filter criteria: overall < 70 OR placement_level == Needs Training OR any domain < 70
        query = db.query(Student, StudentAnalytics).join(
            StudentAnalytics, Student.id == StudentAnalytics.student_id
        ).filter(
            (StudentAnalytics.overall_score < 70.0) |
            (StudentAnalytics.placement_readiness_level == "Needs Training") |
            (StudentAnalytics.dsa_average < 70.0) |
            (StudentAnalytics.dbms_average < 70.0) |
            (StudentAnalytics.fullstack_average < 70.0) |
            (StudentAnalytics.aptitude_average < 70.0) |
            (StudentAnalytics.coding_average < 70.0) |
            (StudentAnalytics.academic_average < 70.0) |
            (StudentAnalytics.technical_average < 70.0)
        ).order_by(StudentAnalytics.overall_score.asc()).limit(limit)

        results = query.all()
        students_list = [map_student_row(s, a, i, "Overall") for i, (s, a) in enumerate(results)]
        answer = "Here are the students flagged as needing attention due to critical domain scores or training levels."

    return {
        "intent": intent,
        "domain": domain,
        "limit": limit,
        "students": students_list,
        "answer": answer
    }
