from difflib import get_close_matches

def get_closest_match(skill, job_skills):
    """Finds the closest match for a skill from job_skills using fuzzy matching"""
    match = get_close_matches(skill, job_skills, n=1, cutoff=0.8)
    return match[0] if match else None

def match_skills(resume_skills, job_skills):
    """Matches extracted resume skills with job requirements"""
    resume_skills = {skill.lower().strip() for skill in resume_skills}
    job_skills = {skill.lower().strip() for skill in job_skills}

    matched = {get_closest_match(skill, job_skills) for skill in resume_skills if get_closest_match(skill, job_skills)}
    missing = job_skills - matched

    match_percentage = (len(matched) / len(job_skills)) * 100 if job_skills else 0

    return list(matched), list(missing), match_percentage

if __name__ == "__main__":
    job_skills = ["Flask", "AWS", "Python", "SQL"]  # Sample job description skills

    from resume_parser import parse_resume  

    resume_file = r"C:\Users\hp\OneDrive\Desktop\Ayush_Resume.pdf"  # Change this to your resume file
    extracted_skills = parse_resume(resume_file)

    if extracted_skills:
        matched_skills, missing_skills, match_percentage = match_skills(extracted_skills, job_skills)

        print("\n🔍 Job Skills:", job_skills)
        print("✅ Matched Skills:", matched_skills)
        print("❌ Missing Skills:", missing_skills)
        print(f"📊 Match Percentage: {match_percentage:.2f} %")
