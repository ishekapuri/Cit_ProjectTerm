import pytest
from flask import Flask
from db import db
from routes.html import html_routes
from sqlalchemy import select, func, insert
from models import Collection, Quiz, Stack, StackQuiz

def create_app():
    # Flask expects template folder to be in the same directory, so we need to specify it in this case
    app = Flask(__name__, template_folder='../templates')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    app.register_blueprint(html_routes)

    return app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def app_with_data():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()
        db.session.add()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def client2(app_with_data):
    return app_with_data.test_client()

def test_homepage(client):
    response = client.get("/")
    assert b"<h1>Stackables</h1>" in response.data
    assert response.status_code == 200


