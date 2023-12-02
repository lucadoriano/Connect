from flask import render_template

from core import app
from core.auth import load_user

@app.route('/')
def home():
    return render_template('home.html')