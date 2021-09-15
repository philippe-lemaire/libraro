from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import User


class IsbnForm(FlaskForm):
    isbn13 = StringField("ISBN13", validators=[DataRequired()])
    submit1 = SubmitField("Look up this book")


class BookForm(FlaskForm):
    isbn13 = StringField("ISBN13", render_kw={"readonly": True})
    title = StringField("Title", validators=[DataRequired()])
    authors = StringField("Authors", validators=[DataRequired()])
    year = StringField("year", validators=[DataRequired()])
    read = BooleanField("read")
    submit2 = SubmitField("Add this book")


class BookUpdateForm(BookForm):
    submit2 = SubmitField("Update this book")


class DeleteBookForm(FlaskForm):
    submit = SubmitField("Remove this book")


class ProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 128), Email()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Update profile")
