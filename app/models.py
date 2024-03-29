from logging import NullHandler
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from flask_login import UserMixin


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128))
    books = db.relationship("Book", backref="user")
    bio = db.Column(db.String(256))
    street_address = db.Column(db.String(128))
    zip_code = db.Column(db.Integer)
    city = db.Column(db.String(128))
    country = db.Column(db.String(64))
    picture = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.username


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    isbn13 = db.Column(db.String(64))
    title = db.Column(db.String(128))
    authors = db.Column(db.String(128))
    publisher = db.Column(db.String(128))
    year = db.Column(db.String(64))
    language = db.Column(db.String(128), nullable=True)
    last_updated = db.Column(db.DateTime())
    read = db.Column(db.Boolean())
    to_trade = db.Column(db.Boolean())
    user_review_stars = db.Column(db.Integer, nullable=True)
    user_review_text = db.Column(db.String(256), nullable=True)
    cover = db.Column(db.String(256), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
