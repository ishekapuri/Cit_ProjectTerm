# import pytest
# from flask import Flask
# from db import db
# from routes.html import html_routes
# from routes.api import api_routes
# from sqlalchemy import select, func, insert
# from models import Collection, Quiz, Stack, Card

# def create_app():
#     # Flask expects template folder to be in the same directory, so we need to specify it in this case
#     app = Flask(__name__, template_folder='../templates')
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.init_app(app)
#     app.register_blueprint(html_routes)
#     app.register_blueprint(api_routes)
#     return app

# # client with 2 stacks, 3 cards
# @pytest.fixture()
# def app_with_data():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#     })
#     with app.app_context():
#         db.create_all()
#         db.session.add_all([
#             Stack(name="Test Stack 1"),
#             Stack(name="Test Stack 2"),
#             Card(name="Test Card 1", answer="Answer 1", stack_id=1),
#             Card(name="Test Card 2", answer="Answer 2", stack_id=1),
#             Card(name="Test Card 3", answer="Answer 3", stack_id=2),
#         ])
#         db.session.commit()
#     yield app
#     with app.app_context():
#         db.session.remove()
#         db.drop_all()

# @pytest.fixture()
# def client2(app_with_data):
#     app = app_with_data
#     with app.app_context():
#         yield app.test_client()

# def test_get_quiz(client2):
#     response = client2.get("/")
#     assert response.status_code == 200
#     assert b"<h2>Create a New Quiz</h2>" in response.data