# ----------------------
# Importing Libraries
# ---------------------

import os
import openai
import json
from dotenv import load_dotenv

# ------------------------
# Load API Key
# ------------------------

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

# ------------------------
# Reading the Text Files
# ------------------------

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error Reading {file_path}: {e}")
        return ""


# -----------------------------------
# Skill Extraction Using OpenAI GPT
# -----------------------------------

def extract_skills(text, source_type):
    prompt = f"""
    Extract a clean list of key professionals and technical skills from the following {source_type} text.
    Only return the skill names in a python list. Do not include explanations or duplicates.
    
    Text:
    {text[:3000]}  # Limit to 3000 charecters to avoid token limit
    """


    try:
        response = openai.ChatCompletion.create(                  # calling openAI API to get response from GPT
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0

        )

        result = response['choices'][0]['message']['content']                # store the response
        return json.loads(result) if result.startswith("[") else []
    except Exception as e:
        print(f"Error from OpenAI API: {e}")
        return []                                                   # Return empty list if error occurs
    

# -----------------------------
# Process All Files in Folder
# -----------------------------

def process_folder(folder_path, output_path, source_type):
    os.makedirs(output_path, exist_ok=True)                     # Creating output path
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            text = read_text_file(file_path)
            skills = extract_skills(text, source_type)

            output_file = os.path.splitext(filename)[0] + ".json"
            output_file_path = os.path.join(output_path, output_file)

            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump({"skills": skills}, f, indent=4)                    # save the python data into a json format

            print(f"Extracted skills from {filename}")


# -----------------------
# Main Driver
# -----------------------

if __name__ == "__main__":
    resumes_input = "../data/extracted_text/resumes_cleaned"
    jd_input = "../data/extracted_text/jd_cleaned"

    resumes_output = "../output/skills/resumes"
    jd_output = "../output/skills/jd"

    process_folder(resumes_input, resumes_output, source_type="resume")
    process_folder(jd_input, jd_output, source_type="job_description")