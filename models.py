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

    def __repr__(self):
        return '<User %r>' % self.username