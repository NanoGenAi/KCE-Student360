from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AISummary(Base):
    __tablename__ = "ai_summaries"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    summary = Column(Text, nullable=False)
    strengths_json = Column(Text, nullable=True)  # JSON-encoded array of strengths
    weaknesses_json = Column(Text, nullable=True)  # JSON-encoded array of weaknesses
    recommendations_json = Column(Text, nullable=True)  # JSON-encoded array of recommendations
    placement_advice = Column(Text, nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="ai_summary")
