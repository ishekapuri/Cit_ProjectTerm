from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)