from flask_wtf import FlaskForm

from wtforms import EmailField, PasswordField, StringField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

from core.models import User
    
class Login(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class Register(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match'),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('User already exist')

class Profile(FlaskForm):
    image = FileField('Image')
    fullname = StringField('Fullname')
    description = StringField('Description')
    skills = StringField('Skills')
    about = TextAreaField('About')

    def validate_skills(self, field):
        if len(field.data.split(',')) > 4:
            raise ValidationError('Too many skills (max 4)')