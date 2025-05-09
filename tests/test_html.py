# import pytest
# from flask import Flask

# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
#     from db import db
#     db.init_app(app)

#     from yourapplication.views.admin import admin
#     from yourapplication.views.frontend import frontend
#     app.register_blueprint(admin)
#     app.register_blueprint(frontend)

#     return app