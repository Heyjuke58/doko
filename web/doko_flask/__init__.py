import os

from flask import Flask, jsonify, send_from_directory
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

app = Flask(__name__)
app.config.from_object("doko_flask.config.Config")
db.init_app(app)

from .views.auth import auth_views
from .views.create_table import create_table_view
from .views.lobby import lobby_view

app.register_blueprint(lobby_view, url_prefix="/")
app.register_blueprint(create_table_view, url_prefix="/")
app.register_blueprint(auth_views, url_prefix="/")

from .models.game import Game
from .models.ruleset import Ruleset
from .models.table import Table
from .models.user import User

if os.getenv("FLASK_DEBUG", False):
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        print("Created fresh database")

login_manager = LoginManager()
login_manager.login_view = "auth_views.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.config["STATIC_FOLDER"], "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)
