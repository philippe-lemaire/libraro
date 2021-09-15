from datetime import datetime
from isbnlib import meta
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import main
from app.models import Book
from .forms import DeleteBookForm, IsbnForm, BookForm, BookUpdateForm

from .. import db
from .. import config


@main.route("/")
def index():

    if current_user.is_authenticated:
        books = (
            Book.query.filter_by(user_id=current_user.id)
            .order_by(desc(Book.last_updated))
            .limit(5)
            .all()
        )
    else:
        books = []
    return render_template("index.html", current_time=datetime.utcnow(), books=books)


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
        book.title = book_response["Title"]
        book.authors = ", ".join(book_response["Authors"])
        book.year = book_response["Year"]
        book.last_updated = datetime.now()
        print(book.last_updated)
        book.read = False

    if bookform.submit2.data and bookform.validate():
        book.title = bookform.title.data
        book.isbn13 = bookform.isbn13.data
        book.authors = bookform.authors.data
        book.year = bookform.year.data
        book.read = bookform.read.data
        book.user_id = current_user.id
        book.last_updated = datetime.utcnow()
        print(book.title)
        db.session.add(book)
        db.session.commit()
        flash(f"{book.title} by {book.authors} has been added to your Libraro.")
        return redirect(url_for("main.index"))
    # fill in the book form
    bookform.isbn13.data = book.isbn13
    bookform.title.data = book.title
    bookform.authors.data = book.authors
    bookform.year.data = book.year
    return render_template(
        "add_a_book.html", form=form, bookform=bookform, searched=searched, book=book
    )


@main.route("/edit/book/<int:id>", methods=["GET", "POST"])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    if current_user.id != book.user_id:
        abort(403)
    # create and fill the bookform with book data
    bookform = BookUpdateForm()
    deleteform = DeleteBookForm()
    if bookform.submit2.data and bookform.validate():
        book.title = bookform.title.data
        book.authors = bookform.authors.data
        book.year = bookform.year.data
        book.read = bookform.read.data
        book.last_updated = datetime.utcnow()
        db.session.add(book)
        db.session.commit()
        flash(f"{book.title} by {book.authors} has been updated in your Libraro.")
        return redirect(url_for("main.my_books"))

    bookform.isbn13.data = book.isbn13
    bookform.title.data = book.title
    bookform.authors.data = book.authors
    bookform.year.data = book.year
    bookform.read.data = book.read
    if deleteform.validate_on_submit():
        db.session.delete(book)
        db.session.commit()
        flash(f"{book.title} by {book.authors} has been removed from your Libraro.")
        return redirect(url_for("main.my_books"))
    return render_template(
        "edit_book.html", bookform=bookform, deleteform=deleteform, book=book
    )


@main.route("/delete/book/<int:id>")
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    if current_user.id != book.user_id:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash(f"{book.title} by {book.authors} has been removed from your Libraro.")
    return redirect(url_for("main.my_books"))


@main.route("/my_books")
@login_required
def my_books():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template("my_books.html", books=books)


@main.route("/my_books/<authors>")
@login_required
def my_books_by_author(authors):
    books = (
        Book.query.filter(Book.authors.like(authors))
        .filter_by(user_id=current_user.id)
        .all()
    )
    return render_template("my_books.html", books=books, authors=authors)


@main.route("/my_authors")
@login_required
def my_authors():
    books = Book.query.filter_by(user_id=current_user.id).all()
    authors = [book.authors for book in books]
    authors = list(set(authors))
    return render_template("my_authors.html", authors=authors)
