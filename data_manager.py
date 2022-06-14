import os
import csv

QUESTION_FILE = os.path.join(os.path.dirname(__file__), "data", "question.csv")
QUESTION_HEADERS = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "image",
]

ANSWER_FILE = os.path.join(os.path.dirname(__file__), "data", "answer.csv")
ANSWER_HEADERS = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image",
]


def read_file(filename, headers):
    with open(filename) as file:
        reader = csv.DictReader(file, headers)
        return list(reader)[1:]


def write_file(filename, headers, datalist):
    with open(filename, "w") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        for line in datalist:
            writer.writerow(line)


def read_questions():
    return read_file(QUESTION_FILE, QUESTION_HEADERS)


def read_question(id):
    return [item for item in read_questions() if item.get("id") == id][0]


def add_question(data):
    questions = read_questions()
    questions.append(data)
    write_file(QUESTION_FILE, QUESTION_HEADERS, questions)


