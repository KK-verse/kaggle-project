import os
import json
from sqlalchemy.orm import Session
from app.models import Resume, JobMatch
from app.services.gemini_service import match_jobs_with_gemini

JOBS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.json")

def load_all_jobs() -> list:
    """
    Loads all sample jobs from the local JSON dataset.
    """
    if not os.path.exists(JOBS_FILE_PATH):
        return []
    try:
        with open(JOBS_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading jobs.json: {e}")
        return []

def get_filtered_jobs(
    search_query: str = None,
    location: str = None,
    work_type: str = None,
    role_type: str = None,
    fresher_friendly: bool = None,
    women_hiring_program: bool = None,
    diversity_hiring: bool = None
) -> list:
    """
    Filters the sample jobs based on search inputs and filter tags.
    """
    jobs = load_all_jobs()
    filtered = []
    
    for job in jobs:
        # Search query check (title, company, description, skills)
        if search_query:
            query = search_query.lower()
            match_found = (
                query in job.get("title", "").lower() or
                query in job.get("company", "").lower() or
                query in job.get("description", "").lower() or
                any(query in s.lower() for s in job.get("required_skills", []))
            )
            if not match_found:
                continue
                
        # Location filter
        if location and location.lower() != "all" and job.get("location", "").lower() != location.lower():
            continue
            
        # Work type (Remote/Hybrid/Onsite) filter
        if work_type and work_type.lower() != "all" and job.get("work_type", "").lower() != work_type.lower():
            continue
            
        # Role type (Full-Time/Internship) filter
        if role_type and role_type.lower() != "all" and job.get("role_type", "").lower() != role_type.lower():
            continue
            
        # Fresher friendly filter
        if fresher_friendly is not None and fresher_friendly and not job.get("fresher_friendly", False):
            continue
            
        # Women hiring filter
        if women_hiring_program is not None and women_hiring_program and not job.get("women_hiring_program", False):
            continue
            
        # Diversity hiring filter
        if diversity_hiring is not None and diversity_hiring and not job.get("diversity_hiring", False):
            continue
            
        filtered.append(job)
        
    return filtered

def match_resume_with_all_jobs(db: Session, resume_id: int) -> list:
    """
    Compares the resume against all jobs in the database.
    Saves/updates results in SQLite job_matches table.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise ValueError(f"Resume with ID {resume_id} not found.")

    jobs = load_all_jobs()
    if not jobs:
        return []

    # Map resume fields to a clean dict for Gemini
    resume_data = {
        "skills": resume.skills or [],
        "education": resume.education or [],
        "projects": resume.projects or [],
        "experience": resume.experience or [],
        "certifications": resume.certifications or [],
        "ats_score": resume.ats_score,
        "quality_score": resume.quality_score
    }

    # Call Gemini match service
    matches_results = match_jobs_with_gemini(resume_data, jobs)

    # Delete existing matches for this resume
    db.query(JobMatch).filter(JobMatch.resume_id == resume_id).delete()

    # Save new matches
    db_matches = []
    for item in matches_results:
        db_match = JobMatch(
            resume_id=resume_id,
            job_id=item.get("job_id"),
            role=item.get("role"),
            company=item.get("company"),
            compatibility_score=item.get("compatibility_score", 0),
            explanation=item.get("explanation"),
            matched_skills=item.get("matched_skills", []),
            missing_skills=item.get("missing_skills", []),
            how_to_improve=item.get("how_to_improve")
        )
        db.add(db_match)
        db_matches.append(db_match)
        
    db.commit()
    for m in db_matches:
        db.refresh(m)
        
    return db_matches
