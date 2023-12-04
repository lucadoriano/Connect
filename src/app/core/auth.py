
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from core import app, login_manager, bcrypt, db
from core.models import User
from core.forms import Login, Register

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    if form.validate_on_submit():            
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=bcrypt.generate_password_hash(
                form.password.data
            ).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('auth.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
        except Exception as e:
            print(f'ERROR: {e}')
    return render_template('auth.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))