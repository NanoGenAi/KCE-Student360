from pydantic import BaseModel, Field
from typing import List, Optional

class ResumeMetadataUpdate(BaseModel):
    resume_title: Optional[str] = None
    preferred_role: Optional[str] = None
    career_objective: Optional[str] = None
    key_skills: Optional[List[str]] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    use_in_portfolio: Optional[bool] = None

class ResumeResponse(BaseModel):
    id: int
    resume_title: str
    resumeTitle: str
    preferred_role: Optional[str] = None
    preferredRole: Optional[str] = None
    career_objective: Optional[str] = None
    careerObjective: Optional[str] = None
    key_skills: List[str] = Field(default_factory=list)
    keySkills: List[str] = Field(default_factory=list)
    file_name: Optional[str] = None
    fileName: Optional[str] = None
    file_url: Optional[str] = None
    fileUrl: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    use_in_portfolio: bool
    useInPortfolio: bool

    class Config:
        from_attributes = True
