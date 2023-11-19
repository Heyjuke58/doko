from sqlalchemy.sql import func

from .. import db


class Table(db.Model):
    __tablename__ = "tables"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    date_created = db.Column(
        db.DateTime(timezone=False), default=func.now(), nullable=False
    )
    ruleset_id = db.Column(db.Integer, db.ForeignKey("rulesets.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    games = db.relationship("Game", backref="Table")

    def __init__(self, name, password, ruleset_id, user_id) -> None:
        self.name = name
        self.password = password
        self.ruleset_id = ruleset_id
        self.user_id = user_id
