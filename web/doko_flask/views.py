from flask import Blueprint, render_template
from flask_login import current_user, login_required

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def lobby():
    return render_template("lobby.html", user=current_user)


@views.route("/create_table")
@login_required
def create_table():
    return render_template("create_table.html", user=current_user)
