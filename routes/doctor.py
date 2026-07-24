from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from database.db import db, bcrypt
from database.model import User, PredictionHistory

doctor = Blueprint("doctor", __name__, url_prefix="/doctor")


def doctor_required(view_func):
    """Only lets logged-in users with role='doctor' access the route."""

    @wraps(view_func)
    def wrapped(*args, **kwargs):

        if not current_user.is_authenticated or current_user.role != "doctor":
            flash("Please login as a doctor to continue.", "danger")
            return redirect(url_for("doctor.login"))

        return view_func(*args, **kwargs)

    return wrapped


@doctor.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, role="doctor").first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("doctor.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("doctor/login.html")


@doctor.route("/logout")
@doctor_required
def logout():

    logout_user()

    return redirect(url_for("doctor.login"))


@doctor.route("/dashboard")
@doctor_required
def dashboard():

    total_patients = User.query.filter_by(role="user").count()

    total_predictions = PredictionHistory.query.count()

    return render_template(
        "doctor/dashboard.html",
        total_patients=total_patients,
        total_predictions=total_predictions
    )


@doctor.route("/patients")
@doctor_required
def search_patients():

    query = request.args.get("q", "").strip()

    patients = []

    if query:

        patients = User.query.filter(
            User.role == "user",
            (User.full_name.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
        ).all()

    return render_template(
        "doctor/search_patients.html",
        patients=patients,
        query=query
    )


@doctor.route("/patients/<int:patient_id>/history")
@doctor_required
def patient_history(patient_id):

    patient = User.query.filter_by(id=patient_id, role="user").first_or_404()

    history = PredictionHistory.query.filter_by(
        user_id=patient.id
    ).order_by(
        PredictionHistory.prediction_date.desc()
    ).all()

    return render_template(
        "doctor/patient_history.html",
        patient=patient,
        history=history
    )


@doctor.route("/reports")
@doctor_required
def reports():

    history = PredictionHistory.query.order_by(
        PredictionHistory.prediction_date.desc()
    ).limit(100).all()

    return render_template(
        "doctor/reports.html",
        history=history
    )
