import os
import json
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import engine, Base, get_db
from app import models, schemas
from app.config import UPLOAD_FOLDER
from app.services.resume_parser import parse_and_evaluate_resume
from app.services.gemini_service import generate_career_score_with_gemini, generate_roadmap_with_gemini
from app.services.job_service import get_filtered_jobs, match_resume_with_all_jobs, load_all_jobs
from app.services.optimizer_service import optimize_and_generate_resume

# Create Database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CareerPilot AI Agent API", version="1.0.0")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serves uploaded PDF files statically if needed (for downloading)
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="static")


@app.post("/api/resumes/upload", response_model=schemas.ResumeResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads a PDF resume, parses its text, runs Gemini AI analysis (extracting skills, projects, SWOT, etc.),
    calculates initial career scores, and matches it against sample job openings.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported.")

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save resume file: {e}")

    try:
        # Parse and analyze using resume parser + Gemini
        parsed_data = parse_and_evaluate_resume(file_path, file.filename)

        # Create database entry
        db_resume = models.Resume(
            filename=parsed_data["filename"],
            filepath=parsed_data["filepath"],
            extracted_text=parsed_data["extracted_text"],
            name=parsed_data.get("name"),
            email=parsed_data.get("email"),
            phone=parsed_data.get("phone"),
            skills=parsed_data.get("skills", []),
            education=parsed_data.get("education", []),
            projects=parsed_data.get("projects", []),
            experience=parsed_data.get("experience", []),
            certifications=parsed_data.get("certifications", []),
            achievements=parsed_data.get("achievements", []),
            ats_score=parsed_data.get("ats_score", 0),
            quality_score=parsed_data.get("quality_score", 0),
            strengths=parsed_data.get("strengths", []),
            weaknesses=parsed_data.get("weaknesses", []),
            missing_keywords=parsed_data.get("missing_keywords", []),
            suggestions=parsed_data.get("suggestions", [])
        )
        
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)

        # Precalculate Career Readiness Score
        career_raw = generate_career_score_with_gemini(parsed_data)
        db_career = models.CareerScore(
            resume_id=db_resume.id,
            readiness_score=career_raw.get("readiness_score", 0),
            explanation=career_raw.get("explanation"),
            action_plan=career_raw.get("action_plan", [])
        )
        db.add(db_career)

        # Precalculate Job Matches against all sample jobs
        match_resume_with_all_jobs(db, db_resume.id)
        
        db.commit()
        return db_resume

    except Exception as e:
        # Cleanup uploaded file if anything failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")


@app.post("/api/resumes/use-sample", response_model=schemas.ResumeResponse)
def use_sample_resume(payload: dict, db: Session = Depends(get_db)):
    """
    Simulates uploading a sample resume file by copying it from the data/sample_resumes folder
    and running the parse/analysis pipeline.
    """
    filename = payload.get("filename")
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required.")
        
    sample_dir = os.path.join(os.path.dirname(__file__), "data", "sample_resumes")
    source_path = os.path.join(sample_dir, filename)
    
    if not os.path.exists(source_path):
        raise HTTPException(status_code=404, detail="Sample resume not found.")
        
    dest_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Copy file to uploads folder
    import shutil
    try:
        shutil.copy(source_path, dest_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to copy sample file: {e}")
        
    # Run parsing pipeline
    try:
        parsed_data = parse_and_evaluate_resume(dest_path, filename)
        
        # Create database entry
        db_resume = models.Resume(
            filename=parsed_data["filename"],
            filepath=parsed_data["filepath"],
            extracted_text=parsed_data["extracted_text"],
            name=parsed_data.get("name"),
            email=parsed_data.get("email"),
            phone=parsed_data.get("phone"),
            skills=parsed_data.get("skills", []),
            education=parsed_data.get("education", []),
            projects=parsed_data.get("projects", []),
            experience=parsed_data.get("experience", []),
            certifications=parsed_data.get("certifications", []),
            achievements=parsed_data.get("achievements", []),
            ats_score=parsed_data.get("ats_score", 0),
            quality_score=parsed_data.get("quality_score", 0),
            strengths=parsed_data.get("strengths", []),
            weaknesses=parsed_data.get("weaknesses", []),
            missing_keywords=parsed_data.get("missing_keywords", []),
            suggestions=parsed_data.get("suggestions", [])
        )
        
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)

        # Precalculate Career Readiness Score
        career_raw = generate_career_score_with_gemini(parsed_data)
        db_career = models.CareerScore(
            resume_id=db_resume.id,
            readiness_score=career_raw.get("readiness_score", 0),
            explanation=career_raw.get("explanation"),
            action_plan=career_raw.get("action_plan", [])
        )
        db.add(db_career)

        # Precalculate Job Matches against all sample jobs
        match_resume_with_all_jobs(db, db_resume.id)
        
        db.commit()
        return db_resume
    except Exception as e:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise HTTPException(status_code=500, detail=f"Failed to process sample resume: {e}")


