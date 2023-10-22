from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = str(request.form.get("email")).lower()
        password = str(request.form.get("password"))

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.lobby"))
            else:
                flash("Incorrect password, try again", category="error")
        else:
            flash(f"There is no user with the email {email}.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = str(request.form.get("email")).lower()
        username = str(request.form.get("username"))
        password1 = str(request.form.get("password1"))
        password2 = str(request.form.get("password2"))

        user1 = User.query.filter_by(email=email).first()
        user2 = User.query.filter_by(username=username).first()

        if user1:
            flash(f"User with the email {email} already exists.", category="error")
        elif user2:
            flash(f"User with the name {username} already exists.", category="error")
        elif password1 != password2:
            flash("Passwords do not match.", category="error")
        elif len(password1) < 5:
            flash("Password must be at least contain 5 characters.", category="error")
        else:
            try:
                new_user = User(email, username, generate_password_hash(password1, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                flash("Signed up successfully!", category="success")
                login_user(new_user, remember=True)
                return redirect(url_for("views.lobby"))

            except IntegrityError as e:
                flash(f"Could not sign you up. There is an integrity error {e}.", category="error")
            except Exception as e:
                flash(f"There was an error: {e}", category="error")

    return render_template("sign_up.html", user=current_user)
