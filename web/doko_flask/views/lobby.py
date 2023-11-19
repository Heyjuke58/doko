from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .. import db
from ..models.table import Table

lobby_view = Blueprint("lobby_view", __name__)


@lobby_view.route("/")
@login_required
def lobby():
    tables = Table.query.all()
    page = int(request.args.get("page", 1))

    pagination = db.paginate(
        db.select(Table).order_by(Table.date_created),
        max_per_page=8,
        page=page,
        per_page=8,
    )
    return render_template(
        "lobby.html",
        user=current_user,
        # tables=tables,
        pagination=pagination,
        data_to_show=pagination.items,
    )
