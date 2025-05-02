from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

class Collection(db.Model):
    __tablename__="collection_table"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    stacks = relationship("Stack", back_populates="collection")

    def countStacks(self):
        return len(self.stacks)