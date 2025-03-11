from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text
import os

app = Flask(__name__)

# Sample skill keywords (you can expand this list)
SKILL_KEYWORDS = {
    "Python", "Java", "Machine Learning", "Deep Learning", "Data Science", 
    "NLP", "Computer Vision", "SQL", "React", "Node.js", "Flask", "Django"
}

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    return extract_text(pdf_path)

def extract_skills(text):
    """Extract skills based on keyword matching."""
    text_lower = text.lower()
    extracted_skills = {skill for skill in SKILL_KEYWORDS if skill.lower() in text_lower}
    return list(extracted_skills)

def match_skills(resume_skills, job_skills):
    """Calculate skill match percentage."""
    matched = set(resume_skills) & set(job_skills)
    if len(job_skills) == 0:
        return {"matched_skills": list(matched), "match_score": 0}
    match_score = (len(matched) / len(job_skills)) * 100
    return {"matched_skills": list(matched), "match_score": round(match_score, 2)}

@app.route('/match', methods=['POST'])
def match_resume():
    """API endpoint to process resumes and job descriptions."""
    if 'file' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Missing file or job description"}), 400

    file = request.files['file']
    job_description = request.form['job_description']

    # Save file temporarily
    file_path = "uploaded_resume.pdf"
    file.save(file_path)

    # Extract text and process skills
    resume_text = extract_text_from_pdf(file_path)
    os.remove(file_path)  # Clean up

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    result = match_skills(resume_skills, job_skills)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
