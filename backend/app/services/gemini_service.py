import os
import json
import google.generativeai as genai
from app.config import GEMINI_API_KEY

# Configure Gemini API if key is present
API_KEY_CONFIGURED = False
if GEMINI_API_KEY and GEMINI_API_KEY.strip():
    try:
        genai.configure(api_key=GEMINI_API_KEY.strip())
        API_KEY_CONFIGURED = True
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")

def get_gemini_model():
    if API_KEY_CONFIGURED:
        return genai.GenerativeModel("gemini-2.5-flash")
    return None

def parse_resume_with_gemini(text: str) -> dict:
    """
    Parses resume text and extracts details along with ATS/Quality scores.
    """
    prompt = f"""
    You are an expert technical recruiter and resume writer.
    Analyze the following resume text and extract the information in JSON format.
    Provide scores from 0 to 100 for ATS score and overall Resume Quality, along with SWOT feedback.

    Your output MUST be a valid JSON object matching the following structure:
    {{
        "name": "string or null",
        "email": "string or null",
        "phone": "string or null",
        "skills": ["string"],
        "education": [
            {{
                "school": "string",
                "degree": "string",
                "year": "string",
                "gpa": "string or null"
            }}
        ],
        "projects": [
            {{
                "title": "string",
                "description": "string",
                "technologies": ["string"]
            }}
        ],
        "experience": [
            {{
                "company": "string",
                "role": "string",
                "duration": "string",
                "achievements": ["string"]
            }}
        ],
        "certifications": ["string"],
        "achievements": ["string"],
        "ats_score": 0,
        "quality_score": 0,
        "strengths": ["string"],
        "weaknesses": ["string"],
        "missing_keywords": ["string"],
        "suggestions": ["string"]
    }}

    Resume text to parse:
    \"\"\"{text}\"\"\"
    """
    
    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API Error in parse_resume: {e}. Falling back to mock data.")
            
    # Fallback/Mock parser in case Gemini API is not configured or fails
    return _generate_mock_parse_result(text)


def generate_career_score_with_gemini(resume_data: dict) -> dict:
    """
    Calculates a unique Career Readiness Score (0-100) and creates an action plan.
    """
    prompt = f"""
    You are an elite career mentor.
    Based on the following extracted resume profile, calculate an overall Career Readiness Score (0-100).
    Take into account their current experience, projects, skills, and areas of improvement.
    Explain the score reasoning and provide a concrete action plan checklist to reach 90+.

    Your output MUST be a valid JSON object matching the following structure:
    {{
        "readiness_score": 0,
        "explanation": "string explaining their current industry readiness and why they got this score",
        "action_plan": ["string item detailing specific step they should take"]
    }}

    Resume data:
    {json.dumps(resume_data, indent=2)}
    """
    
    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API Error in career_score: {e}. Falling back to mock data.")

    # Fallback mock generator
    return _generate_mock_career_score(resume_data)


def match_jobs_with_gemini(resume_data: dict, jobs: list) -> list:
    """
    Evaluates compatibility score for multiple jobs and returns detailed reasonings.
    """
    prompt = f"""
    You are an AI-powered job matching agent.
    Compare the following resume data against the list of jobs.
    For each job, calculate a compatibility score (0-100), identify matched and missing skills,
    explain the reasoning, and provide tips on how to improve compatibility.

    Your output MUST be a valid JSON array of objects matching the following structure:
    [
        {{
            "job_id": "string",
            "role": "string",
            "company": "string",
            "compatibility_score": 0,
            "explanation": "string details of why this compatibility score was assigned",
            "matched_skills": ["string"],
            "missing_skills": ["string"],
            "how_to_improve": "string detailing action points to increase compatibility for this specific role"
        }}
    ]

    Resume data:
    {json.dumps(resume_data, indent=2)}

    Jobs list:
    {json.dumps(jobs, indent=2)}
    """
    
    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API Error in job matching: {e}. Falling back to mock data.")

    # Fallback mock generator
    return _generate_mock_job_matching(resume_data, jobs)


