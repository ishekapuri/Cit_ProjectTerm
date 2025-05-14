from db import db
from app import app
from models import Stack, Card

class TestStack:
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
            stack = Stack(name="test_stack")
            db.session.add(stack)
            db.session.commit()
            
            test_stack = db.session.execute(db.select(Stack).where(Stack.name == "test_stack")).scalar()
            
            assert test_stack is not None
            assert test_stack.id is not None
            assert test_stack.name == "test_stack"

    def test_add_card_to_stack(self):
        with app.app_context():
            stack = Stack(name="test_stack2")
            card1 = Card(name="test_card", answer="answer")
            card2 = Card(name="test_card2", answer="answer2")
            db.session.add_all([stack, card1, card2])
            db.session.commit()
            
            stack.addCard(card1)
            
            stack.addCard(card2)

            assert len(stack.cards) == 2
