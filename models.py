from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=False, nullable=False)
    login = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=False, nullable=False)
    admin = db.Column(db.Integer, unique=False, nullable=False, default=0)
    image = db.Column(db.LargeBinary, unique=False, nullable=True)

    order = db.relationship("Order", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Text, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    order_comic = db.relationship("Order_comic", backref="order", lazy=True)

    def __repr__(self):
        return '<Order %r>' % self.id


class Publisher(db.Model):
    __tablename__ = "publisher"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=False, nullable=False)
    contact = db.Column(db.Text, nullable=True)
    image = db.Column(db.LargeBinary, unique=False, nullable=True)

    comic = db.relationship("Comic", backref="publicher", lazy=True)

    def __repr__(self):
        return '<Publisher %r>' % self.id


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.Text, unique=False, nullable=False)
    bio = db.Column(db.Text, unique=False, nullable=True)
    image = db.Column(db.LargeBinary, unique=False, nullable=True)

    comic = db.relationship("Comic", backref="author", lazy=True)

    def __repr__(self):
        return '<Author %r>' % self.id


class Comic(db.Model):
    __tablename__ = "comic"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    year = db.Column(db.Integer, unique=False, nullable=True)
    image = db.Column(db.LargeBinary, unique=False, nullable=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    order_comic = db.relationship("Order_comic", backref="comic", lazy=True)
    genre_comic = db.relationship("Genre_comic", backref="comic", lazy=True)

    def __repr__(self):
        return '<Comic %r>' % self.id


class Order_comic(db.Model):
    __tablename__ = "order_comic"

    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, unique=False, nullable=False, default=1)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    comic_id = db.Column(db.Integer, db.ForeignKey("comic.id"), nullable=False)

    def __repr__(self):
        return '<Order_comic %r>' % self.id


class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)

    genre_comic = db.relationship("Genre_comic", backref="genre", lazy=True)

    def __repr__(self):
        return '<Genre %r>' % self.genre


class Genre_comic(db.Model):
    __tablename__ = "genre_comic"

    id = db.Column(db.Integer, primary_key=True)
    comic_id = db.Column(db.Integer, db.ForeignKey("comic.id"), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)

    def __repr__(self):
        return '<Genre_comic %r>' % self.id

