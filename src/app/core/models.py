import uuid

from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Boolean, UUID, Text, String, ForeignKey

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    email = db.Column(String(120), unique=True)
    username = db.Column(String(60), nullable=True)
    password = db.Column(String(300), nullable=False)
    tutor = db.Column(Boolean, default=False)
    profile = db.relationship(
        'Profile', backref='user', uselist=False, lazy='joined',
    )

    def __init__(self, email, password, username):
        self.email = email
        self.username = username
        self.password = password

        self.profile = Profile(user_id=self.id)

    def __repr__(self):
        return f'<User [{self.id}] - {self.username}>'
        
    @classmethod
    def find_by_id(cls, id: uuid):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e

class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID, ForeignKey('user.id'), unique=True, nullable=False)
    image = db.Column(String(), nullable=True)
    fullname = db.Column(String(100), nullable=True)
    description = db.Column(String(100), nullable=True)
    about = db.Column(String(500), nullable=True)
    skills = db.Column(String(500), default='', nullable=True)

    def __init__(self, user_id):
        self.user_id = user_id
    
    def __repr__(self):
        return f'<Profile [{self.id}] - {self.fullname}'