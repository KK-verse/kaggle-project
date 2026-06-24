import os
import sys

# Add backend directory root to path
sys.path.append(os.path.dirname(__file__))

from app.database import engine, Base, SessionLocal
from app.services.resume_parser import parse_and_evaluate_resume
from app.services.optimizer_service import optimize_and_generate_resume
from app.models import Resume, CareerScore, JobMatch, OptimizedResume

def run_test():
    print("--------------------------------------------------")
    print("Starting CareerPilot Backend Service Tests...")
    print("--------------------------------------------------")
    
    print("1. Creating database tables in SQLite...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Run sample PDF generation
    print("2. Generating sample resume PDF files...")
    import app.data.generate_samples as gs
    gs.generate_all_samples()
    
    sample_dir = os.path.join(os.path.dirname(__file__), "app", "data", "sample_resumes")
    sample_file = os.path.join(sample_dir, "resume_software_freshman.pdf")
    
    if not os.path.exists(sample_file):
        print(f"Error: Sample file not found at {sample_file}")
        return
        
    print(f"3. Testing PDF text extraction and AI parsing on: {sample_file}")
    try:
        parsed_data = parse_and_evaluate_resume(sample_file, "resume_software_freshman.pdf")
        print("SUCCESS: Resume parsed successfully!")
        print(f"   Candidate Name: {parsed_data.get('name')}")
        print(f"   Skills Extracted: {parsed_data.get('skills')}")
        print(f"   ATS Score: {parsed_data.get('ats_score')}/100")
        
        # Test DB insertion
        print("4. Saving candidate profile to SQLite 'resumes' table...")
        db_resume = Resume(
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
        print(f"SUCCESS: Profile stored. Assigned Resume ID: {db_resume.id}")
        
        # Test Career Readiness Score
        print("5. Evaluating Career Readiness Score & Recommendations...")
        from app.services.gemini_service import generate_career_score_with_gemini
        career_raw = generate_career_score_with_gemini(parsed_data)
        db_career = CareerScore(
            resume_id=db_resume.id,
            readiness_score=career_raw.get("readiness_score", 0),
            explanation=career_raw.get("explanation"),
            action_plan=career_raw.get("action_plan", [])
        )
        db.add(db_career)
        db.commit()
        print(f"SUCCESS: Career readiness analysis complete. Score: {db_career.readiness_score}/100")
        
        # Test Job Matching
        print("6. Matching profile against local jobs dataset (jobs.json)...")
        from app.services.job_service import match_resume_with_all_jobs
        matches = match_resume_with_all_jobs(db, db_resume.id)
        print(f"SUCCESS: Job match calculations complete. Found {len(matches)} matches.")
        if matches:
            print(f"   Top Fit: {matches[0].role} at {matches[0].company} ({matches[0].compatibility_score}% compatibility)")
        
        # Test Optimization
        print("7. Tailoring resume for custom Job Description...")
        jd = "We need a Software Engineer who knows Python, SQL, and Docker. Must design and implement backend REST services and perform unit testing."
        db_opt = optimize_and_generate_resume(
            db=db,
            resume_id=db_resume.id,
            job_id="job_1",
            target_role="Software Engineer",
            company="TechCorp Solutions",
            job_description=jd
        )
        print(f"SUCCESS: Resume optimization complete.")
        print(f"   ATS Match Score: Before = {db_opt.match_score_before}% | After = {db_opt.match_score_after}%")
        print(f"   Optimized PDF compiled at: {db_opt.pdf_path}")
        
        print("--------------------------------------------------")
        print("SUCCESS: All Backend Service Tests Passed!")
        print("--------------------------------------------------")
        
    except Exception as e:
        print("--------------------------------------------------")
        print(f"ERROR: Backend service tests failed: {e}")
        print("--------------------------------------------------")
    finally:
        db.close()

if __name__ == "__main__":
    run_test()
