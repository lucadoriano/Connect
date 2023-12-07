from flask import render_template, redirect, url_for

from core import app, db
from core.auth import load_user, current_user, login_required
from core.models import User
from core.forms import Profile

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/profile', methods=["GET", "POST"])
@app.route('/profile/<uuid>')
@login_required
def profile(uuid=None):
    form = Profile()
    if not uuid:
        uuid = current_user.id
    try:
        user = User.query.filter_by(id=uuid).first()
    except:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        tmp = [x.replace(" ", "") for x in form.skills.data.split(",")]
        test = [{"name": skill} for skill in tmp]
        skills = []
        skills.extend(test)
        
        user.profile["fullname"] = form.fullname.data
        user.profile["description"] = form.description.data
        user.profile["skills"] = skills
        db.session.commit()
    return render_template('profile.html', form=form, user=user)