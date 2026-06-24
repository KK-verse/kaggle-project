import fitz  # PyMuPDF
import pdfplumber
import os
from app.services.gemini_service import parse_resume_with_gemini

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extracts plain text from a PDF file using PyMuPDF, with pdfplumber as a fallback.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Resume file not found at {filepath}")

    text = ""
    
    # Method 1: PyMuPDF (Fast)
    try:
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"PyMuPDF extraction failed for {filepath}: {e}. Trying pdfplumber...")

    # Method 2: pdfplumber (Better structure preservation)
    if not text.strip():
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber extraction failed for {filepath}: {e}")

    # Fallback/Safety Check
    if not text.strip():
        raise ValueError("Could not extract any readable text from the uploaded PDF resume.")

    return text

def parse_and_evaluate_resume(filepath: str, filename: str) -> dict:
    """
    Extracts text from PDF and sends it to Gemini for evaluation.
    """
    raw_text = extract_text_from_pdf(filepath)
    parsed_data = parse_resume_with_gemini(raw_text)
    
    # Inject filename, filepath and raw extracted text
    parsed_data["filename"] = filename
    parsed_data["filepath"] = filepath
    parsed_data["extracted_text"] = raw_text
    
    return parsed_data
