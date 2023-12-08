from flask import Flask

from core.models import db, migrate
from core import settings

app = Flask(
    __name__, 
    static_folder=settings.STATIC_FOLDER,
    template_folder=settings.TEMPLATE_FOLDER
)
app.secret_key = settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE
app.config["TEMPLATES_AUTO_RELOAD"] = settings.DEBUG
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER

def init_db():
    db.init_app(app)
    migrate.init_app(app, db, command='migrate')

    from core.models import User, Profile
    db.create_all()

def init_auth():
    from core.auth import login_manager
    login_manager.init_app(app)
    
with app.app_context():
    init_db()
    init_auth()