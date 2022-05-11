from datetime import datetime

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'
    serialize_only = ('name', 'date', 'message','user_id')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=True, unique=False)
    date = db.Column(db.DateTime, nullable=True, unique=False)
    message = db.Column(db.String(300), nullable=True, unique=False)
    is_completed = db.Column('is_completed', db.Boolean(), nullable=False, server_default='0')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks", uselist=False)

    def __init__(self, name, date, message, user_id):
        self.name = name
        self.date = date
        self.message = message
        self.user_id = user_id

    def serialize(self):
        return {
            'name': self.name,
            'message': self.message,
            'date': self.date,
            'user_id': self.user_id
        }


class Song(db.Model,SerializerMixin):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    artist = db.Column(db.String(300), nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="songs", uselist=False)

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    serialize_only = ('title', 'longitude', 'latitude')


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    longitude = db.Column(db.String(300), nullable=True, unique=False)
    latitude = db.Column(db.String(300), nullable=True, unique=False)
    population = db.Column(db.Integer, nullable=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates="locations", uselist=False)

    def __init__(self, title, longitude, latitude, population):
        self.title = title
        self.longitude = longitude
        self.latitude = latitude
        self.population = population

    def serialize(self):
        return {
            'title': self.title,
            'long': self.longitude,
            'lat': self.latitude,
        }


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    songs = db.relationship("Song", back_populates="user", cascade="all, delete")
    locations = db.relationship("Location", back_populates="user", cascade="all, delete")
    tasks = db.relationship("Task", back_populates="user", cascade="all, delete")

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email


