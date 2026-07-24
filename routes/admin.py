from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from database.db import db, bcrypt
from database.model import User, PredictionHistory

admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    """Only lets logged-in users with role='admin' access the route."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):

        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Please login as an admin to continue.", "danger")
            return redirect(url_for("admin.login"))

        return view_func(*args, **kwargs)

    return wrapped


@admin.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, role="admin").first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("admin.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("admin/login.html")


@admin.route("/logout")
@admin_required
def logout():

    logout_user()

    return redirect(url_for("admin.login"))


@admin.route("/dashboard")
@admin_required
def dashboard():

    total_users = User.query.filter_by(role="user").count()

    total_doctors = User.query.filter_by(role="doctor").count()

    total_predictions = PredictionHistory.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_doctors=total_doctors,
        total_predictions=total_predictions
    )


@admin.route("/doctors/add", methods=["GET", "POST"])
@admin_required
def add_doctor():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already registered.", "danger")
            return redirect(url_for("admin.add_doctor"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_doctor = User(
            full_name=name,
            email=email,
            password=hashed_password,
            role="doctor"
        )

        db.session.add(new_doctor)
        db.session.commit()

        flash("Doctor added successfully.", "success")

        return redirect(url_for("admin.manage_users"))

    return render_template("admin/add_doctor.html")


@admin.route("/users")
@admin_required
def manage_users():

    users = User.query.filter_by(role="user").all()

    doctors = User.query.filter_by(role="doctor").all()

    return render_template(
        "admin/manage_users.html",
        users=users,
        doctors=doctors
    )


@admin.route("/doctors/<int:doctor_id>/remove")
@admin_required
def remove_doctor(doctor_id):

    doctor_user = User.query.filter_by(id=doctor_id, role="doctor").first()

    if doctor_user:
        db.session.delete(doctor_user)
        db.session.commit()
        flash("Doctor removed.", "success")

    return redirect(url_for("admin.manage_users"))


@admin.route("/users/<int:user_id>/remove")
@admin_required
def remove_user(user_id):

    target_user = User.query.filter_by(id=user_id, role="user").first()

    if target_user:
        db.session.delete(target_user)
        db.session.commit()
        flash("User removed.", "success")

    return redirect(url_for("admin.manage_users"))


@admin.route("/analytics")
@admin_required
def analytics():

    total_users = User.query.filter_by(role="user").count()

    total_doctors = User.query.filter_by(role="doctor").count()

    total_predictions = PredictionHistory.query.count()

    top_diseases = db.session.query(
        PredictionHistory.predicted_disease,
        db.func.count(PredictionHistory.id).label("count")
    ).group_by(
        PredictionHistory.predicted_disease
    ).order_by(
        db.func.count(PredictionHistory.id).desc()
    ).limit(5).all()

    return render_template(
        "admin/analytics.html",
        total_users=total_users,
        total_doctors=total_doctors,
        total_predictions=total_predictions,
        top_diseases=top_diseases
    )
