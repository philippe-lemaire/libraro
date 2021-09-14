from datetime import datetime, date
from operator import methodcaller
from isbnlib import meta
from flask import render_template, session, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from wtforms.fields.simple import SubmitField
from . import main
from app.models import User, Book
from .forms import IsbnForm, BookForm, BookUpdateForm

from .. import db
from .. import config


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/add_a_book", methods=["GET", "POST"])
@login_required
def add_a_book():
    form = IsbnForm()
    bookform = BookForm()
    book = Book()
    searched = False
    if form.submit1.data and form.validate():
        searched = True
        isbn = form.isbn13.data
        service = config.get("SERVICE") or "goob"
        book_response = meta(isbn, service=service)
        book.isbn13 = book_response["ISBN-13"]
        book.user_id = current_user.id
        book.title = book_response["Title"]
        book.authors = ", ".join(book_response["Authors"])
        book.year = book_response["Year"]
        book.last_updated = datetime.now()
        book.read = False
        # fill in the book form
        bookform.isbn13.data = book.isbn13
        bookform.title.data = book.title
        bookform.authors.data = book.authors
        bookform.year.data = book.year
    if bookform.submit2.data and bookform.validate():
        book.title = bookform.title.data
        book.authors = bookform.authors.data
        book.year = bookform.year.data
        book.read = bookform.read.data
        db.session.add(book)
        db.session.commit()
        flash(f"{book.title} by {book.authors} has been added to your Libraro.")
        return redirect(url_for("main.index"))
    return render_template(
        "add_a_book.html", form=form, bookform=bookform, searched=searched
    )


@main.route("/my_books")
@login_required
def my_books():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template("my_books.html", books=books)


@main.route("/edit/book/<int:id>", methods=["GET", "POST"])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    if current_user.id != book.user_id:
        abort(403)
    # create and fill the bookform with book data
    bookform = BookUpdateForm()

    if bookform.submit2.data and bookform.validate():
        book.title = bookform.title.data
        book.authors = bookform.authors.data
        book.year = bookform.year.data
        book.read = bookform.read.data
        db.session.add(book)
        db.session.commit()
        flash(f"{book.title} by {book.authors} has been updated in your Libraro.")
        return redirect(url_for("main.my_books"))

    bookform.isbn13.data = book.isbn13
    bookform.title.data = book.title
    bookform.authors.data = book.authors
    bookform.year.data = book.year
    return render_template("edit_book.html", bookform=bookform, book=book)
