from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .. import db
from ..models.table import Table

lobby_view = Blueprint("lobby_view", __name__)


@lobby_view.route("/")
@login_required
def lobby():
    tables = Table.query.all()
    return render_template("lobby.html", user=current_user, tables=tables)
