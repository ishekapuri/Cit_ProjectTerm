from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, orm
from models import StackQuiz, Stack, Card
import json, random
    
class Quiz(db.Model):
    __tablename__="quiz_table"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    isComplete = mapped_column(Boolean, default=False)
    completedCards = mapped_column(String, default="[]")
    remainingCards = mapped_column(String, default="[]")

    contents = relationship("StackQuiz", back_populates="quiz")

    def init_cards(self):
        remainingJSON = json.loads(self.remainingCards)
        stackQuizzes = db.session.execute(db.select(StackQuiz).where(StackQuiz.quiz_id == self.id)).scalars()

        for stackQuiz in stackQuizzes:
            if stackQuiz.stack_id not in remainingJSON:
                cards = db.session.execute(db.select(Card).where(Card.stack_id == stackQuiz.stack_id)).scalars()
                remainingJSON.append({stackQuiz.stack.id: [card.id for card in cards]})
        
        self.remainingCards = str(remainingJSON)

    def addStack(self, stack_id):
        stackQuiz = StackQuiz(quiz=self, stack=db.session.execute(db.select(Stack).where(Stack.id == stack_id)).scalar())
        db.session.add(stackQuiz)
        db.session.commit()

    def getStacks(self):
        stackQuizzes = db.session.execute(db.select(StackQuiz).where(StackQuiz.quiz_id == self.id)).scalars()
        stacks = []
        for stackQuiz in stackQuizzes:
            stacks.append(stackQuiz.stack)
        return stacks

    def randomize_Cards(self):
        remainingJSON = json.loads(self.remainingCards)
        remainingJSON = random.shuffle(remainingJSON)
        self.remainingCards = str(remainingJSON)
        db.session.commit()
    
    def update_Quiz_Results(self, completedCards, remainingCards):
        self.completedCards = str(completedCards)
        self.remainingCards = str(remainingCards)
        if len(remainingCards) == 0:
            self.isComplete = True
        db.session.commit()

    def reset_quiz(self):
        self.isComplete = False
        self.completedCards = str([])
        self.remainingCards = str([{stackQuiz.stack.id: [card.id for card in db.session.execute(db.select(Card).where(Card.stack_id == stackQuiz.stack.id)).scalars()]} for stackQuiz in db.session.execute(db.select(StackQuiz).where(StackQuiz.quiz_id == self.id)).scalars()])
        db.session.commit()

    