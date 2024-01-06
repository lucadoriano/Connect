from flask_wtf import FlaskForm

from wtforms import (
    EmailField,
    PasswordField,
    StringField,
    TextAreaField,
    FileField,
    RadioField
)

from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

from core.models import User
from core.auth import current_user
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    type = RadioField(
        'I want to join as a:',
        choices=["Student", "Tutor"], 
        validators=[DataRequired()]
    )
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match'),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_username(self, field):
        if User.find_by_username(username=field.data):
            raise ValidationError('Username not available')

    def validate_email(self, field):
        if User.find_by_email(email=field.data):
            raise ValidationError('User already exist')

class ProfileForm(FlaskForm):
    image = FileField('Image')
    fullname = StringField('Fullname')
    description = StringField('Description')
    skills = StringField('Skills')
    about = TextAreaField('About')

    def validate_skills(self, field):
        skills = field.data.split(',')

        if len(skills) > 4:
            raise ValidationError('Too many skills (max 4)')

        for skill in skills:
            if not skill.strip():
                raise ValidationError('Skills should not contain empty values')

        if field.data.endswith(' ,'):
            field.data = field.data[:-2]

class MessageForm(FlaskForm):
    recipient = StringField('Recipient', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired()])

    def validate_recipient(self, field):
        if field.data == current_user.username:
            raise ValidationError('Cannot send a message to yourself')

class RoomForm(FlaskForm):
    callee = StringField('Callee', validators=[DataRequired()])

    def validate_callee(self, field):
        if field.data == current_user.username:
            raise ValidationError('Cannot call yourself')

        if not User.find_by_username(username=field.data):
            raise ValidationError('User doesn\'t exist')

class MarkdownForm(FlaskForm):
    markdown = TextAreaField('Markdown', id='markdown')