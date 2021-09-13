import os
from app import create_app, db
from app.models import Role, Book, User

# from libraro.models import User, Role, Book
from flask_migrate import Migrate

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy

current_config = os.getenv("FLASK_CONFIG") or "default"
print(current_config)
app = create_app(current_config)

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Book=Book)
