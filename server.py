from flask import Flask, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
import os

import data_manager

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(__file__), "static", "uploads"
)


@app.get("/")
def index():
    return render_template(
        "index.html",
        questions=data_manager.read_questions(),
    )


@app.get("/question/<qid>")
@app.get("/question/<qid>/")
def single_question(qid):
    return render_template("single.html", question=data_manager.read_question(qid))


def vote_question(qid, vote):
    questions = data_manager.read_questions()
    for index, question in enumerate(questions):
        if question.get("id") == qid:
            questions[index]["vote_number"] = (
                int(questions[index]["vote_number"]) + vote
            )

    data_manager.write_file(
        data_manager.QUESTION_FILE,
        data_manager.QUESTION_HEADERS,
        questions,
    )


@app.get("/question/<qid>/vote/up")
@app.get("/question/<qid>/vote/up/")
def upvote_question(qid):
    vote_question(qid, 1)
    return redirect(url_for("single_question", qid=qid))


@app.get("/question/<qid>/vote/down")
@app.get("/question/<qid>/vote/down/")
def downvote_question(qid):
    vote_question(qid, -1)
    return redirect(url_for("single_question", qid=qid))


@app.get("/new")
def new_question_form():
    return render_template("new_question.html")


@app.post("/new")
def new_question():
    try:
        f = request.files["File"]
        image = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], image))
    except KeyError:
        image = ""

    new_data = {
        "id": 0,
        "submission_time": 0,
        "view_number": 1,
        "vote_number": 0,
        "title": request.form.get("title"),
        "message": request.form.get("message"),
        "image": image,
    }

    data_manager.add_question(new_data)
    return redirect(url_for("single_question", qid=0))


if __name__ == "__main__":
    app.run(debug=True)
