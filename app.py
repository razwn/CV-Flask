import argparse
import logging
import re

from flask import Flask, jsonify
from pypdf import PdfReader
from pprint import pprint as pp

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


def parse_command():
    """Parses command line arguments and returns them.
    
    :rtype: tuple(str, str, str)
    :return: A tuple of the run type, resume part and path to the CV file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("run_type", help="Local or Server")
    parser.add_argument("resume_part", help="Personal, Experience or Education")
    parser.add_argument("path", help="Path to the CV file")
    
    args = parser.parse_args()
    return args.run_type, args.resume_part, args.path


class CV:
    """Class for processing CV data from a PDF file."""
    def __init__(self):
        self.cv_data = self.process_cv_data()
    
    def __import_CV(self):
        """
        Import CV as a list of strings.
        
        :param self: self object, the instance of the class.
        :type self: object
        
        :raises FileNotFoundError: If the specified file is not found.
        
        :rtype: list
        :return: List of strings, each string representing a line of text from the CV.
        """
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
        """Processes the CV data from the PDF file given and returns a dictionary of the processed data.
        
        :param self: self, the instance of the class
        :type self: object
        
        :rtype: dict
        :return: A dictionary of the processed CV data with the following structure:
                {
                    "personal": {
                        "name": str,
                        "location": str,
                        "email": str,
                        "linkedin": str,
                        "summary": str
                    },
                    "experience": {
                        "companies": List[{"title": str, "company": str, "period": str}]
                        "skills": List[str]
                    },
                    "education": List[{"university": str, "degree": str, "period": str}]
                }
        """
        text = self.__import_CV()
        for index, row in enumerate(text[2:], 2):
            # Iterating over the rows omitting the first two rows as they are assumed to be the name and location and taken care of separately. 
            match = re.findall(r".+@.+\..+", row)
            if match:
                email = match[0]
                continue
            
            match = re.findall(r"linkedin.com.+", row)
            if match:
                linkedin_url = match[0]
            
            if "Summary" in row:
                index_summary = index # Storing the index of the row containing the word "Summary" for later use.
            
            elif "Experience" in row:
                summary = text[index_summary + 1 : index] # Using the index saved before to get the summary section.
                summary = [row for row in summary if "\xa0" not in row]
                
                index_experience = index # Storing the index of the row containing the word "Experience" for later use.
            
            elif "Education" in row:
                experience_row_list = text[index_experience + 1 : index] # Using the index saved before to get the experience section.
                nr_exp = len(experience_row_list)
                experiences = [experience_row_list[i : i + 3] for i in range(0, nr_exp, 3)] # Splitting the list into sublists of length 3.
                experiences = [
                    dict(zip(["title", "company", "period"], exp))
                    for exp in experiences 
                ] # Creating a list of dictionaries with the keys "title", "company" and "period" and the values from the sublists.
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
        """Fetches the CV data for the specified resume part and returns it as a dictionary.
        :param self: self, the instance of the class
        :type self: object
        :param resume_part: The resume part to fetch data for <personal/experience/education>.
        :type resume_part: str
        
        :rtype: dict
        :return: A dictionary of the processed CV data for the specified resume part.
        """
        if "all" in resume_part:
            return self.cv_data
        return self.cv_data[resume_part]


@app.route("/", methods=["GET"])
def index():
    """Returns a jsonified dictionary of the data from the CV."""
    return jsonify(cv.fetch_cv_data("all"))


@app.route("/personal", methods=["GET"])
def personal():
    """Returns a jsonified dictionary of the personal data from the CV."""
    return jsonify(cv.fetch_cv_data("personal"))


@app.route("/experience", methods=["GET"])
def experience():
    """Returns a jsonified dictionary of the experience data from the CV."""
    return jsonify(cv.fetch_cv_data("experience"))


@app.route("/education", methods=["GET"])
def education():
    """Returns a jsonified dictionary of the education data from the CV."""
    return jsonify(cv.fetch_cv_data("education"))


if __name__ == "__main__":
    run_type, resume_part, path = parse_command()
    run_type, resume_part = [x.lower() for x in (run_type, resume_part)]
    
    cv = CV()
    
    if "local" in run_type:
        pp(cv.fetch_cv_data(resume_part))
    elif "server" in run_type:
        app.run()