def generate_roadmap_with_gemini(resume_data: dict, target_role: str) -> dict:
    """
    Generates a personalized 4-month learning roadmap.
    """
    prompt = f"""
    You are a professional career coach.
    Based on the user's profile and their target role, generate a comprehensive 4-month learning roadmap.
    The roadmap must target their missing skills and guide them step-by-step from Month 1 to Month 4.

    Your output MUST be a valid JSON object matching the following structure:
    {{
        "target_role": "string",
        "roadmap": {{
            "month_1": {{
                "title": "string (e.g. Core Foundations & Basics)",
                "learning_goals": ["string"],
                "milestones": ["string"],
                "resources": ["string (e.g. FreeCodeCamp, Official Documentation, Coursera)"],
                "practice_tasks": ["string"],
                "mini_project": {{
                    "title": "string",
                    "description": "string"
                }}
            }},
            "month_2": {{
                "title": "string",
                "learning_goals": ["string"],
                "milestones": ["string"],
                "resources": ["string"],
                "practice_tasks": ["string"],
                "mini_project": {{
                    "title": "string",
                    "description": "string"
                }}
            }},
            "month_3": {{
                "title": "string",
                "learning_goals": ["string"],
                "milestones": ["string"],
                "resources": ["string"],
                "practice_tasks": ["string"],
                "mini_project": {{
                    "title": "string",
                    "description": "string"
                }}
            }},
            "month_4": {{
                "title": "string",
                "learning_goals": ["string"],
                "milestones": ["string"],
                "resources": ["string"],
                "practice_tasks": ["string"],
                "mini_project": {{
                    "title": "string",
                    "description": "string"
                }}
            }}
        }}
    }}

    Resume data:
    {json.dumps(resume_data, indent=2)}

    Target Role:
    {target_role}
    """
    
    model = get_gemini_model()
    if model:
        try:
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API Error in roadmap: {e}. Falling back to mock data.")

    # Fallback mock generator
    return _generate_mock_roadmap(resume_data, target_role)


def optimize_resume_with_gemini(resume_data: dict, job_description: str, target_role: str) -> dict:
    """
    Optimizes a resume by tailoring experience bullets, adding relevant keywords,
    and suggesting formatting improvements to boost compatibility.
    """
    prompt = f"""
    You are an expert ATS optimization agent and professional resume writer.
    Tailor the user's resume for the provided job description and target role.
    Do not invent fake credentials, but rewrite existing projects and experience descriptions to
    align them with the job requirements and highlight relevant skills.
    
    You should:
    1. Optimize their summary to speak to the company and role.
    2. Rewrite experiences bullet points using the STAR method (Situation, Task, Action, Result) with strong verbs and metrics where possible.
    3. Add important missing keywords that match the job description.
    4. Suggest project reordering if appropriate.
    5. Return an optimized resume JSON alongside original and optimized match scores.

    Your output MUST be a valid JSON object matching the following structure:
    {{
        "match_score_before": 0,
        "match_score_after": 0,
        "optimized_resume": {{
            "name": "string",
            "email": "string",
            "phone": "string",
            "summary": "string - a customized professional summary aligned to the target role",
            "skills": ["string - optimized list of skills"],
            "education": [
                {{
                    "school": "string",
                    "degree": "string",
                    "year": "string",
                    "gpa": "string or null"
                }}
            ],
            "experience": [
                {{
                    "company": "string",
                    "role": "string",
                    "duration": "string",
                    "achievements": ["string - rewritten results-oriented achievements matching job keywords"]
                }}
            ],
            "projects": [
                {{
                    "title": "string",
                    "description": "string - optimized to focus on relevant technologies and impact",
                    "technologies": ["string"]
                }}
            ],
            "certifications": ["string"],
            "achievements": ["string"]
        }}
    }}

    Resume Data:
    {json.dumps(resume_data, indent=2)}

    Target Role:
    {target_role}

    Job Description:
    {job_description}
    """
    
    model = get_gemini_model()
    if model:
        try:
            print("DEBUG: Sending request to Gemini API for resume optimization...")
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            raw_text = response.text
            print(f"DEBUG: Gemini response received. Raw response: {raw_text}")
            
            # Validate JSON parsing
            parsed_json = json.loads(raw_text)
            print("DEBUG: JSON validation success")
            return parsed_json
        except Exception as e:
            print(f"ERROR: Gemini API Error in optimizer: {e}. Falling back to mock optimizer.")

    # Fallback mock generator (only if Gemini is not configured or fails)
    print("DEBUG: Gemini API key not configured or call failed. Falling back to mock optimizer...")
    mock_res = _generate_mock_optimizer(resume_data, job_description, target_role)
    print("DEBUG: JSON validation success (mock data)")
    return mock_res


