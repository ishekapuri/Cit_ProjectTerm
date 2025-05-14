from flask import Blueprint, render_template, request
from db import db
from models import * 
import json

## test
html_routes = Blueprint("html_routes", __name__)

# HOME PAGE ==========================================================
@html_routes.route("/")
def home():
    collections = db.session.execute(db.select(Collection)).scalars()
    quizzes = db.session.execute(db.select(Quiz)).scalars()
    return render_template("home.html", collections=collections, quizzes=quizzes)

# MAKE QUIZ ==========================================================
@html_routes.route("/makeQuiz", methods=["GET"])
def make_quiz():
    collections = db.session.execute(db.select(Collection)).scalars()
    return render_template("makeQuiz.html", collections=collections)

@html_routes.route("/makeQuiz", methods=["POST"])
def make_quiz_post():
    collections = db.session.execute(db.select(Collection)).scalars()
    quizzes = db.session.execute(db.select(Quiz)).scalars()
    quiz_name = request.form.get("quiz_name")
    stack_ids = request.form.getlist("stack_ids")

    if quiz_name == "":
        return render_template("makeQuiz.html", 
                               error="Please enter a name for the quiz.",
                                collections=collections,
                                quizzes=quizzes), 400
    if db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar() is not None:
        return render_template("makeQuiz.html", 
                               error="Quiz name already exists.",
                                collections=collections,
                                quizzes=quizzes), 400
    if len(stack_ids) == 0:
        return render_template("makeQuiz.html", 
                               error="Please select at least one stack.",
                                collections=collections,
                                quizzes=quizzes), 400
    
    quiz = Quiz(name=quiz_name)
    db.session.add(quiz)
    
    for stack_id in stack_ids:
        stack = db.session.execute(db.select(Stack).where(Stack.id == stack_id)).scalar()
        db.session.add(StackQuiz(quiz=quiz, stack=stack))
    quizzes = db.session.execute(db.select(Quiz)).scalars()

    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    quiz.init_cards()

    db.session.add(quiz)
    db.session.commit()

    # goes to home after creating quiz (for now)
    return render_template("home.html", collections=collections, quizzes=quizzes)

# QUIZ INFO ==========================================================
@html_routes.route("/quiz/<string:quiz_name>", methods=["GET"])
def quiz_info(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    completedCards = json.loads(quiz.completedCards)
    remainingCards = json.loads(quiz.remainingCards)
    cardList = []
    for cardDict in remainingCards:
        for stack_id, cards in cardDict.items():
            for card in cards:
                cardList.append(db.session.execute(db.select(Card).where(Card.id == card)).scalar())

    stacks = db.session.execute(db.select(Stack).where(Stack.id.in_(db.session.execute(db.select(StackQuiz.stack_id).where(StackQuiz.quiz_id == quiz.id)).scalars()))).scalars()
    return render_template("quizInfo.html", quiz=quiz, stacks=stacks, data=cardList)


# COLLECTION LIST ==========================================================
@html_routes.route("/collections")
def collections():
    collections = db.session.execute(db.select(Collection)).scalars()
    return render_template("collections.html", data=collections)

# STACKS IN COLLECTION ==========================================================
@html_routes.route("/collections/<string:collection_name>")
def stacks(collection_name):
    collection_id = (db.session.execute(db.select(Collection).where(Collection.name == collection_name)).scalar()).id
    stacks = db.session.execute(db.select(Stack).where(Stack.collection_id == collection_id)).scalars()
    return render_template("stacks.html", collection=collection_name, data=stacks)

# # STACK DETAILS ==========================================================
@html_routes.route("/collections/<string:collection_name>/<string:stack_name>")
def cards(collection_name, stack_name):
    stack_id = (db.session.execute(db.select(Stack).where(Stack.name == stack_name)).scalar()).id
    cards = db.session.execute(db.select(Card).where(Card.stack_id == stack_id)).scalars()
    return render_template("cards.html", stack=stack_name, data=cards)





