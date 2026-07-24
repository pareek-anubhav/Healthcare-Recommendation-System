from flask_login import current_user
from database.db import db
from database.model import PredictionHistory
from flask import Blueprint, render_template, request
from services.predictor import (
    predict_and_recommend,
    feature_names
)

prediction = Blueprint("prediction", __name__)


from flask_login import login_required

@prediction.route("/predict")
@login_required
def home():

    symptoms = sorted(feature_names)

    return render_template(
        "user/predict.html",
        symptoms=symptoms
    )


@prediction.route("/predict", methods=["POST"])
def predict():

    selected_symptoms = request.form.getlist("symptoms")

    if len(selected_symptoms) == 0:

        return render_template(
            "user/predict.html",
            symptoms=sorted(feature_names),
            error="Please select at least one symptom."
        )

    result = predict_and_recommend(selected_symptoms)
    if current_user.is_authenticated:

        if current_user.is_authenticated and result["best_prediction"]:

         best = result["best_prediction"]

        history = PredictionHistory(
        user_id=current_user.id,
        symptoms=", ".join(selected_symptoms),
        predicted_disease=best["disease"],
        confidence=best["confidence"]
    )

    db.session.add(history)
    db.session.commit()

    db.session.add(history)
    db.session.commit()
    return render_template(
        "user/result.html",
        result=result
    )
