from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from database.model import PredictionHistory

from database.db import db, bcrypt
from database.model import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Check existing user
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            full_name=name,
            email=email,
            password=hashed_password,
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("prediction.home"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("auth.login"))


@auth.route("/history")
@login_required
def history():

    history = PredictionHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        PredictionHistory.prediction_date.desc()
    ).all()

    return render_template(
        "user/history.html",
        history=history
    )