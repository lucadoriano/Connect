from sqlalchemy import Boolean, Integer, String

from core import db, Base


class User(Base):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(30), nullable=False)
    last_name = db.Column(String(30), nullable=False)
    email = db.Column(String(120), unique=True)
    tutor = db.Column(Boolean, default=False)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User [{self.id}] - {self.name}>'
