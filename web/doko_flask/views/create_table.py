from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from .. import db
from ..models.ruleset import Ruleset
from ..models.table import Table

create_table_view = Blueprint("create_table_view", __name__)


@create_table_view.route("/create-table", methods=["GET", "POST"])
@login_required
def create_table():
    # TODO: get request: get last ruleset of user if one exists and prefill values accordingly
    if request.method == "POST":
        new_ruleset = Ruleset(
            user_id=current_user.id,  # type: ignore
            nines=bool(int(request.form.get("nines"))),  # type: ignore
            dulle_rule=str(request.form.get("dulle")),
            reverse_dulle_rule=bool(int(request.form.get("reverse_dulle_rule"))),  # type: ignore
            announcement_counting=str(request.form.get("announcement_counting")),
            also_double_extra_points=bool(
                int(request.form.get("also_double_extra_points"))  # type: ignore
            ),
            mandatory_announcement=bool(
                int(request.form.get("mandatory_announcement"))  # type: ignore
            ),
            piggies=bool(int(request.form.get("piggies"))),  # type: ignore
            piggies_auto_announce=bool(int(request.form.get("piggies_auto_announce"))),  # type: ignore
            piggies_in_poverty=bool(int(request.form.get("piggies_in_poverty"))),  # type: ignore
            piggies_in_trump_and_color_solo=bool(
                int(request.form.get("piggies_in_trump_and_color_solo"))  # type: ignore
            ),
            trump_solo=bool(int(request.form.get("trump_solo"))),  # type: ignore
            queens_solo=bool(int(request.form.get("queens_solo"))),  # type: ignore
            jacks_solo=bool(int(request.form.get("jacks_solo"))),  # type: ignore
            fleshless_solo=bool(int(request.form.get("fleshless_solo"))),  # type: ignore
            queens_jacks_solo=bool(int(request.form.get("queens_jacks_solo"))),  # type: ignore
            kings_solo=bool(int(request.form.get("kings_solo"))),  # type: ignore
            color_solo=str(request.form.get("color_solo")),
            fox_caught=bool(int(request.form.get("fox_caught"))),  # type: ignore
            fox_caught_in_solos=bool(int(request.form.get("fox_caught_in_solos"))),  # type: ignore
            fox_last_trick=bool(int(request.form.get("fox_last_trick"))),  # type: ignore
            doppelkopf=bool(int(request.form.get("doppelkopf"))),  # type: ignore
            karlchen=bool(int(request.form.get("karlchen"))),  # type: ignore
            karlchen_caught=str(request.form.get("karlchen_caught")),
            dulle_caught=str(request.form.get("dulle_caught")),
            jacks_pile=bool(int(request.form.get("jacks_pile"))),  # type: ignore
            hearts_trick=bool(int(request.form.get("hearts_trick"))),  # type: ignore
            poverty=bool(int(request.form.get("poverty"))),  # type: ignore
            wedding_decision_trick=str(request.form.get("wedding_decision_trick")),
            five_louses=bool(int(request.form.get("five_louses"))),  # type: ignore
            fox_highest_trump=bool(int(request.form.get("fox_highest_trump"))),  # type: ignore
            seven_fulls=bool(int(request.form.get("seven_fulls"))),  # type: ignore
            less_than_3_trumps=bool(int(request.form.get("less_than_3_trumps"))),  # type: ignore
            bock_round_scheme=str(request.form.get("bock_scheme")),
            hearts_trick_bock=bool(int(request.form.get("hearts_trick_bock"))),  # type: ignore
            split_arse_bock=bool(int(request.form.get("split_arse_bock"))),  # type: ignore
            lost_black_bock=bool(int(request.form.get("lost_black_bock"))),  # type: ignore
            both_announce_bock=bool(int(request.form.get("both_announce_bock"))),  # type: ignore
            jacks_pile_bock=bool(int(request.form.get("jacks_pile_bock"))),  # type: ignore
        )
        db.session.add(new_ruleset)
        db.session.commit()

        table_name = str(request.form.get("table_name"))
        if table_name == "":
            table_name = current_user.username + "'s table"  # type: ignore
        password = str(request.form.get("password"))
        if password == "":
            password = None
        else:
            password = generate_password_hash(password, method="sha256")

        new_table = Table(
            name=table_name,
            password=password,
            ruleset_id=new_ruleset.id,
            user_id=current_user.id,  # type: ignore
        )
        db.session.add(new_table)
        db.session.commit()

        return redirect(url_for("lobby_view.lobby"))

    return render_template("create_table.html", user=current_user)
