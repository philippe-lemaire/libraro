from typing import BinaryIO, Text
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import (
    StringField,
    RadioField,
    TextAreaField,
    BooleanField,
    SubmitField,
    PasswordField,
    ValidationError,
    FileField,
)
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, Optional
from app.models import User


class IsbnForm(FlaskForm):
    isbn13 = StringField("ISBN13", validators=[DataRequired()])
    submit1 = SubmitField("Look up this book")


class BookForm(FlaskForm):
    isbn13 = StringField("ISBN", render_kw={"readonly": True})
    title = StringField("Title", validators=[DataRequired()])
    authors = StringField("Authors", validators=[DataRequired()])
    publisher = StringField("Publisher", validators=[Length(max=128)])
    year = StringField("year", validators=[DataRequired(), Length(max=4)])
    read = BooleanField("read")
    user_review_stars = RadioField(choices=range(1, 6), validators=[Optional()])
    user_review_text = TextAreaField(validators=[Length(max=256), Optional()])
    to_trade = BooleanField("To trade")
    submit2 = SubmitField("Add this book")


class BookUpdateForm(BookForm):
    submit2 = SubmitField("Update this book")


class DeleteBookForm(FlaskForm):
    submit = SubmitField("Remove this book")


class ProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 128), Email()])
    username = StringField("Username", validators=[DataRequired()])
    picture = FileField(label="Upload a profile picture")
    bio = TextAreaField(validators=[Length(max=256), Optional()])
    street_address = StringField(validators=[Length(max=128), Optional()])
    zip_code = IntegerField(validators=[Optional()])
    city = StringField(validators=[Length(max=256), Optional()])
    country = StringField(validators=[Length(max=256), Optional()])
    password = PasswordField(
        "Update password",
        validators=[
            EqualTo("password2", message="Passwords must match."),
        ],
    )
    password2 = PasswordField("Confirm new password")
    submit = SubmitField("Update profile")
