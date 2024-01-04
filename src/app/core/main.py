import os

from flask import render_template, redirect, url_for, request

from werkzeug.utils import secure_filename

from markdown import markdown

from core import app
from core.settings import WS_URL
from core.auth import current_user, login_required, load_user
from core.models import User, Profile, Message, Room, Note
from core.forms import ProfileForm, MessageForm, RoomForm, MarkdownForm


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/profile/', methods=["GET", "POST"])
@app.route('/profile/<string:username>/')
@login_required
def profile(username=None):
    form = ProfileForm()
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

        if image.filename:
            rename_image = secure_filename(f'{str(user.id)}{image_file_type}')
            for file in os.listdir(app.config['UPLOAD_FOLDER']):
                if file.startswith(str(user.id)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], rename_image))
            
        if form.image.data:
            user.profile.image = url_for(
                'static', filename=f'img/profile/{rename_image}'
            )
        user.profile.fullname = form.fullname.data
        user.profile.description = form.description.data
        user.profile.skills = ", ".join(skills)
        user.profile.about = form.about.data
        user.save()
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form, user=user)


@app.route('/tutors/')
@login_required
def tutors():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    tutors = Profile.query.filter_by(tutor=True).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template('tutors.html', tutors=tutors)


@app.route('/notes/', methods=["GET", "POST"])
@login_required
def notes():
    form = MarkdownForm()
    filter = request.args.get('filter')
    if not filter:
        notes = Note.public()
    if filter == 'authored':
        notes = Note.authored(current_user.id)
        
    parsed_notes = []
    for note in notes:
       note.content = markdown(note.content)
       parsed_notes.append(note)

    if form.validate_on_submit():
        if form.markdown.data:
            new_note = Note(
                author_id=current_user.id,
                content=form.markdown.data
            )
            new_note.save()
        return redirect(url_for('notes'))
    return render_template('notes.html', notes=parsed_notes, form=form)


@app.route('/note/delete/<uuid:note>/', methods=["POST"])
@login_required
def delete_note(note):
    delete_note = Note.query.get(str(note))
    if delete_note:
        if Note.get_author(str(note)) == current_user.id:
            delete_note.delete()
    return redirect(url_for('notes'))


@app.route('/inbox/', methods=["GET", "POST"])
@app.route('/inbox/<string:profile>/', methods=["GET", "POST"])
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
        return redirect(url_for('inbox'))
    return render_template('inbox.html', profile=profile, form=form, user=current_user)


@app.route('/room/', methods=["GET", "POST"])
@app.route('/room/<uuid:uuid>/', methods=["GET", "POST"])
@login_required
def room(uuid=None):
    form = RoomForm()
    if form.validate_on_submit():
        create_room = Room(
            caller=current_user.username,
            callee=form.callee.data
        )
        create_room.save()
        uuid = create_room.id
        return redirect(url_for('room', uuid=uuid))
    room = Room.find_by_id(id=uuid)
    return render_template(
        'room.html', ws_url=WS_URL, form=form, room=room, user=current_user
    )