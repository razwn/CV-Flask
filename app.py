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
        pass
    
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


@app.route("/", methods=["GET"])
def index():
    return jsonify("Hello World!")


@app.route("/personal", methods=["GET"])
def personal():
    return jsonify("Personal Info")


@app.route("/experience", methods=["GET"])
def experience():
    return jsonify("Experience Info")


@app.route("/education", methods=["GET"])
def education():
    return jsonify("Education Info")


if __name__ == "__main__":
    run_type, resume_part, path = parse_command()
    run_type, resume_part = [x.lower() for x in (run_type, resume_part)]
    
    cv = CV()
    
    if "local" in run_type:
        pp(cv.fetch_cv_data(resume_part))
    elif "server" in run_type:
        app.run()
