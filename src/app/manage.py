from flask.cli import FlaskGroup
from core.main import app

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()