# --- FALLBACK / MOCK DATA GENERATION FUNCTIONS ---

def _generate_mock_parse_result(text: str) -> dict:
    """Helper to generate details if Gemini fails or is not config'd."""
    # Attempt simple parsing of name/email/phone from text
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    name = lines[0] if len(lines) > 0 else "Applicant Name"
    email = "candidate@example.com"
    phone = "+1-555-0199"
    
    for l in lines[:10]:
        if "@" in l and "." in l:
            email = l.replace("Email:", "").replace("email:", "").strip()
        if any(c.isdigit() for c in l) and ("phone" in l.lower() or "tel" in l.lower() or "+" in l or len(l.replace(" ", "").replace("-", "")) >= 10):
            phone = l.replace("Phone:", "").replace("phone:", "").replace("Mobile:", "").strip()

    text_lower = text.lower()
    
    # 1. Segment text into sections
    sections = {"education": [], "experience": [], "projects": [], "skills": []}
    current_sec = None
    for line in lines:
        l_low = line.lower().strip()
        if not l_low:
            continue
        # Detect headers
        if any(h in l_low for h in ["education", "academic", "study", "studies", "qualification"]):
            current_sec = "education"
        elif any(h in l_low for h in ["experience", "work history", "employment", "professional background", "career"]):
            current_sec = "experience"
        elif any(h in l_low for h in ["project", "key project", "personal project", "portfolio"]):
            current_sec = "projects"
        elif any(h in l_low for h in ["skills", "technical skills", "expertise", "core competencies"]):
            current_sec = "skills"
        elif current_sec and len(line.strip()) > 3:
            sections[current_sec].append(line.strip())

    # 2. Extract Skills
    skills = []
    for line in sections["skills"]:
        delimiters = [",", "|", ";", "•", "·", "/"]
        split_line = [line]
        for d in delimiters:
            new_split = []
            for item in split_line:
                new_split.extend(item.split(d))
            split_line = new_split
        
        for item in split_line:
            cleaned = item.strip().replace(":", "").replace("-", "")
            if 2 <= len(cleaned) <= 30 and not any(h in cleaned.lower() for h in ["skills", "expertise", "proficient"]):
                if cleaned not in skills:
                    skills.append(cleaned)
                    
    # Keyword match from wide pool to augment parsed skills
    skills_pool = [
        "Python", "JavaScript", "TypeScript", "SQL", "HTML", "CSS", "React", "Next.js", "Node.js", 
        "FastAPI", "Flask", "Django", "Docker", "Git", "Java", "C++", "C#", "Machine Learning", "Pandas", 
        "Tableau", "Power BI", "Excel", "Data Analysis", "MongoDB", "PostgreSQL", "AWS",
        "Reservoir Simulation", "Well Logging", "Drilling Engineering", "Production Operations", "Petrel", "Eclipse",
        "CAD (SolidWorks)", "Finite Element Analysis (FEA)", "ANSYS", "MATLAB", "Thermodynamics", "GD&T", "Rapid Prototyping", "AutoCAD",
        "Circuit Design", "Embedded C", "Microcontrollers", "Altium Designer", "Oscilloscopes", "Verilog", "Arduino",
        "Structural Analysis", "Geotechnical Engineering", "Surveying", "Revit", "SAP2000", "Concrete Design",
        "Process Engineering", "Aspen Plus", "Fluid Dynamics", "Chemical Reaction", "Mass Transfer",
        "Bioinformatics", "Biochemistry", "CRISPR", "PCR", "Cell Culture", "Clinical Trials",
        "Financial Modeling", "Corporate Finance", "Valuation", "Project Management", "Marketing", "Salesforce", "Accounting", "Market Research"
    ]
    for sk in skills_pool:
        if sk.lower() in text_lower and sk not in skills:
            skills.append(sk)
            
    if not skills:
        skills = ["Data Analysis", "Project Management", "Excel", "Git"]

    # 3. Extract Education
    school = "University of Technology"
    degree = "B.S. in Engineering/Science"
    year = "2024"
    gpa = "3.7/4.0"
    
    edu_lines = sections["education"] if sections["education"] else lines
    for line in edu_lines:
        l_low = line.lower()
        if any(k in l_low for k in ["bachelor", "b.s.", "b.tech", "master", "m.s.", "ph.d", "mba", "degree", "diploma", "b.e."]):
            degree = line
            if "," in line:
                parts = [p.strip() for p in line.split(",")]
                degree = parts[0]
                for p in parts[1:]:
                    if any(u in p.lower() for u in ["university", "college", "institute", "school", "iit", "nit"]):
                        school = p
                    elif any(c.isdigit() for c in p) and len(p) <= 9:
                        year = p
            break
            
    if school == "University of Technology" or not school:
        for line in edu_lines:
            l_low = line.lower()
            if any(u in l_low for u in ["university", "college", "institute", "school", "iit", "nit"]):
                school = line
                if "," in line:
                    school = line.split(",")[0].strip()
                break

    # 4. Extract Experience
    experience = []
    exp_lines = sections["experience"]
    if exp_lines:
        current_exp = None
        for line in exp_lines:
            l_low = line.lower()
            is_new_header = (
                any(title in l_low for title in ["intern", "engineer", "analyst", "developer", "manager", "associate", "consultant", "lead", "officer"]) or
                any(comp in l_low for comp in ["inc.", "co.", "ltd.", "corp.", "solutions", "group", "technologies", "company", "bank"]) or
                any(dur in l_low for dur in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "present", "2021", "2022", "2023", "2024", "2025"])
            )
            
            if is_new_header and not line.startswith("-") and not line.startswith("•") and not line.startswith("*"):
                if current_exp:
                    experience.append(current_exp)
                role = "Junior Specialist"
                company = "Enterprise Group"
                duration = "June 2023 - Aug 2023"
                
                parts = [p.strip() for p in line.split(",") if p.strip()]
                if len(parts) >= 1:
                    role = parts[0]
                if len(parts) >= 2:
                    company = parts[1]
                if len(parts) >= 3:
                    duration = parts[2]
                
                current_exp = {
                    "company": company,
                    "role": role,
                    "duration": duration,
                    "achievements": []
                }
            elif current_exp:
                clean_ach = line.strip().lstrip("-").lstrip("•").lstrip("*").strip()
                if len(clean_ach) > 10:
                    current_exp["achievements"].append(clean_ach)
                    
        if current_exp:
            experience.append(current_exp)
            
    if not experience:
        role_title = "Graduate Trainee / Intern"
        if "petroleum" in text_lower:
            role_title = "Petroleum Engineering Intern"
        elif "mechanical" in text_lower:
            role_title = "Mechanical Design Intern"
        elif "electrical" in text_lower:
            role_title = "Embedded Systems Intern"
        elif "civil" in text_lower:
            role_title = "Civil Engineering Intern"
        elif "chemical" in text_lower:
            role_title = "Chemical Process Intern"
        elif any(k in text_lower for k in ["finance", "business", "marketing"]):
            role_title = "Business Analyst Intern"
            
        experience = [
            {
                "company": "Industrial Operations Corp",
                "role": role_title,
                "duration": "June 2023 - Present",
                "achievements": [
                    "Analyzed workflow processes and operational telemetry, optimizing execution parameters.",
                    "Collaborated with project managers to draft detailed compliance reports and structural updates."
                ]
            }
        ]

    experience = experience[:2]
    for exp in experience:
        if not exp["achievements"]:
            exp["achievements"] = [
                "Assisted senior engineers/specialists with active project modeling and telemetry collection.",
                "Completed detailed analysis reports and verified compliance standards."
            ]

    # 5. Extract Projects
    projects = []
    proj_lines = sections["projects"]
    if proj_lines:
        current_proj = None
        for line in proj_lines:
            l_low = line.lower()
            is_title = (
                not line.startswith("-") and not line.startswith("•") and not line.startswith("*") and len(line) < 60 and 
                (any(k in l_low for k in ["design", "model", "analysis", "system", "tracker", "simulation", "application", "platform", "tool", "project"]) or len(projects) == 0)
            )
            if is_title:
                if current_proj:
                    projects.append(current_proj)
                current_proj = {
                    "title": line.strip(),
                    "description": "",
                    "technologies": []
                }
            elif current_proj:
                clean_desc = line.strip().lstrip("-").lstrip("•").lstrip("*").strip()
                if not current_proj["description"]:
                    current_proj["description"] = clean_desc
                else:
                    current_proj["description"] += " " + clean_desc
                    
        if current_proj:
            projects.append(current_proj)
            
    for proj in projects:
        proj_text = (proj["title"] + " " + proj["description"]).lower()
        techs = []
        for sk in skills:
            if sk.lower() in proj_text and len(techs) < 4:
                techs.append(sk)
        if not techs:
            techs = skills[:3]
        proj["technologies"] = techs

    if not projects:
        proj_title = "Engineering Analysis & Simulation"
        proj_desc = "Developed an analytical model and conducted simulation studies to optimize process throughput and identify operational bottlenecks."
        proj_techs = skills[:3]
        
        if "petroleum" in text_lower:
            proj_title = "Reservoir Simulation & Recovery Modeling"
            proj_desc = "Developed a numerical simulation to model oil recovery under varying water-flooding strategies using python-based solvers."
            proj_techs = ["Reservoir Simulation", "Excel", "Python"]
        elif "mechanical" in text_lower:
            proj_title = "CAD & Structural Finite Element Analysis"
            proj_desc = "Designed and modeled physical prototype components, validating structural stress distributions with ANSYS software."
            proj_techs = ["CAD (SolidWorks)", "ANSYS", "MATLAB"]
        elif "electrical" in text_lower:
            proj_title = "Embedded Firmware & PCB Design"
            proj_desc = "Designed a low-power microcontroller circuit board to collect and log active analog sensor measurements."
            proj_techs = ["Embedded C", "Altium Designer", "Microcontrollers"]
        elif "civil" in text_lower:
            proj_title = "Structural Concrete Truss Design"
            proj_desc = "Performed structural loading calculations and prepared detailed layout drafts using AutoCAD and Revit."
            proj_techs = ["AutoCAD", "Structural Analysis", "Revit"]
        elif "chemical" in text_lower:
            proj_title = "Chemical Process Flow Simulation"
            proj_desc = "Simulated process flow dynamics and mass transfer characteristics for multi-stage chemical reactions using Aspen Plus."
            proj_techs = ["Process Engineering", "Aspen Plus", "Fluid Dynamics"]
        elif any(k in text_lower for k in ["finance", "business"]):
            proj_title = "Corporate Valuation & Forecast Model"
            proj_desc = "Built a dynamic DCF (Discounted Cash Flow) financial model to forecast corporate earnings and determine equity value."
            proj_techs = ["Financial Modeling", "Excel", "Valuation"]
            
        projects = [
            {
                "title": proj_title,
                "description": proj_desc,
                "technologies": proj_techs
            }
        ]

    projects = projects[:2]
    for proj in projects:
        if not proj["description"]:
            proj["description"] = "Designed, implemented, and tested active prototype components to achieve target operational efficiencies."
        if not proj["technologies"]:
            proj["technologies"] = skills[:3]

    # ATS and Quality Scores
    ats_score = 65
    quality_score = 70
    if len(skills) > 5:
        ats_score += min(15, len(skills))
    if len(experience) > 0:
        quality_score += 10
    if len(projects) > 0:
        quality_score += 10

    ats_score = min(95, max(45, ats_score))
    quality_score = min(95, max(45, quality_score))

    strengths = [
        f"Solid foundational knowledge in {skills[0] if skills else 'engineering core'}",
        "Completed professional projects demonstrating practical implementation",
        "Clear structural presentation of achievements and credentials"
    ]
    
    weaknesses = [
        "Lacks advanced industry certifications in the current profile",
        "Experience achievements could benefit from more metrics-oriented results",
        "Profile lacks some emerging technology keywords relevant to high-match roles"
    ]
    
    suggestions = [
        "Include more measurable metrics (e.g., speed improvements, cost reductions) in achievements.",
        "Obtain a professional certification in your target specialty field.",
        "Deploy or publish your portfolio projects and include links to the active results."
    ]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": [
            {
                "school": school,
                "degree": degree,
                "year": year,
                "gpa": gpa
            }
        ],
        "projects": projects,
        "experience": experience,
        "certifications": ["Professional Field Certificate"],
        "achievements": ["Academic Merit Scholar", "Project Competition Runner-up"],
        "ats_score": ats_score,
        "quality_score": quality_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_keywords": ["Project Management", "Quality Standards", "Analytics Tools"],
        "suggestions": suggestions
    }


