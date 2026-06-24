import os
from dotenv import load_dotenv

# Load env file from current or parent directories
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careerpilot.db")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
