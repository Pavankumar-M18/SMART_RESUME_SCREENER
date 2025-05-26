# --------  IMPORTING LIBRARIES  ---------
import fitz
import os
import re


# ------------  Text Extraction From PDF  -----------------

def extract_text_from_pdf(file_path):                   
    try:
        doc = fitz.open(file_path)               # open the pdf file
        text = ""                                # initialize empty string to store all extracted text
        for page in doc:                         # loop over each page in the pdf
            text += page.get_text()              # get text from current page and add to text variable
        doc.close()                          # close the pdf file 
        return text                          # return the combined text from all pages
    except Exception as e:
        print(f"Error Reading {file_path}: {e}")       # prints error message with file if error occurs
        return ""                                 # return empty string if failed
    

# -----------------  Read The Text From a Text File(JD)  ---------------

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:           # open the text file in read mode using utf-8 encoding
            return file.read()            # read the entire file as a string and return it
    except Exception as e:
        print(f"Error Reading {file_path}: {e}")
        return ""

 
# -----------------  Text Cleaning  ----------------

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)        # replace all kind of whitespaces with a single space
    text = re.sub(r'[^\w\s]', '', text)     # remove all special charecters & keep only words and spaces
    return text.strip()                     # remove any extra space at the begining or ending of the text


# --------------  Process all Resumes in Folder  -------------

def process_resumes(resume_folder, output_folder):
    for filename in os.listdir(resume_folder):             # loop through each file name in given folder
        if filename.endswith(".pdf"):
            file_path = os.path.join(resume_folder, filename)   # builds complete path to the pdf file
            text = extract_text_from_pdf(file_path)             # returns raw text inside the pdf and stored in text variable
            cleaned_text = clean_text(text)                     # stores cleaned text in cleaned_text

            output_filename = os.path.splitext(filename)[0] + ".txt"    # changes pdf filename extension from .pdf to .txt file
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)                  # writes the cleaned text into the .txt file

            print(f"Processed Resume: {filename}")


# ----------- Process all Job Descriptions in folder  ----------------

def process_job_descriptions(jd_folder, jd_cleaned):
    for filename in os.listdir(jd_folder):                     # Loop over every file inside jd folder
        if filename.endswith(".txt"):                             # checks filename end with '.txt'
            file_path = os.path.join(jd_folder, filename)
            text = read_text_file(file_path)                     # raed & store the raw text in 'text' variable

            cleaned_text = clean_text(text)                      # clean the raw jd
            output_path = os.path.join(jd_cleaned, filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)               # write the cleaned text into the file
            
            print(f"Processed Job Description: {filename}")



# -------------------- Main Driver  -------------------

if __name__ == "__main__":
    resume_folder = "../data/raw_resumes_real"                             # Path to resumes PDF Files
    jd_folder = "../data/job_descriptions"                        # path to JD's '.txt' Files
    output_folder = "../data/extracted_text/resumes_cleaned"      # cleaned resumes text files will exist
    jd_output_folder = "../data/extracted_text/jd_cleaned"         # cleaned job description text files will exist

    # Create out put folders if doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(jd_output_folder, exist_ok=True)

    # Process resumes & JD's
    process_resumes(resume_folder, output_folder)
    process_job_descriptions(jd_folder, jd_output_folder)

    print("🎉 All resumes and JDs processed successfully.")