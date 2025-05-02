from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey

class StackQuiz(db.Model):
    __tablename__ ="stackQuiz_table"

    quiz_id = mapped_column(Integer, ForeignKey("quiz_table.id"), primary_key=True)
    stack_id = mapped_column(Integer, ForeignKey("stack_table.id"), primary_key=True)

    stack = relationship("Stack")
    quiz = relationship("Quiz", back_populates="contents")