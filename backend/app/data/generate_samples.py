import os
import sys

# Add backend root to path so we can import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.services.optimizer_service import generate_resume_pdf

# Ensure the output sample resumes directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_resumes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define 5 distinct sample candidates
candidates = [
    {
        "filename": "resume_software_freshman.pdf",
        "data": {
            "name": "Rohan Sharma",
            "email": "rohan.sharma@email.com",
            "phone": "+91-98765-43210",
            "summary": "Passionate Computer Science undergraduate seeking a Software Engineering internship. Strong base in object-oriented programming, data structures, and automation scripting in Python and Java. Eager to collaborate in agile product squads.",
            "skills": ["Python", "Java", "OOP", "Git", "HTML", "CSS", "SQL"],
            "education": [
                {
                    "degree": "B.Tech in Computer Science & Engineering",
                    "school": "IIT Bombay",
                    "year": "2021 - 2025",
                    "gpa": "8.8 / 10"
                }
            ],
            "experience": [
                {
                    "company": "Tech Club IITB",
                    "role": "Frontend Developer Lead",
                    "duration": "May 2023 - Present",
                    "achievements": [
                        "Maintained and optimized the club portal frontend using HTML, CSS, and basic JavaScript.",
                        "Coordinated hackathons and programming competitions for over 500+ participants."
                    ]
                }
            ],
            "projects": [
                {
                    "title": "Personal Budget Tracker CLI",
                    "description": "Command line python application that manages monthly expenses, categories, and logs transaction files on disk.",
                    "technologies": ["Python", "Git", "JSON"]
                }
            ],
            "certifications": ["HackerRank Python (Basic) Certificate", "freeCodeCamp Responsive Web Design"],
            "achievements": ["Ranked 150th in National Coding Olympiad 2022", "Winner of College Innovation Challenge"]
        }
    },
    {
        "filename": "resume_data_analyst.pdf",
        "data": {
            "name": "Priya Patel",
            "email": "priya.patel@email.com",
            "phone": "+91-99887-76655",
            "summary": "Result-oriented Statistics graduate with practical skills in data manipulation, database query optimization, and interactive dashboard creation. Seeking an Associate Data Analyst position to drive business decision-making.",
            "skills": ["Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Pandas"],
            "education": [
                {
                    "degree": "B.Sc (Hons) in Statistics",
                    "school": "Delhi University",
                    "year": "2021 - 2024",
                    "gpa": "9.1 / 10"
                }
            ],
            "experience": [
                {
                    "company": "MarketMetrics Lab",
                    "role": "Data Analyst Intern",
                    "duration": "May 2023 - July 2023",
                    "achievements": [
                        "Queried PostgreSQL databases to clean and structure transaction logs for weekly report assemblies.",
                        "Designed 5 interactive Tableau dashboards visualizing core sales conversions and user retention curves."
                    ]
                }
            ],
            "projects": [
                {
                    "title": "Housing Price Exploratory Analysis",
                    "description": "Cleaned datasets of 5000+ rental records using Pandas/NumPy and built linear regression models predicting pricing trends.",
                    "technologies": ["Python", "Pandas", "Scikit-Learn", "Matplotlib"]
                }
            ],
            "certifications": ["Google Data Analytics Professional Certificate", "Microsoft Power BI Data Analyst Associate"],
            "achievements": ["Academic Excellence Award (Top 2% of class)", "First Prize in Delhi University DataViz Contest"]
        }
    },
    {
        "filename": "resume_web_developer.pdf",
        "data": {
            "name": "Aarav Mehta",
            "email": "aarav.mehta@email.com",
            "phone": "+91-98989-89898",
            "summary": "Enthusiastic Web Developer with a strong focus on React and Next.js ecosystems. Specialized in writing clean TypeScript, configuring responsive layouts using Tailwind, and integrating Rest APIs.",
            "skills": ["JavaScript", "React", "Next.js", "Tailwind CSS", "TypeScript", "HTML", "CSS", "Node.js"],
            "education": [
                {
                    "degree": "B.E. in Information Technology",
                    "school": "VJTI Mumbai",
                    "year": "2020 - 2024",
                    "gpa": "8.5 / 10"
                }
            ],
            "experience": [
                {
                    "company": "Freelance Client Portals",
                    "role": "UI Developer Engineer",
                    "duration": "June 2022 - July 2023",
                    "achievements": [
                        "Built and deployed 5 custom responsive client landing sites using React and Tailwind CSS.",
                        "Optimized image delivery and API payloads, boosting page load speeds by 25%."
                    ]
                }
            ],
            "projects": [
                {
                    "title": "Developer Hub Dashboard",
                    "description": "A centralized project sharing web app allowing developers to post source links and vote on technical posts.",
                    "technologies": ["React", "Tailwind CSS", "Node.js", "Express"]
                }
            ],
            "certifications": ["React Front-End Developer (Meta Professional Certificate)", "Scrimba Frontend Career Path"],
            "achievements": ["VJTI Hackathon Runner-up 2023", "Maintained open-source UI libraries with 10+ pull requests"]
        }
    },
    {
        "filename": "resume_general_science.pdf",
        "data": {
            "name": "Ananya Sen",
            "email": "ananya.sen@email.com",
            "phone": "+91-97777-66666",
            "summary": "Chemistry honors student with excellent analytical mindset and research capabilities. Proficient in executing lab protocols, documenting experimental logs, and using basic Python scripting to analyze Titration telemetry.",
            "skills": ["Python", "MS Excel", "Research", "Data Analysis", "Communication", "Technical Writing"],
            "education": [
                {
                    "degree": "B.Sc in Chemistry",
                    "school": "Presidency University",
                    "year": "2021 - 2024",
                    "gpa": "7.9 / 10"
                }
            ],
            "experience": [
                {
                    "company": "Presidency Chemistry Lab",
                    "role": "Lab Assistant",
                    "duration": "Aug 2023 - Present",
                    "achievements": [
                        "Cataloged daily chemical inventory and experimental titrations in MS Excel spreadsheets.",
                        "Maintained laboratory compliance standards and prepared weekly lab briefs."
                    ]
                }
            ],
            "projects": [
                {
                    "title": "Titration Curve Grapher",
                    "description": "A graphical tkinter application plotting temperature and pH profiles, exporting charts as PDF.",
                    "technologies": ["Python", "Matplotlib", "Tkinter"]
                }
            ],
            "certifications": [],
            "achievements": ["Winner of State Level Science Quiz 2022", "Represented College in Chemistry National Seminar"]
        }
    },
    {
        "filename": "resume_unoptimized.pdf",
        "data": {
            "name": "Rahul Verma",
            "email": "rahul.v@email.com",
            "phone": "+91-96666-55555",
            "summary": "Basic computer graduate. Looking for computer-related jobs like typing, data entry, assistant, or junior programmer. Ready to work hard.",
            "skills": ["Python", "SQL", "MS Office", "Typing"],
            "education": [
                {
                    "degree": "B.Com in Computer Applications",
                    "school": "Osmania University",
                    "year": "2020 - 2023",
                    "gpa": "6.8 / 10"
                }
            ],
            "experience": [
                {
                    "company": "Local Agency Office",
                    "role": "Computer Assistant",
                    "duration": "2022 - 2022",
                    "achievements": [
                        "Helped staff run computers and type documents.",
                        "Ran simple SQL select commands for customers."
                    ]
                }
            ],
            "projects": [
                {
                    "title": "Simple Calculator",
                    "description": "Just a basic calculator app that adds and subtracts variables.",
                    "technologies": ["Python"]
                }
            ],
            "certifications": [],
            "achievements": []
        }
    }
]

def generate_all_samples():
    print("Generating sample resumes...")
    for candidate in candidates:
        filename = candidate["filename"]
        data = candidate["data"]
        filepath = os.path.join(OUTPUT_DIR, filename)
        print(f"Creating {filename} at {filepath}...")
        try:
            generate_resume_pdf(data, filepath)
            print(f"Successfully generated {filename}")
        except Exception as e:
            print(f"Failed to generate {filename}: {e}")
    print("All sample resumes generated successfully!")

if __name__ == "__main__":
    generate_all_samples()
