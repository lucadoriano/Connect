
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from core import app, login_manager, bcrypt, db
from core.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    ctx = 'register'
    email = request.form.get("email")
    if request.form.get("password"):
        password = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        new_user = User(email, password, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
    return render_template('auth.html', ctx=ctx)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            print(user.password)
            print(password)
            print(bcrypt.check_password_hash(password=password, pw_hash=user.password))
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("home"))
            else:
                pass
                #raise error here
    return render_template('auth.html')

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))