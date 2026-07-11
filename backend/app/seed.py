import os
import sys
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session

# Add the project root to python path to run as a module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.student import Student, FacultyProfile, MentorAssignment
from app.models.score import AssessmentScore, StudentAnalytics
from app.models.submission import StudentProject, StudentCertification, StudentAchievement
from app.models.profile import UserProfile, StudentAbout
from app.models.portfolio import PortfolioCustomization
from app.utils.security import get_password_hash
from app.services.analytics_service import recalculate_student_analytics

def seed_data():
    """Populates the database with demo users, 10 students, scores, and submissions. Idempotent check-existing."""
    print("Initializing database session...")
    db = SessionLocal()
    try:
        print("Seeding/Verifying demo users...")
        hashed_password = get_password_hash("Password123!")

        # 1. Create Core Users if missing
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(username="admin", email="admin@student360.com", password_hash=hashed_password, role="admin")
            db.add(admin_user)
            db.flush()

        faculty_user = db.query(User).filter(User.username == "faculty").first()
        if not faculty_user:
            faculty_user = User(username="faculty", email="faculty@student360.com", password_hash=hashed_password, role="faculty")
            db.add(faculty_user)
            db.flush()

        mentor_user = db.query(User).filter(User.username == "mentor").first()
        if not mentor_user:
            mentor_user = User(username="mentor", email="mentor@student360.com", password_hash=hashed_password, role="mentor")
            db.add(mentor_user)
            db.flush()

        placement_user = db.query(User).filter(User.username == "placement").first()
        if not placement_user:
            placement_user = User(username="placement", email="placement@student360.com", password_hash=hashed_password, role="placement_mentor")
            db.add(placement_user)
            db.flush()

        # Create Profiles for faculty and admin if missing
        admin_profile = db.query(UserProfile).filter(UserProfile.user_id == admin_user.id).first()
        if not admin_profile:
            admin_profile = UserProfile(user_id=admin_user.id, full_name="Admin Officer", email="admin@student360.com", department="Administration")
            db.add(admin_profile)

        faculty_profile = db.query(FacultyProfile).filter(FacultyProfile.user_id == faculty_user.id).first()
        if not faculty_profile:
            faculty_profile = FacultyProfile(user_id=faculty_user.id, name="Dr. Ramanujam", email="faculty@student360.com", department="Computer Science & Engineering", designation="Professor & Head")
            db.add(faculty_profile)

        mentor_profile = db.query(UserProfile).filter(UserProfile.user_id == mentor_user.id).first()
        if not mentor_profile:
            mentor_profile = UserProfile(user_id=mentor_user.id, full_name="Prof. Priya", email="mentor@student360.com", department="Information Technology")
            db.add(mentor_profile)

        placement_profile = db.query(UserProfile).filter(UserProfile.user_id == placement_user.id).first()
        if not placement_profile:
            placement_profile = UserProfile(user_id=placement_user.id, full_name="Placement Mentor", email="placement@student360.com", department="Placement Cell")
            db.add(placement_profile)
        
        db.flush()

        # 2. Create 10 Students
        student_names = [
            "Shahul", "Rachith", "Padma Kumar", "Priya", "Meera",
            "Arun", "Kavin", "Nisha", "Harini", "Sanjay"
        ]
        
        register_numbers = [
            "22AD001", "22AD002", "22AD003", "22AD004", "22AD005",
            "22AD006", "22AD007", "22AD008", "22AD009", "22AD010"
        ]

        students = []
        student_users = []

        for i, name in enumerate(student_names):
            reg = register_numbers[i]
            if name == "Shahul":
                email = "shahul@student360.com"
                username = "shahul"
            else:
                email = f"{name.lower().replace(' ', '')}@student360.com"
                username = reg.lower()
            
            # Check User record
            u = db.query(User).filter(User.username == username).first()
            if not u:
                u = User(username=username, email=email, password_hash=hashed_password, role="student")
                db.add(u)
                db.flush()
            student_users.append(u)

            # Check Student record
            s = db.query(Student).filter(Student.register_no == reg).first()
            if not s:
                cgpa = round(8.0 + (i * 0.1), 2)
                s = Student(
                    user_id=u.id,
                    register_no=reg,
                    name=name,
                    email=email,
                    phone=f"987654321{i}",
                    department="AI & DS",
                    year="III",
                    section="A",
                    batch="2028",
                    cgpa=cgpa,
                    profile_image=None
                )
                db.add(s)
                db.flush()
            students.append(s)

            # Check Assignment
            assignment = db.query(MentorAssignment).filter(MentorAssignment.student_id == s.id).first()
            if not assignment:
                assignment = MentorAssignment(mentor_id=mentor_user.id, student_id=s.id)
                db.add(assignment)

            # Check UserProfile for student
            up = db.query(UserProfile).filter(UserProfile.user_id == u.id).first()
            if not up:
                up = UserProfile(
                    user_id=u.id,
                    full_name=name,
                    email=email,
                    phone=s.phone,
                    department="AI & DS",
                    location="Coimbatore",
                    profile_image=None,
                    bio=f"I am {name}, studying Artificial Intelligence & Data Science."
                )
                db.add(up)

            # Check StudentAbout
            about = db.query(StudentAbout).filter(StudentAbout.student_id == s.id).first()
            if not about:
                about = StudentAbout(
                    student_id=s.id,
                    headline="AI & DS Student | Aspiring SDE",
                    about_me=f"I am {name}, an Artificial Intelligence and Data Science student. I love coding and problem solving.",
                    career_objective="To build a strong career in software development.",
                    skills_json='["Python", "DSA", "DBMS", "Java"]'
                )
                db.add(about)

            # Check Customization
            cust = db.query(PortfolioCustomization).filter(PortfolioCustomization.student_id == s.id).first()
            if not cust:
                cust = PortfolioCustomization(
                    student_id=s.id,
                    headline="AI & DS Student | Aspiring SDE",
                    about_me=f"I am {name}, an Artificial Intelligence and Data Science student. I love coding and problem solving.",
                    career_objective="To build a strong career in software development.",
                    skills_json='["Python", "DSA", "DBMS", "Java"]',
                    theme="Dark Minimal",
                    section_visibility_json='{"showProjects":true,"showCertifications":true,"showAchievements":true,"showAcademicHighlights":true,"showContactLinks":true}',
                    resume_visibility=True
                )
                db.add(cust)

        db.flush()

        # 3. Create Assessment Scores
        # Categories: DSA, DBMS, FullStack, Aptitude, Coding, Academic, Technical
        base_scores = {
            "DSA": [85, 70, 75, 90, 80, 65, 88, 72, 95, 60],        # Sanjay (index 8) is highest in DSA
            "DBMS": [75, 80, 98, 85, 90, 60, 70, 92, 88, 82],       # Padma Kumar (index 2) is highest in DBMS
            "FullStack": [98, 88, 80, 85, 72, 90, 65, 78, 84, 70],  # Shahul (index 0) is highest in FullStack
            "Aptitude": [75, 82, 80, 88, 92, 70, 84, 76, 90, 65],   # Sanjay / Meera are strong
            "Coding": [96, 75, 85, 88, 70, 92, 80, 68, 90, 74],     # Shahul is strong
            "Academic": [88, 92, 84, 90, 86, 78, 80, 85, 94, 72],   # Harini is highest
            "Technical": [94, 80, 88, 85, 78, 90, 72, 82, 86, 68]   # Shahul is strong
        }

        # Check and populate scores for students
        for i, student in enumerate(students):
            score_exists = db.query(AssessmentScore).filter(AssessmentScore.student_id == student.id).first()
            if not score_exists:
                for category, scores_list in base_scores.items():
                    base_percentage = scores_list[i]
                    
                    # 1. Midterm assessment
                    score1 = AssessmentScore(
                        student_id=student.id,
                        uploaded_by=faculty_user.id,
                        assessment_name=f"{category} Midterm",
                        category=category,
                        score=base_percentage - 2,
                        max_marks=100.0,
                        percentage=base_percentage - 2,
                        assessment_date=datetime.utcnow() - timedelta(days=30)
                    )
                    # 2. Endterm assessment
                    score2 = AssessmentScore(
                        student_id=student.id,
                        uploaded_by=faculty_user.id,
                        assessment_name=f"{category} Endterm",
                        category=category,
                        score=base_percentage + 2,
                        max_marks=100.0,
                        percentage=base_percentage + 2,
                        assessment_date=datetime.utcnow() - timedelta(days=10)
                    )
                    db.add_all([score1, score2])

        db.flush()

        # 4. Add Project, Certification, or Achievement if missing
        # Shahul (index 0) Project
        shahul_proj_exists = db.query(StudentProject).filter(
            StudentProject.student_id == students[0].id,
            StudentProject.title == "E-Commerce Microservices Platform"
        ).first()
        
        if not shahul_proj_exists:
            shahul_proj = StudentProject(
                student_id=students[0].id,
                title="E-Commerce Microservices Platform",
                description="Built a microservices e-commerce platform using React, FastAPI, and PostgreSQL with JWT auth.",
                tech_stack='["React", "FastAPI", "PostgreSQL", "Docker"]',
                role="Lead Backend Developer",
                github_link="https://github.com/shahul/ecommerce-ms",
                live_demo_link="https://ecommerce-ms.example.com",
                status="Approved",
                mentor_feedback="Excellent work on backend structure and API design.",
                reviewed_by=mentor_user.id,
                reviewed_at=datetime.utcnow()
            )
            db.add(shahul_proj)

        # Priya (index 3) Certification
        priya_cert_exists = db.query(StudentCertification).filter(
            StudentCertification.student_id == students[3].id,
            StudentCertification.title == "AWS Certified Solutions Architect - Associate"
        ).first()

        if not priya_cert_exists:
            priya_cert = StudentCertification(
                student_id=students[3].id,
                title="AWS Certified Solutions Architect - Associate",
                issuer="Amazon Web Services (AWS)",
                credential_id="AWS-ASA-9921",
                issue_date=date(2025, 1, 15),
                expiry_date=date(2028, 1, 15),
                certificate_link="https://aws.verification.com/cert/aws-asa-9921",
                status="Approved",
                mentor_feedback="Well done! Cloud credentials significantly boost career alignment.",
                reviewed_by=mentor_user.id,
                reviewed_at=datetime.utcnow()
            )
            db.add(priya_cert)

        # Meera (index 4) Achievement
        meera_ach_exists = db.query(StudentAchievement).filter(
            StudentAchievement.student_id == students[4].id,
            StudentAchievement.title == "Smart India Hackathon 2025 Finalist"
        ).first()

        if not meera_ach_exists:
            meera_ach = StudentAchievement(
                student_id=students[4].id,
                title="Smart India Hackathon 2025 Finalist",
                achievement_type="Hackathon",
                organization="Ministry of Education, Government of India",
                description="Qualified to the national finals of SIH 2025 under smart agriculture theme.",
                achievement_date=date(2025, 3, 10),
                proof_link="https://sih.gov.in/finalists",
                status="Pending"
            )
            db.add(meera_ach)
        
        db.flush()

        # Recalculate StudentAnalytics for each student to capture live project/cert counts & averages
        print("Recalculating analytics averages and placement readiness score metrics...")
        for s in students:
            recalculate_student_analytics(db, s.id)

        db.commit()
        print("Database successfully seeded with demo and student data.")

    except Exception as e:
        db.rollback()
        print(f"Error occurred during seeding: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
