import os
import PyPDF2
import docx2txt
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define a set of known skills for matching
KNOWN_SKILLS = {
    "python", "java", "c++", "javascript", "sql", "aws", "flask", "django", "linux",
    "machine learning", "data science", "react", "node.js"
}

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyPDF2"""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        logging.error(f"Error reading PDF {pdf_path}: {e}")
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file"""
    try:
        return docx2txt.process(docx_path)
    except Exception as e:
        logging.error(f"Error reading DOCX {docx_path}: {e}")
        return ""

def extract_skills(text):
    """Extracts skills from text using case-insensitive regex matching"""
    extracted = set()
    for skill in KNOWN_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'  # Ensure full-word matches
        if re.search(pattern, text, re.IGNORECASE):
            extracted.add(skill.lower())
    return list(extracted)

def parse_resume(file_path):
    """Parses the resume and extracts text & skills based on file extension"""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        logging.error(f"Unsupported file format: {ext}")
        return "", []

    if not text.strip():
        logging.warning(f"No text extracted from {file_path}")
        return "", []

    skills = extract_skills(text)
    return text, skills

if __name__ == "__main__":
    resume_file = r"C:\Users\hp\OneDrive\Desktop\Ayush_Resume.pdf"  # Change this to your file path
    text, extracted_skills = parse_resume(resume_file)

    if extracted_skills:
        print("Extracted Skills:", extracted_skills)
    else:
        print("No skills detected.")