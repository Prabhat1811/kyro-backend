from .database import db
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

class LikedShows(db.Model):
    __tablename__ = 'liked_shows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.String, nullable=False)

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.String, nullable=False)
