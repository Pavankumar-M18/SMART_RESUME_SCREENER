# IMPORTING LIBRARIES

import os
import json

# -----------------------------
# READ SKILLS FROM JSON FILES
# ------------------------------

def read_skills_from_json(folder_path):
    """
    Reads all JSON files from a folder and returns {filename: [skills]} Dictionary
    """
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    content = json.load(f)
                    data[filename] = content.get("skills", [])
                except Exception as e:
                    print(f"Error Reading {filename}: {e}")
    return data


# ----------------------
# JACCARD SIMILARITY
# -----------------------

def jaccard_similarity(set1, set2):
    """
    calculate Jaccard Similarity between two sets
    """
    intersection = set1.intersection(set2)               # common item
    union = set1.union(set2)                             # All unique items
    if not union:
        return 0.0
    return len(intersection) / len(union)               # Jaccard similarity score


# ------------------------------
# MATCH RESUMES BASED ON SKILLS
# ------------------------------

def match_resumes(resume_skills_data, jd_skills_data, top_n=4):
    """
    Compare each Resume's skills to JD's skills and resturn top N matches.
    """
    results = []                    # to store each resume's similarity score

    jd_skills = list(jd_skills_data.values())[0]
    jd_skills_set = set([skill.lower() for skill in jd_skills])

    for resume_file, skills in resume_skills_data.items():
        resume_skills_set = set([skill.lower() for skill in skills])
        similarity = jaccard_similarity(jd_skills_set, resume_skills_set)
        results.append((resume_file, similarity))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]
    

# ----------------------
# MAIN DRIVER
#-----------------------

if __name__ == "__main__":
    resume_skills_folder = "../output/skills/resumes"
    jd_skills_folder = "../output/skills/jd"

    resume_skills_data = read_skills_from_json(resume_skills_folder)
    jd_skills_data = read_skills_from_json(jd_skills_folder)

    top_matches = match_resumes(resume_skills_data, jd_skills_data, top_n=5)

    print("\nTop Matching Resumes based on skills:")
    for filename, score in top_matches:
        print(f"{filename} => Similarity Score: {score:.2f}")