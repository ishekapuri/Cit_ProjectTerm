from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
import random

class StackQuiz(db.Model):
    __tablename__ ="stackQuiz_table"

    quiz_id = mapped_column(Integer, ForeignKey("quiz_table.id"), primary_key=True)
    stack_id = mapped_column(Integer, ForeignKey("stack_table.id"), primary_key=True)

    stack = relationship("Stack")
    quiz = relationship("Quiz", back_populates="contents")

    def completeQuestion(self, index):
        self.completedQuestions.append(index)

    def resetCompletedQuestions(self):
        self.completedQuestions = []

    def shuffleQuestions(self):
        questions = self.stack.cards
        random.shuffle(questions)
        return questions



    