@app.get("/api/resumes/{resume_id}", response_model=schemas.ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the parsed resume analysis by ID.
    """
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@app.get("/api/career-score/{resume_id}", response_model=schemas.CareerScoreResponse)
def get_career_score(resume_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the career readiness evaluation score and action plan checklist.
    """
    score = db.query(models.CareerScore).filter(models.CareerScore.resume_id == resume_id).order_by(models.CareerScore.created_at.desc()).first()
    if not score:
        raise HTTPException(status_code=404, detail="Career score not found for this resume")
    return score


@app.get("/api/jobs")
def list_jobs(
    search: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    work_type: Optional[str] = Query(None),
    role_type: Optional[str] = Query(None),
    fresher_friendly: Optional[bool] = Query(None),
    women_hiring: Optional[bool] = Query(None),
    diversity_hiring: Optional[bool] = Query(None)
):
    """
    Returns filtered lists of jobs from the local JSON dataset.
    """
    return get_filtered_jobs(
        search_query=search,
        location=location,
        work_type=work_type,
        role_type=role_type,
        fresher_friendly=fresher_friendly,
        women_hiring_program=women_hiring,
        diversity_hiring=diversity_hiring
    )


@app.get("/api/jobs/matches/{resume_id}", response_model=List[schemas.JobMatchResponse])
def get_job_matches(resume_id: int, db: Session = Depends(get_db)):
    """
    Retrieves calculated job compatibility scores for the uploaded resume.
    """
    matches = db.query(models.JobMatch).filter(models.JobMatch.resume_id == resume_id).order_by(models.JobMatch.compatibility_score.desc()).all()
    # If no matches exist, attempt to generate them on the fly
    if not matches:
        try:
            matches = match_resume_with_all_jobs(db, resume_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to match jobs: {e}")
    return matches


@app.post("/api/roadmaps", response_model=schemas.RoadmapResponse)
def generate_roadmap(req: schemas.RoadmapRequest, db: Session = Depends(get_db)):
    """
    Generates a personalized 4-month learning roadmap for a target career role.
    """
    # Check if roadmap already exists
    existing = db.query(models.Roadmap).filter(
        models.Roadmap.resume_id == req.resume_id,
        models.Roadmap.target_role.ilike(req.target_role)
    ).first()
    
    if existing:
        return existing

    resume = db.query(models.Resume).filter(models.Resume.id == req.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume_data = {
        "skills": resume.skills or [],
        "education": resume.education or [],
        "projects": resume.projects or [],
        "experience": resume.experience or []
    }

    try:
        roadmap_raw = generate_roadmap_with_gemini(resume_data, req.target_role)
        db_roadmap = models.Roadmap(
            resume_id=req.resume_id,
            target_role=req.target_role,
            roadmap_data=roadmap_raw.get("roadmap", {})
        )
        db.add(db_roadmap)
        db.commit()
        db.refresh(db_roadmap)
        return db_roadmap
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate learning roadmap: {e}")


@app.get("/api/roadmaps/{resume_id}/{target_role}", response_model=schemas.RoadmapResponse)
def get_roadmap(resume_id: int, target_role: str, db: Session = Depends(get_db)):
    """
    Gets generated roadmap for a target role.
    """
    roadmap = db.query(models.Roadmap).filter(
        models.Roadmap.resume_id == resume_id,
        models.Roadmap.target_role.ilike(target_role)
    ).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found for this role")
    return roadmap


@app.post("/api/optimize", response_model=schemas.OptimizeResponse)
def optimize_resume(req: schemas.OptimizeRequest, db: Session = Depends(get_db)):
    """
    Tailors resume to match a specific job description, generating optimized text
    and saving a newly formatted ReportLab PDF on disk.
    """
    try:
        db_opt = optimize_and_generate_resume(
            db=db,
            resume_id=req.resume_id,
            job_id=req.job_id,
            target_role=req.target_role,
            company=req.company,
            job_description=req.job_description
        )
        
        # Build pdf url pointing to the file serving endpoint
        pdf_url = f"/api/optimize/download/{db_opt.id}"
        
        # Return response object manually since db_opt doesn't contain dynamic pdf_url field
        return schemas.OptimizeResponse(
            id=db_opt.id,
            resume_id=db_opt.resume_id,
            job_id=db_opt.job_id,
            target_role=db_opt.target_role,
            company=db_opt.company,
            match_score_before=db_opt.match_score_before,
            match_score_after=db_opt.match_score_after,
            pdf_url=pdf_url,
            optimized_text=db_opt.optimized_text,
            created_at=db_opt.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume optimization failed: {e}")


@app.get("/api/optimize/download/{optimized_id}")
@app.get("/api/optimize/download/{optimized_id}.pdf")
def download_optimized_resume(optimized_id: str, db: Session = Depends(get_db)):
    """
    Serves the tailored/optimized PDF resume file as a downloadable binary attachment.
    """
    print(f"DEBUG: Download endpoint execution triggered for optimized_id: {optimized_id}")
    if optimized_id.endswith(".pdf"):
        optimized_id = optimized_id[:-4]
    try:
        opt_id = int(optimized_id)
    except ValueError:
        print(f"ERROR: Invalid ID format for optimized_id: {optimized_id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    opt = db.query(models.OptimizedResume).filter(models.OptimizedResume.id == opt_id).first()
    if not opt or not opt.pdf_path or not os.path.exists(opt.pdf_path):
        print(f"ERROR: Optimized PDF file not found for ID {opt_id}")
        raise HTTPException(status_code=404, detail="Optimized PDF file not found")
        
    filename = f"optimized_{opt.target_role.replace(' ', '_')}_resume.pdf" if opt.target_role else "optimized_resume.pdf"
    print(f"DEBUG: Serving optimized PDF download path: {opt.pdf_path}, filename: {filename}")
    
    headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\""
    }
    return FileResponse(
        path=opt.pdf_path,
        media_type="application/pdf",
        headers=headers
    )


@app.get("/api/optimize/preview/{optimized_id}")
@app.get("/api/optimize/preview/{optimized_id}.pdf")
def preview_optimized_resume(optimized_id: str, db: Session = Depends(get_db)):
    """
    Serves the tailored/optimized PDF resume file inline for in-browser previewing.
    """
    print(f"DEBUG: Preview endpoint execution triggered for optimized_id: {optimized_id}")
    if optimized_id.endswith(".pdf"):
        optimized_id = optimized_id[:-4]
    try:
        opt_id = int(optimized_id)
    except ValueError:
        print(f"ERROR: Invalid ID format for optimized_id: {optimized_id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    opt = db.query(models.OptimizedResume).filter(models.OptimizedResume.id == opt_id).first()
    if not opt or not opt.pdf_path or not os.path.exists(opt.pdf_path):
        print(f"ERROR: Optimized PDF file not found for ID {opt_id}")
        raise HTTPException(status_code=404, detail="Optimized PDF file not found")
        
    print(f"DEBUG: Serving optimized PDF preview path: {opt.pdf_path}")
    
    headers = {
        "Content-Disposition": "inline"
    }
    return FileResponse(
        path=opt.pdf_path,
        media_type="application/pdf",
        headers=headers
    )


@app.get("/api/resumes/download/{resume_id}")
@app.get("/api/resumes/download/{resume_id}.pdf")
def download_original_resume(resume_id: str, db: Session = Depends(get_db)):
    """
    Serves the original uploaded PDF resume as a downloadable binary attachment.
    """
    print(f"DEBUG: Download endpoint execution triggered for resume_id: {resume_id}")
    if resume_id.endswith(".pdf"):
        resume_id = resume_id[:-4]
    try:
        res_id = int(resume_id)
    except ValueError:
        print(f"ERROR: Invalid ID format for resume_id: {resume_id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    resume = db.query(models.Resume).filter(models.Resume.id == res_id).first()
    if not resume or not resume.filepath or not os.path.exists(resume.filepath):
        print(f"ERROR: Original resume file not found for ID {res_id}")
        raise HTTPException(status_code=404, detail="Original resume file not found")
        
    print(f"DEBUG: Serving original PDF download path: {resume.filepath}, filename: {resume.filename}")
    
    headers = {
        "Content-Disposition": f"attachment; filename=\"{resume.filename or 'original_resume.pdf'}\""
    }
    return FileResponse(
        path=resume.filepath,
        media_type="application/pdf",
        headers=headers
    )


@app.get("/api/resumes/preview/{resume_id}")
@app.get("/api/resumes/preview/{resume_id}.pdf")
def preview_original_resume(resume_id: str, db: Session = Depends(get_db)):
    """
    Serves the original uploaded PDF resume inline for in-browser previewing.
    """
    print(f"DEBUG: Preview endpoint execution triggered for resume_id: {resume_id}")
    if resume_id.endswith(".pdf"):
        resume_id = resume_id[:-4]
    try:
        res_id = int(resume_id)
    except ValueError:
        print(f"ERROR: Invalid ID format for resume_id: {resume_id}")
        raise HTTPException(status_code=400, detail="Invalid ID format")

    resume = db.query(models.Resume).filter(models.Resume.id == res_id).first()
    if not resume or not resume.filepath or not os.path.exists(resume.filepath):
        print(f"ERROR: Original resume file not found for ID {res_id}")
        raise HTTPException(status_code=404, detail="Original resume file not found")
        
    print(f"DEBUG: Serving original PDF preview path: {resume.filepath}")
    
    headers = {
        "Content-Disposition": "inline"
    }
    return FileResponse(
        path=resume.filepath,
        media_type="application/pdf",
        headers=headers
    )


