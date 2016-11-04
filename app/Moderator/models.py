from werkzeug import check_password_hash, generate_password_hash
from flask_login import UserMixin

from app import db


class Moderator(db.Model, UserMixin):

    __tablename__ = 'moderator'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    name = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(198), nullable=False, unique=True)
    passhash = db.Column(db.String(500), nullable=False)

    def __init__(self, name, email, passhash):
        self.name = name
        self.email = email
        self.passhash = passhash

    def __repr__(self):
        return '<Moderator %r' % self.name

    @classmethod
    def create(cls, name, email, password):
        pwhash = generate_password_hash(password)
        user = Moderator(name, email, pwhash)
        return user

    def validate(self, password):
        return check_password_hash(self.passhash, password)
