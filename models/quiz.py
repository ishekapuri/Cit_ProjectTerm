from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Boolean
from models import StackQuiz

    
class Quiz(db.Model):
    __tablename__="quiz_table"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    isComplete = mapped_column(Boolean, default=False)


    contents = relationship("StackQuiz", back_populates="quiz")

    def addStack(self, stack_id):
        stackQuiz = StackQuiz(self.id, stack_id)
        db.session.add(stackQuiz)
        db.session.commit()
