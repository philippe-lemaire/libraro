from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_a_book")
def add_a_book():
    return render_template("add_a_book.html")
