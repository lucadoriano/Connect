import uuid

from sqlalchemy import Boolean, UUID, Integer, String, JSON
from sqlalchemy.ext.mutable import MutableDict
from flask_login import UserMixin
from core import db, Base
from core import settings


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    email = db.Column(String(120), unique=True)
    username = db.Column(String(60), nullable=True)
    password = db.Column(String(300), nullable=False)
    tutor = db.Column(Boolean, default=False)
    profile = db.Column(MutableDict.as_mutable(JSON), nullable=True)

    def __init__(self, email, password, username,
                 profile=settings.DEFAULT_PROFILE):
        self.email = email
        self.username = username
        self.password = password
        self.profile = profile

    def __repr__(self):
        return f'<User [{self.id}] - {self.username}>'