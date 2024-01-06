import os

from dotenv import load_dotenv

from sqlalchemy import URL

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv(os.path.join(BASE_DIR, '.env'))

DEBUG = True
DATABASE = URL.create(
    'postgresql+psycopg2',
    username='user',
    password=os.environ.get('DATABASE_PASSWORD', 'demo1234'),
    host='postgres', #fetches internal docker-compose address, given its hostname
    port=5432,
    database='postgres'
)

SECRET_KEY = os.environ.get('SECRET_KEY', 'Chym09p5qFDBzJQg1A9VAwphByyndbe0')

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/img/profile') # change with docker volume
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

WS_URL = "ws://127.0.0.1/ws" #or tunneling/server address