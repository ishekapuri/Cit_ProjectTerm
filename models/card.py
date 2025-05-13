from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey

class Card(db.Model):
    __tablename__ = "card_table"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    answer = mapped_column(String, nullable=False)
    flipped = mapped_column(Boolean, default=False)

    stack_id = mapped_column(Integer, ForeignKey("stack_table.id"))

    def __str__(self):
        return f"Card(id={self.id}, name={self.name}, answer={self.answer}, flipped={self.flipped})"



    