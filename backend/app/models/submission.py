from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class StudentProject(Base):
    __tablename__ = "student_projects"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(String, nullable=False)  # Comma-separated or string format
    role = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    live_demo_link = Column(String, nullable=True)
    proof_file = Column(String, nullable=True)
    status = Column(String, default="Pending", nullable=False)  # Pending, Approved, Rejected, Correction Required
    mentor_feedback = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="projects")
    reviewer = relationship("User")

class StudentCertification(Base):
    __tablename__ = "student_certifications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    issuer = Column(String, nullable=False)
    credential_id = Column(String, nullable=True)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    certificate_link = Column(String, nullable=True)
    proof_file = Column(String, nullable=True)
    status = Column(String, default="Pending", nullable=False)  # Pending, Approved, Rejected, Correction Required
    mentor_feedback = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="certifications")
    reviewer = relationship("User")

class StudentAchievement(Base):
    __tablename__ = "student_achievements"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    achievement_type = Column(String, nullable=False)  # Hackathon, Contest, Academic, Sports, etc.
    organization = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    achievement_date = Column(Date, nullable=False)
    proof_link = Column(String, nullable=True)
    proof_file = Column(String, nullable=True)
    status = Column(String, default="Pending", nullable=False)  # Pending, Approved, Rejected, Correction Required
    mentor_feedback = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="achievements")
    reviewer = relationship("User")

class MentorReviewLog(Base):
    __tablename__ = "mentor_review_logs"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String, nullable=False)  # project, certification, achievement
    item_id = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    feedback = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    student = relationship("Student")
    mentor = relationship("User")
