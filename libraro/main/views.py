from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
import forms
from .. import db
from ..models import User


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/add_a_book")
def add_a_book():
    return render_template("add_a_book.html")
