import os

DEBUG = True

POSTGRES_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres'

TEMPLATE_FOLDER = os.path.abspath('./../app/templates')
STATIC_FOLDER = os.path.abspath('./../app/static')