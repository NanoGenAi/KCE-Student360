from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    register_no = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    department = Column(String, nullable=False)
    year = Column(String, nullable=False)
    section = Column(String, nullable=False)
    batch = Column(String, nullable=False)
    cgpa = Column(Float, default=0.0, nullable=False)
    profile_image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    analytics = relationship("StudentAnalytics", back_populates="student", uselist=False, cascade="all, delete-orphan")
    about = relationship("StudentAbout", back_populates="student", uselist=False, cascade="all, delete-orphan")
    portfolio_customization = relationship("PortfolioCustomization", back_populates="student", uselist=False, cascade="all, delete-orphan")
    ai_summary = relationship("AISummary", back_populates="student", uselist=False, cascade="all, delete-orphan")
    
    # Submissions and Scores
    scores = relationship("AssessmentScore", back_populates="student", cascade="all, delete-orphan")
    projects = relationship("StudentProject", back_populates="student", cascade="all, delete-orphan")
    certifications = relationship("StudentCertification", back_populates="student", cascade="all, delete-orphan")
    achievements = relationship("StudentAchievement", back_populates="student", cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="student", cascade="all, delete-orphan")
    
    # Mentor assignments linking this student to their mentor(s)
    mentor_assignments = relationship("MentorAssignment", back_populates="student", cascade="all, delete-orphan")

class FacultyProfile(Base):
    __tablename__ = "faculty_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    department = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="faculty_profile")

class MentorAssignment(Base):
    __tablename__ = "mentor_assignments"

    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # User ID of mentor
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)  # Student ID
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    mentor = relationship("User")
    student = relationship("Student", back_populates="mentor_assignments")
