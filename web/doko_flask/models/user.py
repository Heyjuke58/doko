from flask_login import UserMixin
from sqlalchemy.sql import func

from .. import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(
        db.DateTime(timezone=False), default=func.now(), nullable=False
    )
    tables = db.relationship("Table", backref="User")
    rulesets = db.relationship("Ruleset", backref="User")

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
