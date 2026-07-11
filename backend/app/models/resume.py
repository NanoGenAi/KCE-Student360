from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    resume_title = Column(String, nullable=False)
    preferred_role = Column(String, nullable=True)
    career_objective = Column(Text, nullable=True)
    key_skills_json = Column(Text, nullable=True)  # JSON-encoded array or string representation of skills
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    use_in_portfolio = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="resumes")
