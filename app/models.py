from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, TINYTEXT, TEXT, DATE, DATETIME, BOOLEAN, DECIMAL

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(INTEGER(unsigned = True), primary_key=True)
    username = db.Column(TINYTEXT, unique=False, nullable=False)
    login = db.Column(TINYTEXT, unique=True, nullable=False)
    password = db.Column(TEXT, unique=False, nullable=False)
    admin = db.Column(BOOLEAN, unique=False, nullable=False, default=0)
    image = db.Column(TEXT, unique=False, nullable=True)

    order = db.relationship("Order", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(INTEGER(unsigned = True), primary_key=True)
    time = db.Column(DATETIME, unique=False, nullable=False)
    user_id = db.Column(INTEGER(unsigned = True), db.ForeignKey("user.id"), nullable=False)

    order_comic = db.relationship("Order_comic", backref="order", lazy=True)

    def __repr__(self):
        return '<Order %r>' % self.id


class Publisher(db.Model):
    __tablename__ = "publisher"

    id = db.Column(INTEGER(unsigned = True), primary_key=True)
    title = db.Column(TINYTEXT, unique=False, nullable=False)
    contact = db.Column(TEXT, nullable=True)
    image = db.Column(TEXT, unique=False, nullable=True)

    comic = db.relationship("Comic", backref="publicher", lazy=True)

    def __repr__(self):
        return '<Publisher %r>' % self.id


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(INTEGER(unsigned = True), primary_key=True)
    fio = db.Column(TINYTEXT, unique=False, nullable=False)
    bio = db.Column(TEXT, unique=False, nullable=True)
    image = db.Column(TEXT, unique=False, nullable=True)

    comic = db.relationship("Comic", backref="author", lazy=True)

    def __repr__(self):
        return '<Author %r>' % self.id


class Comic(db.Model):
    __tablename__ = "comic"

    id = db.Column(INTEGER(unsigned = True), primary_key=True)
    title = db.Column(TINYTEXT, unique=False, nullable=False)
    description = db.Column(TEXT, unique=False, nullable=True)
    price = db.Column(DECIMAL(precision=19, scale=2), unique=False, nullable=False)
    year = db.Column(DATE, unique=False, nullable=True)
    image = db.Column(TEXT, unique=False, nullable=True)
    publisher_id = db.Column(INTEGER(unsigned = True), db.ForeignKey("publisher.id"), nullable=False)
    author_id = db.Column(INTEGER(unsigned = True), db.ForeignKey("author.id"), nullable=False)

    order_comic = db.relationship("Order_comic", backref="comic", lazy=True)
    genre_comic = db.relationship("Genre_comic", backref="comic", lazy=True)

    def __repr__(self):
        return '<Comic %r>' % self.id


class Order_comic(db.Model):
    __tablename__ = "order_comic"

    id = db.Column(INTEGER(unsigned = True), primary_key=True)
    count = db.Column(TINYINT(unsigned = True), unique=False, nullable=False, default=1)
    order_id = db.Column(INTEGER(unsigned = True), db.ForeignKey("order.id"), nullable=False)
    comic_id = db.Column(INTEGER(unsigned = True), db.ForeignKey("comic.id"), nullable=False)

    def __repr__(self):
        return '<Order_comic %r>' % self.id


class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column(INTEGER(unsigned = True), primary_key=True)
    title = db.Column(TINYTEXT, unique=True, nullable=False)

    genre_comic = db.relationship("Genre_comic", backref="genre", lazy=True)

    def __repr__(self):
        return '<Genre %r>' % self.genre


class Genre_comic(db.Model):
    __tablename__ = "genre_comic"

    comic_id = db.Column(INTEGER(unsigned = True), db.ForeignKey("comic.id"), primary_key=True, nullable=False)
    genre_id = db.Column(INTEGER(unsigned = True), db.ForeignKey("genre.id"), primary_key=True, nullable=False)

    def __repr__(self):
        return '<Genre_comic %r>' % self.id

