import uuid

from datetime import datetime
from pytz import timezone

from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Boolean, UUID, Integer, String, ForeignKey, DateTime

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    email = db.Column(String(120), unique=True)
    username = db.Column(String(60), nullable=True)
    password = db.Column(String(300), nullable=False)
    
    profile = db.relationship(
        'Profile', 
        backref='user', 
        uselist=False, 
        lazy='joined',
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
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()
    
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

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(UUID, ForeignKey('user.id'), unique=True, nullable=False)
    image = db.Column(String, nullable=True)
    fullname = db.Column(String(100), nullable=True)
    description = db.Column(String(100), nullable=True)
    about = db.Column(String, nullable=True)
    skills = db.Column(String(500), default='', nullable=True)
    tutor = db.Column(Boolean, default=False)

    messages_sent = db.relationship(
        'Message', 
        back_populates='sender_profile',
        foreign_keys='Message.sender_id'
    )
    messages_received = db.relationship(
        'Message', 
        back_populates='recipient_profile',
        foreign_keys='Message.recipient_id'
    )
    notes_created = db.relationship(
        'Note',
        back_populates='author_profile',
        foreign_keys='Note.author_id'
    )

    def __init__(self, user_id):
        self.user_id = user_id
    
    def __repr__(self):
        return f'<Profile [{self.id}] - {self.fullname}>'
    

class Message(db.Model):
    id = db.Column(Integer, primary_key=True)
    sender_id = db.Column(UUID, ForeignKey('profile.user_id'), nullable=False)
    recipient_id = db.Column(UUID, ForeignKey('profile.user_id'), nullable=False)
    body = db.Column(String, nullable=False)
    timestamp = db.Column(DateTime(timezone=True))

    sender_profile = db.relationship(
        'Profile', 
        back_populates='messages_sent',
        foreign_keys='Message.sender_id'
    )
    recipient_profile = db.relationship(
        'Profile',
        back_populates='messages_received',
        foreign_keys='Message.recipient_id'
    )

    def __init__(self, sender_id, recipient_id, body):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.body = body
        self.timestamp = datetime.now(tz=timezone('Europe/Rome'))

    def __repr__(self):
        return f'<Message [{self.id}]>'


    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e


class Room(db.Model):
    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    caller = db.Column(String(60), nullable=False)
    callee = db.Column(String(60), nullable=False)

    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee
        
    @classmethod
    def find_by_id(cls, id: uuid):
        return cls.query.filter_by(id=id).first()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e


class Note(db.Model):
    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    author_id = db.Column(UUID, ForeignKey('profile.user_id'), nullable=False)
    content = db.Column(String, nullable=False)
    timestamp = db.Column(DateTime, default=datetime.now())
    archived = db.Column(Boolean, default=False)

    author_profile = db.relationship(
        'Profile', 
        back_populates='notes_created',
        foreign_keys='Note.author_id'
    )


    @classmethod
    def get_author(cls, id):
        return cls.query.get(id).author_id

    @classmethod
    def public(cls):
        return cls.query.filter_by(archived=False).order_by(Note.timestamp.desc())
    
    @classmethod
    def authored(cls, author):
        return cls.query.filter_by(archived=False, author_id=author)\
            .order_by(Note.timestamp.desc())

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e