def _generate_mock_career_score(resume_data: dict) -> dict:
    skills_count = len(resume_data.get("skills", []))
    exp_count = len(resume_data.get("experience", []))
    proj_count = len(resume_data.get("projects", []))
    
    # Calculate a mock score based on data size
    base = 60
    base += min(15, skills_count * 2)
    base += min(15, exp_count * 5)
    base += min(10, proj_count * 3)
    score = min(95, max(45, base))

    return {
        "readiness_score": score,
        "explanation": f"Your career readiness score is {score}/100. You have a solid starting foundation with {skills_count} core technical skills and {proj_count} listed projects. However, you can make your profile more competitive for target entry-level positions by improving database systems design knowledge and obtaining relevant developer certifications.",
        "action_plan": [
            "Add measurable metrics to internship bullets (e.g., 'improved performance by 15%')",
            "Learn cloud deployments (AWS, Docker) to cover missing infrastructure keywords",
            "Implement one end-to-end full-stack or data engineering project including database integration",
            "Obtain one specialized certification (e.g., Oracle SQL, AWS Developer Associate)"
        ]
    }


def _generate_mock_job_matching(resume_data: dict, jobs: list) -> list:
    res = []
    user_skills = set(s.lower() for s in resume_data.get("skills", []))
    
    for job in jobs:
        req_skills = job.get("required_skills", [])
        matched = [s for s in req_skills if s.lower() in user_skills]
        missing = [s for s in req_skills if s.lower() not in user_skills]
        
        # Calculate compatibility score
        if req_skills:
            pct = int((len(matched) / len(req_skills)) * 100)
            score = max(35, min(98, pct))
        else:
            score = 70
            
        # Tweak score based on role title match
        role_lower = job.get("title", "").lower()
        skills_str = " ".join(resume_data.get("skills", [])).lower()
        if "data" in role_lower and "python" in skills_str and "sql" in skills_str:
            score = max(score, 78)
        if "software" in role_lower and ("javascript" in skills_str or "java" in skills_str or "python" in skills_str):
            score = max(score, 80)
        if "petroleum" in role_lower and ("reservoir" in skills_str or "well logging" in skills_str or "drilling" in skills_str or "excel" in skills_str):
            score = max(score, 85)
        if "mechanical" in role_lower and ("cad" in skills_str or "solidworks" in skills_str or "ansys" in skills_str or "fea" in skills_str):
            score = max(score, 85)
        if "embedded" in role_lower and ("embedded c" in skills_str or "circuit" in skills_str or "microcontroller" in skills_str or "altium" in skills_str):
            score = max(score, 85)

        res.append({
            "job_id": job.get("id", "job_1"),
            "role": job.get("title", "Role"),
            "company": job.get("company", "Company"),
            "compatibility_score": score,
            "explanation": f"You match {len(matched)} of the {len(req_skills)} key technical requirements for this role. Your background in {' and '.join(matched[:2]) if matched else 'general software'} fits well with the team structure, but you need to bridge the gap in missing tools.",
            "matched_skills": matched,
            "missing_skills": missing,
            "how_to_improve": f"To optimize your profile for {job.get('title')}, add a dedicated section demonstrating expertise in {', '.join(missing[:3]) if missing else 'advanced concepts'} and update your resume summary to align with the core focus of {job.get('company')}."
        })
        
    return sorted(res, key=lambda x: x["compatibility_score"], reverse=True)


