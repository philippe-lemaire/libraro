from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
Bootstrap(app)

# SQL Setup with sqlite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data/data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_a_book")
def add_a_book():
    return render_template("add_a_book.html")
