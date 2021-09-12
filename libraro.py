import os
from .libraro import create_app, db
from .libraro.models import User, Role, Book
from flask_migrate import Migrate

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy


app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
