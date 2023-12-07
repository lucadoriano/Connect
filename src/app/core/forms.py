import json

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

from core.models import User

class JSONField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = json.loads(valuelist[0])
        else:
            self.data = None

    def pre_validate(self, form):
        super().pre_validate(form)
        if self.data:
            if not isinstance(self.data, list):
                raise ValueError('Field must be a list.')
            for item in self.data:
                json.dumps(item)

    def _value(self):
        return json.dumps(self.data) if self.data else ''
    
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
    fullname = StringField('Fullname')
    description = StringField('Description')
    skills = StringField('Skills')

    def validate_skills(self, field):
        if len(field.data.split(',')) > 4:
            raise ValidationError('Too many skills (max 4)')
