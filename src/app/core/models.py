from sqlalchemy import Boolean, Integer, String, JSON
from flask_login import UserMixin
from core import db, Base


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(120), unique=True)
    password = db.Column(String(300), nullable=False)
    first_name = db.Column(String(30), nullable=True)
    last_name = db.Column(String(30), nullable=True)
    tutor = db.Column(Boolean, default=False)
    biography = db.Column(JSON, nullable=True)

    def __init__(self, email, password, first_name=None, last_name=None,
                 biography=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography

    def __repr__(self):
        return f'<User [{self.id}] - {self.first_name}>'