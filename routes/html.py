from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models import * 
import json, math

## test
html_routes = Blueprint("html_routes", __name__)

# HOME PAGE ==========================================================
@html_routes.route("/")
def home():
    collections = db.session.execute(db.select(Collection)).scalars()
    quizzes = db.session.execute(db.select(Quiz)).scalars()
    return render_template("home.html", collections=collections, quizzes=quizzes)

# MAKE QUIZ ==========================================================
@html_routes.route("/makeQuiz", methods=["GET"])
def make_quiz():
    collections = db.session.execute(db.select(Collection)).scalars()
    return render_template("makeQuiz.html", collections=collections)

@html_routes.route("/makeQuiz", methods=["POST"])
def make_quiz_post():
    collections = db.session.execute(db.select(Collection)).scalars()
    quizzes = db.session.execute(db.select(Quiz)).scalars()
    quiz_name = request.form.get("quiz_name")
    stack_ids = request.form.getlist("stack_ids")

    if quiz_name == "":
        return render_template("makeQuiz.html", 
                               error="Please enter a name for the quiz.",
                                collections=collections,
                                quizzes=quizzes), 400
    if db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar() is not None:
        return render_template("makeQuiz.html", 
                               error="Quiz name already exists.",
                                collections=collections,
                                quizzes=quizzes), 400
    if len(stack_ids) == 0:
        return render_template("makeQuiz.html", 
                               error="Please select at least one stack.",
                                collections=collections,
                                quizzes=quizzes), 400
    
    quiz = Quiz(name=quiz_name)
    db.session.add(quiz)
    
    for stack_id in stack_ids:
        stack = db.session.execute(db.select(Stack).where(Stack.id == stack_id)).scalar()
        db.session.add(StackQuiz(quiz=quiz, stack=stack))
    quizzes = db.session.execute(db.select(Quiz)).scalars()

    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    quiz.init_cards()

    db.session.add(quiz)
    db.session.commit()

    # goes to home after creating quiz (for now)
    return render_template("home.html", collections=collections, quizzes=quizzes)

# QUIZ INFO ==========================================================
@html_routes.route("/quiz/<string:quiz_name>", methods=["GET"])
def quiz_info(quiz_name):
    quiz = db.session.execute(db.select(Quiz).where(Quiz.name == quiz_name)).scalar()
    completedCards = json.loads(quiz.completedCards)
    remainingCards = json.loads(quiz.remainingCards)
    # format: [stackname, stacksize, proficiency]
    stackList = quiz.getStacks()
    cardList = []
    quizStats = []
    for pair in remainingCards:
        for stack_id, card in pair.items():
            stack = db.session.execute(db.select(Stack).where(Stack.id == stack_id)).scalar()
            cardList.append(db.session.execute(db.select(Card).where(Card.id == card)).scalar())
    
    for stack in stackList:
        completed = 0
        total = stack.countCards()
        for pair in completedCards:
            pair = json.loads(pair)
            for stack_id, card in pair.items():
                if stack.id == int(stack_id):
                    completed += 1
        percent = math.floor((completed / total)*100)
        quizStats.append([stack.name, stack.collection.name, percent])

    return render_template("quizInfo.html", quiz=quiz, stats=quizStats, data=cardList)


# COLLECTION LIST ==========================================================
@html_routes.route("/collections")
def collections():
    collections = db.session.execute(db.select(Collection)).scalars()
    return render_template("collections.html", data=collections)

# STACKS IN COLLECTION ==========================================================
@html_routes.route("/collections/<string:collection_name>")
def stacks(collection_name):
    collection_id = (db.session.execute(db.select(Collection).where(Collection.name == collection_name)).scalar()).id
    stacks = db.session.execute(db.select(Stack).where(Stack.collection_id == collection_id)).scalars()
    return render_template("stacks.html", collection=collection_name, data=stacks)

