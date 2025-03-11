import os
import pdfplumber
import docx2txt
import logging
import json
import re
from rapidfuzz import process, fuzz

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load skills from JSON file
SKILLS_LIST = set()
SKILLS_FILE = os.path.join(os.path.dirname(__file__), "skills.json")

if os.path.exists(SKILLS_FILE):
    try:
        with open(SKILLS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "skills" in data and isinstance(data["skills"], list):
                SKILLS_LIST = set(map(str.lower, data["skills"]))
            else:
                logging.error("Invalid format in skills.json: Expected a list under 'skills' key.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON: Check skills.json format.")
else:
    logging.error(f"File not found: {SKILLS_FILE}")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        logging.error(f"Error reading PDF {pdf_path}: {e}")
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        return docx2txt.process(docx_path).strip()
    except Exception as e:
        logging.error(f"Error reading DOCX {docx_path}: {e}")
        return ""

def extract_skills(text):
    """Extracts skills using fuzzy matching with rapidfuzz."""
    if not SKILLS_LIST:
        logging.error("SKILLS_LIST is empty. Make sure skills.json is loaded correctly.")
        return []
    
    words = set(re.findall(r'\b\w+(?:\.\w+)*\b', text.lower()))  # Tokenize text, handling dot-separated words
    extracted = set()
    
    for word in words:
        result = process.extractOne(word, SKILLS_LIST, scorer=fuzz.partial_ratio)
        if result and result[1] > 80:  # Score > 80
            extracted.add(result[0].lower())
    
    return list(extracted)

def extract_contact_info(text):
    """Extracts email, phone number, and LinkedIn profile."""
    email = re.search(r'[\w\.]+@[\w\.]+', text)
    phone = re.search(r'\+?\d{10,12}', text)
    linkedin = re.search(r'linkedin.com/[\w\-]+', text)
    
    return {
        "Email": email.group(0) if email else "Not Found",
        "Phone": phone.group(0) if phone else "Not Found",
        "LinkedIn": linkedin.group(0) if linkedin else "Not Found"
    }

def extract_education(text):
    """Extracts education details."""
    education_patterns = [
        r'(?P<degree>B\.?Tech|Intermediate|Matriculation).*?(?P<institution>[\w\s]+),\s*(?P<location>[\w\s]+)',
        r'Session:\s*(?P<session>\d{4}-\d{4})\s*\|\s*Score:\s*(?P<score>[\d\.]+\s*CGPA|\d+%)'
    ]
    
    education = []
    matches = re.findall('|'.join(education_patterns), text)
    
    for match in matches:
        edu = {
            "Degree": match[0] if match[0] else "Unknown",
            "Institution": match[1] if match[1] else "Unknown",
            "Location": match[2] if match[2] else "Unknown",
            "Session": match[3] if match[3] else "Unknown",
            "Score": match[4] if match[4] else "Unknown"
        }
        education.append(edu)
    
    return education

def parse_resume(file_path):
    """Parses resume and extracts structured information."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None  # ✅ Return None to indicate failure

    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        logging.error(f"Unsupported file format: {ext}")
        return None  # ✅ Return None on failure

    if not text:
        logging.warning(f"No text extracted from {file_path}")
        return None  # ✅ Return None if no text extracted

    # ✅ Extract information
    contact_info = extract_contact_info(text)
    education = extract_education(text)
    skills = extract_skills(text)

    print("DEBUG: Extracted Skills ->", skills)  # 🔍 Debug output

    return text, skills, education  # ✅ Ensure this is a tuple


if __name__ == "__main__":
    resume_file = r"C:\Users\hp\OneDrive\Desktop\Ayush_Resume.pdf"
    parsed_data = parse_resume(resume_file)
    
    print(json.dumps(parsed_data, indent=4))
