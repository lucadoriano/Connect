import os

from flask import render_template, redirect, url_for

from werkzeug.utils import secure_filename

from core import app
from core.auth import current_user, login_required, load_user
from core.models import User, Message
from core.forms import Profile, MessageForm


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/profile', methods=["GET", "POST"])
@app.route('/profile/<username>')
@login_required
def profile(username=None):
    form = Profile()
    if not username:
        username = current_user.username
    try:
        user = User.find_by_username(username)
    except:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        skills = [skill.replace(" ", "") for skill in form.skills.data.split(",")]

        image = form.image.data
        _image_filename, image_file_type = os.path.splitext(image.filename)

        rename_image = secure_filename(f'{str(user.id)}{image_file_type}')
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            if file.startswith(str(user.id)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], rename_image))
        
        if form.image.data:
            user.profile.image = url_for('static', filename=f'img/profile/{rename_image}')
        user.profile.fullname = form.fullname.data
        user.profile.description = form.description.data
        user.profile.skills = ", ".join(skills)
        user.profile.about = form.about.data
        user.save()
    return render_template('profile.html', form=form, user=user)


@app.route('/tutors')
@login_required
def tutors():
    return render_template('home.html')


@app.route('/notes')
@login_required
def notes():
    return render_template('home.html')

@app.route('/inbox', methods=["GET", "POST"])
@app.route('/inbox/<profile>', methods=["GET", "POST"])
@login_required
def inbox(profile=None):
    form = MessageForm()
    if form.validate_on_submit():
        recipient = User.find_by_username(username=form.recipient.data)
        if recipient:
            new_message = Message(
                sender_id=current_user.id,
                recipient_id=recipient.id,
                body=form.body.data
            )
            new_message.save()
    return render_template('inbox.html', form=form, user=current_user)

@app.route('/test/<room>')
def host(room):
    return render_template('test.html', room=room, user=current_user)
