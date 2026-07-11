from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class DomainScores(BaseModel):
    DSA: float = 0.0
    DBMS: float = 0.0
    FullStack: float = 0.0
    Aptitude: float = 0.0
    Coding: float = 0.0
    Academic: float = 0.0
    Technical: float = 0.0

class StudentBase(BaseModel):
    id: int
    register_no: str
    registerNo: str
    name: str
    email: str
    phone: Optional[str] = None
    department: str
    year: str
    section: str
    batch: str
    cgpa: float
    profile_image: Optional[str] = None
    profileImage: Optional[str] = None
    overall_score: float = 0.0
    overallScore: float = 0.0
    domain_scores: DomainScores
    domainScores: DomainScores
    strongest_domain: Optional[str] = None
    strongestDomain: Optional[str] = None
    weakest_domain: Optional[str] = None
    weakestDomain: Optional[str] = None

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    register_no: str
    name: str
    email: str
    phone: Optional[str] = None
    department: str
    year: str
    section: str
    batch: str
    cgpa: float = 0.0
    profile_image: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    year: Optional[str] = None
    section: Optional[str] = None
    batch: Optional[str] = None
    cgpa: Optional[float] = None
    profile_image: Optional[str] = None

class StudentAboutSchema(BaseModel):
    headline: Optional[str] = None
    about_me: Optional[str] = None
    aboutMe: Optional[str] = None
    career_objective: Optional[str] = None
    careerObjective: Optional[str] = None
    skills: Optional[List[str]] = None