def _generate_mock_roadmap(resume_data: dict, target_role: str) -> dict:
    return {
        "target_role": target_role,
        "roadmap": {
            "month_1": {
                "title": "Foundational Mastery & Environment Setup",
                "learning_goals": [
                    f"Master core principles of {target_role}",
                    "Deepen understanding of databases and SQL",
                    "Study basic patterns and system configurations"
                ],
                "milestones": [
                    "Complete basic tutorials and online modules",
                    "Design and launch a local database project"
                ],
                "resources": [
                    "FreeCodeCamp SQL and Python Core tutorials",
                    "Official PostgreSQL Documentation",
                    "W3Schools Database tutorials"
                ],
                "practice_tasks": [
                    "Write 20+ complex SQL queries (joins, subqueries, group by)",
                    "Create database relational schemas for a library or store application"
                ],
                "mini_project": {
                    "title": "Relational DB Schema & API Setup",
                    "description": "Create a fully documented database schema and configure a local service to insert/fetch data using SQL scripts."
                }
            },
            "month_2": {
                "title": "Backend Engineering & Frameworks",
                "learning_goals": [
                    "Build RESTful APIs with python-based backend frameworks",
                    "Learn about request-response cycles, middleware, and routers",
                    "Implement basic schema validations"
                ],
                "milestones": [
                    "Launch a local server backend and connect it to a database layer",
                    "Write unit tests for APIs"
                ],
                "resources": [
                    "FastAPI Official Tutorial Guide",
                    "Corey Schafer YouTube Programming Tutorials",
                    "TestDriven.io FastAPI courses"
                ],
                "practice_tasks": [
                    "Create a CRUD endpoint structure for a task management app",
                    "Write unit tests with Pytest covering edge cases"
                ],
                "mini_project": {
                    "title": "Secure CRUD Backend API",
                    "description": "A working REST API backend with full validation, database integration, and high unit test coverage."
                }
            },
            "month_3": {
                "title": "Containerization & Cloud Basics",
                "learning_goals": [
                    "Understand containerization principles using Docker",
                    "Learn basic AWS cloud services (S3, EC2)",
                    "Set up containerized deployments"
                ],
                "milestones": [
                    "Dockerize your local backend application",
                    "Run containerized apps locally and push images to a repository"
                ],
                "resources": [
                    "Docker official getting started guide",
                    "AWS Free Tier Workshops",
                    "TechWorld with Nana Docker Tutorials"
                ],
                "practice_tasks": [
                    "Write a Dockerfile and docker-compose.yml for your backend + database",
                    "Deploy a simple containerized site on a free hosting platform"
                ],
                "mini_project": {
                    "title": "Dockerized Multi-Container Application",
                    "description": "Set up a multi-container local stack utilizing Docker Compose to coordinate a FastAPI web server, PostgreSQL database, and Redis cache."
                }
            },
            "month_4": {
                "title": "CI/CD & Final Capstone Project",
                "learning_goals": [
                    "Configure automated deployment pipelines (GitHub Actions)",
                    "Optimize system performance (indexing, query caching)",
                    "Refine resume with the new skill set and portfolio links"
                ],
                "milestones": [
                    "Have a fully deployed live capstone project with automated CI/CD checks",
                    "Share resume with target networks and apply for active matching roles"
                ],
                "resources": [
                    "GitHub Actions Documentation",
                    "System Design Primer by Donne Martin",
                    "Resume templates and formatting guides"
                ],
                "practice_tasks": [
                    "Set up GitHub Actions to run tests and linter on every git push",
                    "Conduct peer reviews or mock interview coding runs"
                ],
                "mini_project": {
                    "title": "Production-Ready Analytics Platform",
                    "description": "A fully deployed system with continuous integration, responsive dashboards, automated checks, and rich metrics."
                }
            }
        }
    }


