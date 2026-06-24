import os
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.models import Resume, OptimizedResume
from app.services.gemini_service import optimize_resume_with_gemini
from app.config import UPLOAD_FOLDER

def generate_resume_pdf(resume_data: dict, output_path: str):
    """
    Programmatically creates a beautiful, professional PDF resume using ReportLab.
    """
    # 0.5-inch margins (36 points) or 40 points
    doc = SimpleDocTemplate(
        output_path, 
        pagesize=letter,
        rightMargin=40, 
        leftMargin=40,
        topMargin=40, 
        bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styling definitions
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A202C"),
        alignment=1  # Centered
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#4A5568"),
        alignment=1  # Centered
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e3a8a"),  # Indigo-900 / Deep Navy Accent
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748")
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    # 1. Header (Name, Contact Info)
    name = resume_data.get("name", "Applicant Name") or "Applicant Name"
    story.append(Paragraph(name, name_style))
    story.append(Spacer(1, 3))
    
    email = resume_data.get("email") or ""
    phone = resume_data.get("phone") or ""
    contact_items = [item for item in [email, phone] if item]
    contact_text = "  |  ".join(contact_items)
    if contact_text:
        story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 8))
    
    def add_divider_header(title: str):
        story.append(Paragraph(title, section_heading))
        # Thin divider line using a ReportLab Table
        line = Table([[""]], colWidths=[532], rowHeights=[1.2])
        line.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#CBD5E0")),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(line)
        story.append(Spacer(1, 4))
        
    # 2. Professional Summary
    summary = resume_data.get("summary")
    if summary:
        add_divider_header("PROFESSIONAL SUMMARY")
        story.append(Paragraph(summary, body_style))
        story.append(Spacer(1, 6))
        
    # 3. Core Skills
    skills = resume_data.get("skills")
    if skills:
        add_divider_header("TECHNICAL SKILLS")
        skills_str = ", ".join(skills)
        story.append(Paragraph(skills_str, body_style))
        story.append(Spacer(1, 6))
        
    # 4. Professional Experience
    experience = resume_data.get("experience")
    if experience:
        add_divider_header("PROFESSIONAL EXPERIENCE")
        for exp in experience:
            role = exp.get("role", "Software Engineer")
            company = exp.get("company", "Company")
            duration = exp.get("duration", "")
            
            header_text = f"<b>{role}</b> at <i>{company}</i>"
            exp_table = Table(
                [[Paragraph(header_text, body_style), Paragraph(duration, ParagraphStyle('RightAlign', parent=body_style, alignment=2))]], 
                colWidths=[380, 152]
            )
            exp_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
            ]))
            story.append(exp_table)
            
            for achievement in exp.get("achievements", []):
                story.append(Paragraph(f"&bull; {achievement}", bullet_style))
            story.append(Spacer(1, 4))
            
    # 5. Selected Projects
    projects = resume_data.get("projects")
    if projects:
        add_divider_header("PROJECTS & PORTFOLIO")
        for proj in projects:
            title = proj.get("title", "Project")
            techs = ", ".join(proj.get("technologies", []))
            desc = proj.get("description", "")
            
            proj_header = f"<b>{title}</b>"
            if techs:
                proj_header += f" (<i>{techs}</i>)"
                
            story.append(Paragraph(proj_header, body_style))
            story.append(Paragraph(f"&bull; {desc}", bullet_style))
            story.append(Spacer(1, 4))
            
    # 6. Education
    education = resume_data.get("education")
    if education:
        add_divider_header("EDUCATION")
        for edu in education:
            degree = edu.get("degree", "Degree")
            school = edu.get("school", "School")
            year = edu.get("year", "")
            gpa = edu.get("gpa")
            
            edu_text = f"<b>{degree}</b> - {school}"
            if gpa:
                edu_text += f" (GPA: {gpa})"
                
            edu_table = Table(
                [[Paragraph(edu_text, body_style), Paragraph(year, ParagraphStyle('RightAlign', parent=body_style, alignment=2))]], 
                colWidths=[420, 112]
            )
            edu_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
                ('TOPPADDING', (0,0), (-1,-1), 1),
            ]))
            story.append(edu_table)
            story.append(Spacer(1, 2))
            
    # 7. Certifications
    certs = resume_data.get("certifications")
    if certs:
        add_divider_header("CERTIFICATIONS")
        certs_str = ", ".join(certs)
        story.append(Paragraph(certs_str, body_style))
        story.append(Spacer(1, 4))

    # 8. Achievements
    achievements = resume_data.get("achievements")
    if achievements:
        add_divider_header("ACHIEVEMENTS")
        for ach in achievements:
            story.append(Paragraph(f"&bull; {ach}", bullet_style))

    # Build the document
    try:
        doc.build(story)
        print("DEBUG: ReportLab compilation success")
    except Exception as e:
        print(f"ERROR: ReportLab compilation failed: {e}")
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"ReportLab compilation failed: {str(e)}") from e

    # Post-generation validations
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Generated PDF not found on disk at {output_path}")

    file_size = os.path.getsize(output_path)
    print(f"DEBUG: PDF file size: {file_size} bytes")
    print(f"DEBUG: PDF save path: {output_path}")

    if file_size == 0:
        raise ValueError("Generated PDF file is empty (0 bytes).")

    # Verify %PDF- signature
    with open(output_path, "rb") as f:
        signature = f.read(5)
        if signature != b"%PDF-":
            raise ValueError(f"Invalid PDF signature: {signature}. The generated file is not a valid PDF.")
    print("DEBUG: PDF signature validation success")

    # Programmatic opening check using PyMuPDF (fitz)
    try:
        import fitz
        doc_check = fitz.open(output_path)
        pages = doc_check.page_count
        doc_check.close()
        print(f"DEBUG: PDF validation result: Success (Pages: {pages})")
    except Exception as val_err:
        raise RuntimeError(f"Programmatic PDF validation failed: {str(val_err)}") from val_err



