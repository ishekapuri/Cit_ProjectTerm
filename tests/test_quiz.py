from db import db
from app import app
from models import Quiz, Stack, StackQuiz
import pytest

class TestQuiz:
    def setup_method(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        with app.app_context():
            db.create_all()

    def teardown_method(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_quiz(self):
        with app.app_context():
            quiz = Quiz(name="test_quiz")
            db.session.add(quiz)
            db.session.commit()
            
            quiz = db.session.execute(db.select(Quiz).where(Quiz.name == "test_quiz")).scalar()
            
            assert quiz is not None
            assert quiz.id is not None
            assert quiz.name == "test_quiz"
            assert quiz.isComplete is False

    def test_add_stack_to_quiz(self):
        with app.app_context():
            quiz = Quiz(name="test_quiz2")
            stack = Stack(name="test_stack")
            db.session.add_all([quiz, stack])
            db.session.commit()
            
            quiz.addStack(stack.id)
            
            stack_quiz = db.session.execute(
                db.select(StackQuiz).where(StackQuiz.quiz_id == quiz.id, StackQuiz.stack_id == stack.id)).scalar()
            
            assert stack_quiz is not None
            assert stack_quiz.quiz_id == quiz.id
            assert stack_quiz.stack_id == stack.id

    def test_get_stacks_for_quiz(self):
        with app.app_context():
            quiz = Quiz(name="test_quiz3")
            stack1 = Stack(name="test_stack2")
            stack2 = Stack(name="test_stack3")
            db.session.add_all([quiz, stack1, stack2])
            db.session.commit()
            
            quiz.addStack(stack1.id)
            quiz.addStack(stack2.id)

            stacks = quiz.getStacks()
            assert len(stacks) == 2
            assert stacks[0].name == "test_stack2"
            assert stacks[1].name == "test_stack3"