def _generate_mock_optimizer(resume_data: dict, job_description: str, target_role: str) -> dict:
    user_skills = resume_data.get("skills", [])
    
    # Identify some keywords from job description to inject
    jd_lower = job_description.lower()
    keywords_to_add = []
    potential_keywords = ["docker", "kubernetes", "ci/cd", "postgresql", "redis", "aws", "gcp", "agile", "jira", "unit testing"]
    for pk in potential_keywords:
        if pk in jd_lower and pk not in [s.lower() for s in user_skills]:
            keywords_to_add.append(pk.title())
            
    if not keywords_to_add:
        keywords_to_add = ["Docker", "Agile Methodologies", "Unit Testing"]

    optimized_skills = list(set(user_skills + keywords_to_add))
    
    # Tailor summary
    name = resume_data.get("name") or "Professional Candidate"
    summary = f"Motivated and detail-oriented technical professional with expertise in {', '.join(user_skills[:3])}. Proven ability to build clean web backends, optimize query routines, and implement structured code testing. Seeking to leverage skills in {', '.join(keywords_to_add[:2])} to excel as a {target_role}."

    # Tailor experience achievements
    optimized_exp = []
    for exp in resume_data.get("experience", []):
        achievements = exp.get("achievements", [])
        tailored_achievements = [
            f"Designed and optimized core service routines using {target_role} concepts, aligning system functions with technical workflows.",
            f"Boosted response efficiency by incorporating industry best practices, resulting in cleaner and more modular codebase.",
        ]
        if achievements:
            tailored_achievements[0] = f"Refined backend components using target keywords, delivering reliable system operations and increasing data throughput."
            if len(achievements) > 1:
                tailored_achievements[1] = f"Spearheaded database query refactoring, which enhanced execution speeds and decreased server query latency."
        
        optimized_exp.append({
            "company": exp.get("company"),
            "role": exp.get("role"),
            "duration": exp.get("duration"),
            "achievements": tailored_achievements
        })

    # Tailor projects
    optimized_proj = []
    for proj in resume_data.get("projects", []):
        optimized_proj.append({
            "title": proj.get("title"),
            "description": f"Developed an advanced {proj.get('title')} project utilizing {', '.join(proj.get('technologies', [])[:3])}. Optimized API routing schemas to resolve query bottlenecks.",
            "technologies": list(set(proj.get("technologies", []) + [keywords_to_add[0]] if keywords_to_add else proj.get("technologies", [])))
        })

    return {
        "match_score_before": resume_data.get("ats_score", 70),
        "match_score_after": max(92, min(99, resume_data.get("ats_score", 70) + 15)),
        "optimized_resume": {
            "name": name,
            "email": resume_data.get("email"),
            "phone": resume_data.get("phone"),
            "summary": summary,
            "skills": optimized_skills,
            "education": resume_data.get("education", []),
            "experience": optimized_exp,
            "projects": optimized_proj,
            "certifications": resume_data.get("certifications", []),
            "achievements": resume_data.get("achievements", [])
        }
    }
