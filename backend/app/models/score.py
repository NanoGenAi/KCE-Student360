from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AssessmentScore(Base):
    __tablename__ = "assessment_scores"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True) # User ID of faculty member
    assessment_name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # DSA, DBMS, FullStack, Aptitude, Coding, Academic, Technical
    score = Column(Float, nullable=False)
    max_marks = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    assessment_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="scores")
    uploader = relationship("User")

class StudentAnalytics(Base):
    __tablename__ = "student_analytics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    overall_score = Column(Float, default=0.0, nullable=False)
    dsa_average = Column(Float, default=0.0, nullable=False)
    dbms_average = Column(Float, default=0.0, nullable=False)
    fullstack_average = Column(Float, default=0.0, nullable=False)
    aptitude_average = Column(Float, default=0.0, nullable=False)
    coding_average = Column(Float, default=0.0, nullable=False)
    academic_average = Column(Float, default=0.0, nullable=False)
    technical_average = Column(Float, default=0.0, nullable=False)
    strongest_domain = Column(String, nullable=True)
    weakest_domain = Column(String, nullable=True)
    total_assessments = Column(Integer, default=0, nullable=False)
    latest_score = Column(Float, default=0.0, nullable=False)
    best_score = Column(Float, default=0.0, nullable=False)
    average_test_score = Column(Float, default=0.0, nullable=False)
    improvement_trend = Column(String, default="Stable", nullable=False)  # Improving, Stable, Needs Attention
    placement_readiness_score = Column(Float, default=0.0, nullable=False)
    placement_readiness_level = Column(String, default="Needs Training", nullable=False) # Placement Ready, Almost Ready, Needs Training
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="analytics")
