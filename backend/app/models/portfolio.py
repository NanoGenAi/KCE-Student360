from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PortfolioCustomization(Base):
    __tablename__ = "portfolio_customizations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    headline = Column(String, nullable=True)
    about_me = Column(Text, nullable=True)
    career_objective = Column(Text, nullable=True)
    skills_json = Column(Text, nullable=True)  # JSON list of customized skills
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    theme = Column(String, default="Dark Minimal", nullable=False)
    section_visibility_json = Column(Text, nullable=True)  # JSON configuration for visibility switches
    resume_visibility = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="portfolio_customization")
