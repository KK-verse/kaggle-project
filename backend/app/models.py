from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(512), nullable=False)
    extracted_text = Column(Text, nullable=False)
    
    # Personal Info (extracted)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    
    # Resume content structures (stored as JSON lists/objects)
    skills = Column(JSON, nullable=True)            # ["Python", "SQL"]
    education = Column(JSON, nullable=True)         # [{"school": "X", "degree": "Y", "year": "Z", "gpa": "A"}]
    projects = Column(JSON, nullable=True)          # [{"title": "X", "description": "Y", "technologies": ["Z"]}]
    experience = Column(JSON, nullable=True)        # [{"company": "X", "role": "Y", "duration": "Z", "achievements": ["A"]}]
    certifications = Column(JSON, nullable=True)    # ["Cert 1", "Cert 2"]
    achievements = Column(JSON, nullable=True)      # ["Achievement 1"]
    
    # Evaluation Scores
    ats_score = Column(Integer, default=0)
    quality_score = Column(Integer, default=0)
    
    # Evaluation Feedback (JSON lists)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    missing_keywords = Column(JSON, nullable=True)
    suggestions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CareerScore(Base):
    __tablename__ = "career_scores"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    readiness_score = Column(Integer, default=0)
    explanation = Column(Text, nullable=True)
    action_plan = Column(JSON, nullable=True)       # ["Action item 1", "Action item 2"]
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(50), nullable=False)
    role = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    compatibility_score = Column(Integer, default=0)
    explanation = Column(Text, nullable=True)
    matched_skills = Column(JSON, nullable=True)    # ["Python", "SQL"]
    missing_skills = Column(JSON, nullable=True)    # ["Pandas", "PySpark"]
    how_to_improve = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    target_role = Column(String(255), nullable=False)
    roadmap_data = Column(JSON, nullable=False)      # Detailed months structure: {"Month 1": {...}}
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OptimizedResume(Base):
    __tablename__ = "optimized_resumes"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(50), nullable=True)
    target_role = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=False)
    optimized_text = Column(JSON, nullable=False)     # Tailored resume content: contact, summary, bullet points
    pdf_path = Column(String(512), nullable=True)
    match_score_before = Column(Integer, default=0)
    match_score_after = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
