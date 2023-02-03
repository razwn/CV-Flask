import argparse
import logging
import re

from flask import Flask, jsonify
from pypdf import PdfReader
from pprint import pprint as pp

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


def parse_command():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_type", help="Local or Server")
    parser.add_argument("resume_part", help="Personal, Experience or Education")
    parser.add_argument("path", help="Path to the CV file")
    
    args = parser.parse_args()
    return args.run_type, args.resume_part, args.path


class CV:
    def __init__(self):
        self.cv_data = self.process_cv_data()
    
    def __import_CV(self):
        try:
            reader = PdfReader(path)
        except FileNotFoundError as fnf_error:
            app.logger.error(f"File not found: {fnf_error}")
            return str(fnf_error)
        number_of_pages = len(reader.pages)
        text = list()
        for i in range(number_of_pages):
            page = reader.pages[i]
            page_text = page.extract_text().split("\n")[:-1]
            text += page_text
        return text
    
    def process_cv_data(self):
        text = self.__import_CV()
        for index, row in enumerate(text[2:], 2):
            match = re.findall(r".+@.+\..+", row)
            if match:
                email = match[0]
                continue
            
            match = re.findall(r"linkedin.com.+", row)
            if match:
                linkedin_url = match[0]
            
            if "Summary" in row:
                index_summary = index
            
            elif "Experience" in row:
                summary = text[index_summary + 1 : index]
                summary = [row for row in summary if "\xa0" not in row]
                
                index_experience = index
            
            elif "Education" in row:
                experience_row_list = text[index_experience + 1 : index]
                nr_exp = len(experience_row_list)
                experiences = [experience_row_list[i : i + 3] for i in range(0, nr_exp, 3)]
                experiences = [
                    dict(zip(["title", "company", "period"], exp))
                    for exp in experiences
                ]
                
                index_education = index
                
            elif "Licenses & Certifications" in row:
                education_row_list = text[index_education + 1 : index]
                nr_edu = len(education_row_list)
                education = [education_row_list[i : i + 3] for i in range(0, nr_edu, 3)]
                education = [
                    dict(zip(["university", "degree", "period"], edu))
                    for edu in education
                ]
                
            elif "Skills" in row:
                skills = text[index + 1 :]
                skills = [skill.replace("\xa0", "") for skill in skills]
                
        cv_data = {
            "personal": {
                "name": f"{text[0]}",
                "location": f"{text[1]}",
                "email": email,
                "linkedin": linkedin_url,
                "summary": " ".join(summary),
            },
            "experience": {"companies": experiences, "skills": skills},
            "education": education,
        }
        return cv_data
    
    def fetch_cv_data(self, resume_part):
        if "all" in resume_part:
            return self.cv_data
        return self.cv_data[resume_part]


@app.route("/", methods=["GET"])
def index():
    return jsonify(cv.fetch_cv_data("all"))


@app.route("/personal", methods=["GET"])
def personal():
    return jsonify(cv.fetch_cv_data("personal"))


@app.route("/experience", methods=["GET"])
def experience():
    return jsonify(cv.fetch_cv_data("experience"))


@app.route("/education", methods=["GET"])
def education():
    return jsonify(cv.fetch_cv_data("education"))


if __name__ == "__main__":
    run_type, resume_part, path = parse_command()
    run_type, resume_part = [x.lower() for x in (run_type, resume_part)]
    
    cv = CV()
    
    if "local" in run_type:
        pp(cv.fetch_cv_data(resume_part))
    elif "server" in run_type:
        app.run()
