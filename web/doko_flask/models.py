from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class Ruleset(db.Model):
    __tablename__ = "rulesets"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=False), default=func.now(), nullable=False)
    sittings = db.relationship("Table", backref="Ruleset", passive_deletes=True)


class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey("tables.id", ondelete="CASCADE"))


class Table(db.Model):
    __tablename__ = "tables"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    ruleset_id = db.Column(db.Integer, db.ForeignKey("rulesets.id", ondelete="CASCADE"))
    games = db.relationship("Game", backref="Table", passive_deletes=True)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime(timezone=False), default=func.now(), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
