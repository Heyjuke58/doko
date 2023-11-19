from doko_flask import app, db
from doko_flask.models.user import User
from flask.cli import FlaskGroup

cli = FlaskGroup(app)
# app = create_app()


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command("seed_db")
# def seed_db():
#     db.session.add(User("hauke@hinrichs.org", "hauke", "12345"))
#     db.session.commit()


if __name__ == "__main__":
    cli()
