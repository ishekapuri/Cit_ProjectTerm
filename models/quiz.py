from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Boolean

    
class Quiz(db.Model):
    __tablename__="quiz_table"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    isComplete = mapped_column(Boolean, default=False)

    contents = relationship("StackQuiz", back_populates="quiz")
