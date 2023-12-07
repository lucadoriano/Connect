import os

DEBUG = True

POSTGRES_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'

TEMPLATE_FOLDER = os.path.abspath('./../app/templates')
STATIC_FOLDER = os.path.abspath('./../app/static')

DEFAULT_PROFILE = {
    "photo": "http://127.0.0.1:5000/static/img/default-profile-image.png",
    "fullname": "",
    "description": "",
    "skills": [],
}