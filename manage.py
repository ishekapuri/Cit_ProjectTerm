from db import db
from app import app
from sqlalchemy import select, func, insert
import csv, os, random, sys
from models import Card, Collection, Quiz, Stack, StackQuiz

dirname = os.path.dirname(__file__)
flash_cards = os.path.join(dirname, "./data/flash_cards.csv")
sample_stacks = os.path.join(dirname, "./data/stacks.csv")

subjects = {
    1: "Biology",
    2: "Chemistry",
    3: "Computer Science",
    4: "Math",
    5: "Physics",
    6: "Economics",
}

def createAll():
    db.create_all()

def dropAll():
    db.drop_all()

def loadData():
    with db.session() as session:
        with open(sample_stacks, newline='') as stack_data:
            stacks = csv.reader(stack_data)
            next(stacks, None)
            for row in stacks:
                # add a new collection if it doesn't exist
                if not session.execute(select(Collection).where(Collection.id == row[2])).scalar():
                    collectionID = int(row[2])
                    newCollection = Collection(
                        id=collectionID,
                        name=subjects[collectionID]
                    )
                    session.add(newCollection)
                # make a new stack if it doesn't exist
                if not session.execute(select(Stack).where(Stack.id == row[0])).scalar():
                    newStack = Stack(
                        id=row[0],
                        name=row[1],
                        collection_id=row[2]
                    )
                    session.add(newStack)

        with open(flash_cards, newline='') as card_data:
            cards = csv.reader(card_data)
            next(cards, None)
            for row in cards:
                # make a new card if it doesn't exist
                if not session.execute(select(Card).where(Card.id == row[0])).scalar():
                    newCard = Card(
                        id=row[0],
                        name=row[1],
                        answer=row[2],
                        stack_id=row[4]
                    )
                    session.add(newCard)
        session.commit()


if __name__ == "__main__":

    with app.app_context():

        # dropAll()
        createAll()
        loadData()