def optimize_and_generate_resume(
    db: Session, 
    resume_id: int, 
    job_id: str, 
    target_role: str, 
    company: str, 
    job_description: str
) -> OptimizedResume:
    """
    Optimizes the active resume for a specific role and compiles it into a PDF.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise ValueError(f"Resume with ID {resume_id} not found.")

    # Reformat resume database columns to dict representation
    resume_data = {
        "name": resume.name,
        "email": resume.email,
        "phone": resume.phone,
        "skills": resume.skills or [],
        "education": resume.education or [],
        "projects": resume.projects or [],
        "experience": resume.experience or [],
        "certifications": resume.certifications or [],
        "achievements": resume.achievements or [],
        "ats_score": resume.ats_score
    }

    # Run AI Optimization
    opt_result = optimize_resume_with_gemini(resume_data, job_description, target_role)

    # Save to db
    optimized_text = opt_result.get("optimized_resume", {})
    match_score_before = opt_result.get("match_score_before", resume.ats_score)
    match_score_after = opt_result.get("match_score_after", 90)

    # Generate filename and path
    pdf_filename = f"optimized_{resume_id}_{job_id or 'custom'}.pdf"
    pdf_filepath = os.path.join(UPLOAD_FOLDER, pdf_filename)

    # Compile PDF
    generate_resume_pdf(optimized_text, pdf_filepath)

    # Delete existing optimized records for same target job/resume
    db.query(OptimizedResume).filter(
        OptimizedResume.resume_id == resume_id,
        OptimizedResume.job_id == job_id
    ).delete()

    db_opt = OptimizedResume(
        resume_id=resume_id,
        job_id=job_id,
        target_role=target_role,
        company=company,
        job_description=job_description,
        optimized_text=optimized_text,
        pdf_path=pdf_filepath,
        match_score_before=match_score_before,
        match_score_after=match_score_after
    )
    
    db.add(db_opt)
    db.commit()
    db.refresh(db_opt)

    return db_opt
