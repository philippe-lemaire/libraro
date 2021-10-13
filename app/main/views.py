from datetime import datetime
from isbnlib import meta
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import main
from app.models import Book, User
from .forms import DeleteBookForm, IsbnForm, BookForm, BookUpdateForm, ProfileForm

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
        book.title = book_response["Title"]
        book.authors = ", ".join(book_response["Authors"])
        book.year = book_response["Year"]
        book.read = False

    if bookform.submit2.data and bookform.validate():
        book.title = bookform.title.data
        book.isbn13 = bookform.isbn13.data
        book.authors = bookform.authors.data
        book.year = bookform.year.data
        book.read = bookform.read.data
        book.user_id = current_user.id
        book.last_updated = datetime.utcnow()
        book.publisher = bookform.publisher.data
        book.user_review_stars = bookform.user_review_stars.data
        book.user_review_text = bookform.user_review_text.data
        book.to_trade = bookform.to_trade.data
        db.session.add(book)
        db.session.commit()
        flash(f"{book.title} by {book.authors} has been added to your Libraro.")
        return redirect(url_for("main.add_a_book"))
    # fill in the book form
    bookform.isbn13.data = book.isbn13
    bookform.title.data = book.title
    bookform.authors.data = book.authors
    bookform.year.data = book.year
    bookform.publisher.data = book.publisher
    bookform.user_review_stars.data = book.user_review_stars
    bookform.user_review_text.data = book.user_review_text
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
        book.publisher = bookform.publisher.data
        book.user_review_stars = (
            int(bookform.user_review_stars.data)
            if bookform.user_review_stars.data
            else ""
        )
        book.user_review_text = bookform.user_review_text.data
        book.to_trade = bookform.to_trade.data
        db.session.commit()
        flash(f"{book.title} by {book.authors} has been updated in your Libraro.")
        return redirect(url_for("main.my_books"))

    bookform.isbn13.data = book.isbn13
    bookform.title.data = book.title
    bookform.authors.data = book.authors
    bookform.year.data = book.year
    bookform.read.data = book.read
    bookform.publisher.data = book.publisher
    bookform.user_review_stars.data = str(book.user_review_stars)
    bookform.user_review_text.data = book.user_review_text
    bookform.to_trade.data = book.to_trade

    if deleteform.submit.data and deleteform.validate():
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
    num_books_per_author = []
    for author in authors:
        books_by_author = [book for book in books if book.authors == author]
        num_books_per_author.append(len(books_by_author))
    authors = zip(authors, num_books_per_author)
    return render_template("my_authors.html", authors=authors)


@main.route("/my_profile", methods=["GET", "POST"])
@login_required
def my_profile():
    profileform = ProfileForm()

    if profileform.validate_on_submit():
        # update the user and commit to db
        current_user.username = profileform.username.data
        current_user.email = profileform.email.data
        current_user.bio = profileform.bio.data
        current_user.street_address = profileform.street_address.data
        current_user.zip_code = profileform.zip_code.data
        current_user.city = profileform.city.data
        current_user.country = profileform.country.data
        current_user.password = profileform.password.data

        flash("Profile updated")
        db.session.commit()
        return redirect(url_for("main.index"))

    # fill in the form before rendering
    profileform.username.data = current_user.username
    profileform.email.data = current_user.email
    profileform.bio.data = current_user.bio
    profileform.street_address.data = current_user.street_address
    profileform.zip_code.data = current_user.zip_code
    profileform.city.data = current_user.city
    profileform.country.data = current_user.country
    return render_template("my_profile.html", profileform=profileform)


@main.route("/for_trade")
def for_trade():
    books_for_trade = (
        Book.query.filter_by(to_trade=True)
        .join(User)
        .add_columns(User.username, User.city)
        .all()
    )
    return render_template("for_trade.html", books_for_trade=books_for_trade)


@main.route("/for_trade/<city>")
def for_trade_by_city(city):
    books_for_trade = (
        Book.query.filter_by(to_trade=True)
        .join(User)
        .add_columns(User.username, User.city)
        .filter_by(city=city)
        .all()
    )
    return render_template("for_trade.html", books_for_trade=books_for_trade)


@main.route("/user/<int:id>")
def user_page(id):
    user = User.query.get_or_404(id)
    return render_template("user_page.html", user=user)