# # STACK DETAILS ==========================================================
@html_routes.route("/collections/<string:collection_name>/<string:stack_name>")
def cards(collection_name, stack_name):
    stack = db.session.execute(db.select(Stack).where(Stack.name == stack_name)).scalar()
    cards = db.session.execute(db.select(Card).where(Card.stack_id == stack.id)).scalars()
    collection = db.session.execute(db.select(Collection).where(Collection.name == collection_name)).scalar()
    return render_template("cards.html", collection=collection, stack=stack, data=cards)




# # DELETE CARD ========================================

@html_routes.route("/delete_card/<int:card_id>", methods=["POST"])
def delete_card(card_id):
    card = db.session.get(Card, card_id)
    
    stack_id = card.stack_id
    db.session.delete(card)
    db.session.commit()

    stack = db.session.execute(db.select(Stack).where(Stack.id == stack_id)).scalar()
    cards = db.session.execute(
    db.select(Card).where(Card.stack_id == stack_id)).scalars()

    quizlist = db.session.execute(db.select(Quiz)).scalars()
    for quiz in quizlist:
        quiz.init_cards()
    db.session.commit()
    
    return render_template("cards.html", stack=stack, data=cards)

@html_routes.route('/edit/<int:card_id>', methods=['GET'])
def edit_card(card_id):
    card = db.session.get(Card, card_id)
    return render_template("edit.html", card=card, collection_name=card.stack.collection.name, stack_name=card.stack.name)


@html_routes.route('/update/<int:card_id>', methods=['POST'])
def update_card(card_id):
    card = db.session.get(Card, card_id)
    stack_id = card.stack_id
    card.name = request.form['name']
    card.answer = request.form['answer']

    db.session.commit()

    stack = db.session.get(Stack, stack_id)
    cards = db.session.execute(
    db.select(Card).where(Card.stack_id == stack_id)).scalars()
    
    return render_template("cards.html", stack=stack.name, data=cards)

@html_routes.route('/create_collection', methods=['GET', 'POST'])
def create_collection():
    if request.method == 'POST':
        name = request.form.get('collection_name')
        if name:
            new_collection = Collection(name=name)
            db.session.add(new_collection)
            db.session.commit()
            collections = db.session.execute(db.select(Collection)).scalars().all()
            return render_template("home.html", collections=collections)
        return render_template('createCollection.html', error="Collection name is required.")
    return render_template('createCollection.html')


@html_routes.route('/create_stack/<string:collection_name>', methods=['GET', 'POST'])
def create_stack(collection_name):
    collection = db.session.execute(db.select(Collection).where(Collection.name == collection_name)).scalar()

    if request.method == 'POST':
        stack_name = request.form.get('stack_name')
        if stack_name:
            new_stack = Stack(name=stack_name, collection=collection)
            db.session.add(new_stack)
            db.session.commit()
            collections = db.session.execute(db.select(Collection)).scalars().all()
            return render_template("home.html", collections=collections)
        return render_template('createStack.html', error="Stack name is required.", collection_name=collection_name)
    return render_template('createStack.html', collection_name=collection_name)


@html_routes.route('/create_card/<string:stack_name>', methods=['GET', 'POST'])
def create_card(stack_name):
    stack = db.session.execute(db.select(Stack).where(Stack.name == stack_name)).scalar()
    if request.method == 'POST':
        card_name = request.form.get('name')
        card_answer = request.form.get('answer')

        if not card_name or not card_answer:
            return render_template('createCard.html', stack=stack, error="Both fields are required.")

        new_card = Card(name=card_name, answer=card_answer, stack=stack)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('html_routes.cards', collection_name=stack.collection.name, stack_name=stack.name))
    return render_template('createCard.html', stack=stack)


@html_routes.route('/delete_stack/<string:stack_name>', methods=['POST'])
def delete_stack(stack_name):
    stack = db.session.execute(db.select(Stack).where(Stack.name == stack_name)).scalar()
    db.session.delete(stack)
    db.session.commit()
    collections = db.session.execute(db.select(Collection)).scalars().all()
    return render_template("home.html", collections=collections)