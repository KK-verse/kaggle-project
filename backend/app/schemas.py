from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# Resume Schemas
class ResumeBase(BaseModel):
    filename: str
    filepath: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    education: Optional[List[Dict[str, Any]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    ats_score: int = 0
    quality_score: int = 0
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    missing_keywords: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None

class ResumeCreate(ResumeBase):
    extracted_text: str

class ResumeResponse(ResumeBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# CareerScore Schemas
class CareerScoreResponse(BaseModel):
    id: int
    resume_id: int
    readiness_score: int
    explanation: Optional[str] = None
    action_plan: Optional[List[str]] = None
    created_at: datetime
    class Config:
        from_attributes = True


# JobMatch Request/Response
class JobMatchRequest(BaseModel):
    resume_id: int

class JobMatchResponse(BaseModel):
    id: int
    resume_id: int
    job_id: str
    role: str
    company: str
    compatibility_score: int
    explanation: Optional[str] = None
    matched_skills: Optional[List[str]] = None
    missing_skills: Optional[List[str]] = None
    how_to_improve: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True


# Roadmap Request/Response
class RoadmapRequest(BaseModel):
    resume_id: int
    target_role: str

class RoadmapResponse(BaseModel):
    id: int
    resume_id: int
    target_role: str
    roadmap_data: Dict[str, Any]
    created_at: datetime
    class Config:
        from_attributes = True


# Optimize Request/Response
class OptimizeRequest(BaseModel):
    resume_id: int
    job_id: Optional[str] = None
    target_role: str
    company: str
    job_description: str

class OptimizeResponse(BaseModel):
    id: int
    resume_id: int
    job_id: Optional[str] = None
    target_role: str
    company: str
    match_score_before: int
    match_score_after: int
    pdf_url: str
    optimized_text: Dict[str, Any]
    created_at: datetime
    class Config:
        from_attributes = True
