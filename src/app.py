from flask import Flask, request, jsonify
import os
from resume_parser import parse_resume
from skill_matcher import match_skills

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Only .pdf and .docx allowed"}), 400

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Parse resume
    # Parse resume
    parsed_result = parse_resume(file_path)

    if parsed_result is None or not isinstance(parsed_result, tuple) or len(parsed_result) != 3:
        return jsonify({"error": "Failed to parse resume"}), 500

    text, extracted_skills, extracted_education = parsed_result

    if not isinstance(extracted_skills, list) or len(extracted_skills) == 0:
        return jsonify({"error": "Skill extraction failed: No skills found"}), 500


    # Define required job skills (can be dynamic)
    job_skills = ["Flask", "AWS", "Python", "SQL"]
    
    if not isinstance(extracted_skills, list):
        return jsonify({"error": "Skill extraction failed"}), 500
    
    matched_skills, missing_skills, match_percentage = match_skills(extracted_skills, job_skills)

    return jsonify({
        "Extracted Skills": extracted_skills,
        "Job Skills": job_skills,
        "Matched Skills": matched_skills,
        "Missing Skills": missing_skills,
        "Match Percentage": match_percentage
    })

if __name__ == '__main__':
    app.run(debug=True)
