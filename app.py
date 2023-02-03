import argparse
import logging
import re

from flask import Flask, jsonify
from pypdf import PdfReader
from pprint import pprint as pp

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


class CV:
    def __init__(self):
        pass


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
    app.run()
