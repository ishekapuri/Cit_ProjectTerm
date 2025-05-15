from flask import Blueprint, render_template, request, jsonify
from db import db
from models import * 
import json

api_routes = Blueprint("api_routes", __name__)

# Quiz Details ==========================================================
@api_routes.route("/api/quiz/<string:quiz_name>")
def quiz_details(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    if not quiz:
        return {"message": f"Name {quiz_name} not found"}, 404

    return jsonify(quiz.to_json())

# Update Quiz ==========================================================
@api_routes.route("/api/quiz/<string:quiz_name>/update", methods=["POST"])
def update_quiz_mastery(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    if not quiz:
        return {"message": f"Name {quiz_name} not found"}, 404

    data = request.json()
    if not data:
        return {"message": "No data provided"}, 400
    
    completedCards = data["completedCards"]
    remainingCards = data["remainingCards"]
    quiz.completedCards = jsonify(completedCards)
    quiz.remainingCards = jsonify(remainingCards)

    db.session.commit()

    return render_template("quiz_details.html", quiz=quiz, stacks=quiz.stacks, cards=quiz.cards)