import os

from flask import render_template, redirect, url_for

from werkzeug.utils import secure_filename

from core import app
from core.auth import current_user, login_required, load_user
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
        user = User.find_by_id(uuid)
    except:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        skills = [skill.replace(" ", "") for skill in form.skills.data.split(",")]

        image = form.image.data
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        user.profile.image = url_for('static', filename=f'img/profile/{image_filename}')
        user.profile.fullname = form.fullname.data
        user.profile.description = form.description.data
        user.profile.skills = ", ".join(skills)
        user.profile.about = form.about.data
        user.save()
    return render_template('profile.html', form=form, user=user)