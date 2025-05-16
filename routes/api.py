from flask import Blueprint, render_template, request, jsonify
from db import db
from models import * 
import json

api_routes = Blueprint("api_routes", __name__)

# Quiz Details ==========================================================
@api_routes.route("/quiz/<string:quiz_name>/api")
def quiz_details(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    if not quiz:
        return {"message": f"Name {quiz_name} not found"}, 404

    return jsonify(quiz.to_json())

@api_routes.route("/quiz/<string:quiz_name>/api/remCards")
def quiz_details_cards(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    if not quiz:
        return {"message": f"Name {quiz_name} not found"}, 404

    return jsonify(quiz.rem_cards_to_json())

# Update Quiz ==========================================================
@api_routes.route("/quiz/<string:quiz_name>/api/update", methods=["PUT"])
def update_quiz_mastery(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    if not quiz:
        return {"message": f"Name {quiz_name} not found"}, 404

    data = request.get_json()
    if not data:
        return {"message": "No data provided"}, 400
    
    completedCards = data

    quiz.completedCards = json.dumps(completedCards)

    db.session.commit()
    return jsonify(quiz.to_json()), 200

# Shuffle Quiz 

@api_routes.route("/quiz/<string:quiz_name>/api/shuffle", methods=["PUT"])
def shuffle_quiz(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    if not quiz:
        return {"message": f"Name {quiz_name} not found"}, 404

    quiz.randomize_Cards()
    return "success", 201