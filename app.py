from flask import Flask
from db import db 
from pathlib import Path
from routes.html import html_routes
from routes.api import api_routes

# test gitignore

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path("database").resolve()

db.init_app(app)

app.register_blueprint(html_routes)
app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.run(debug=True, port=8888)