import os

from flask import Flask, jsonify, send_from_directory
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

app = Flask(__name__)
app.config.from_object("doko_flask.config.Config")
db.init_app(app)

from .auth import auth
from .views import views

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

from .models import Game, Ruleset, Table, User

if os.getenv("FLASK_DEBUG", False):
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        print("Created fresh database")

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# @app.route("/static/<path:filename>")
# def staticfiles(filename):
#     return send_from_directory(app.config["STATIC_FOLDER"], filename)
