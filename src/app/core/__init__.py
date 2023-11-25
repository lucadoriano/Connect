from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core import settings

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.POSTGRES_URI

db = SQLAlchemy(app)
Base = db.Model


def init_db():
    from core.models import User
    db.create_all()

with app.app_context():
    init_db()