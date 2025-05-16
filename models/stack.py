from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

    
class Stack(db.Model):
    __tablename__="stack_table"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    cards = relationship("Card")
    collection = relationship("Collection", back_populates="stacks")
    collection_id = mapped_column(Integer, ForeignKey("collection_table.id"))
    cards = db.relationship('Card', back_populates='stack')

    def countCards(self):
        return len(self.cards)
    
    def addCard(self, card):
        self.cards.append(card)
        db.session.commit()
