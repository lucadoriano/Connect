from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from core import settings

app = Flask(__name__, 
            static_folder=settings.STATIC_FOLDER,
            template_folder=settings.TEMPLATE_FOLDER)
            
app.config["SQLALCHEMY_DATABASE_URI"] = settings.POSTGRES_URI
app.config["TEMPLATES_AUTO_RELOAD"] = settings.DEBUG
app.secret_key = 'secret-key' #change in production

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db, command='migrate')

Base = db.Model

def init_db():
    from core.models import User
    db.create_all()

with app.app_context():
    init_db()