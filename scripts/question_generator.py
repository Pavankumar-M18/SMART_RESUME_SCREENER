# --------------------
# IMPORTING LIBRARIES
# --------------------

import os
import json

# -----------------------
# READ SKILLS FROM JSON
# -----------------------

def read_skills(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("skills", [])
    except Exception as e:
        print(f"Error Reading {file_path}: {e}")
        return []

# -----------------------------
# SIMULATED QUESTION GENERATOR
# -----------------------------

def generate_questions(resume_skills, jd_skills):
    """
    Simulates interview question generation based on shared skills
    """
    shared_skills = set(resume_skills).intersection(set(jd_skills))                 # Extract common skills

    if not shared_skills:
        return [
            "Tell me about yourself.",
            "Why do you want this role?",
            "What is your biggest strength?"
        ]
    
    questions = []                 # To collect generated questions
    for skill in shared_skills:
        questions.append(f"Can you explain a project where you used {skill}?")
        questions.append(f"What challenges have you faced with {skill}?")

    return questions[:5]        # Limit to 5 questions


# -----------------------
# PROCESS ALL RESUMES
# -----------------------

def process_questions(resume_folder, jd_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    jd_skills = read_skills(jd_file)

    for filename in os.listdir(resume_folder):
        if filename.endswith(".json"):
            resume_path = os.path.join(resume_folder, filename)
            resume_skills = read_skills(resume_path)

            questions = generate_questions(resume_skills, jd_skills)

            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({"questions": questions}, f, indent=4)

            print(f"Generated questions for {filename}")


# -------------------
# MAIN DRIVER
# -------------------

if __name__ == "__main__":
    resumes_input = "../output/skills/resumes"
    jd_input = "../output/skills/jd/software_engineer_jd.json"
    questions_output = "../output/questions"

    process_questions(resumes_input, jd_input, questions_output)