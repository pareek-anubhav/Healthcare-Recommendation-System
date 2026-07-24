from flask import Blueprint, Response
from flask_login import login_required, current_user

from database.model import PredictionHistory

reports = Blueprint("reports", __name__)


@reports.route("/report/<int:history_id>/download")
@login_required
def download_report(history_id):

    record = PredictionHistory.query.filter_by(
        id=history_id,
        user_id=current_user.id
    ).first_or_404()

    content = (
        "MediScan AI - Prediction Report\n"
        "================================\n\n"
        f"Patient Name : {current_user.full_name}\n"
        f"Email        : {current_user.email}\n"
        f"Report Date  : {record.prediction_date}\n\n"
        f"Symptoms Reported : {record.symptoms}\n\n"
        f"Predicted Disease : {record.predicted_disease}\n"
        f"Confidence Score  : {record.confidence}%\n\n"
        "--------------------------------\n"
        "Disclaimer: This report is an AI-generated estimate, not a\n"
        "medical diagnosis. Please consult a doctor before acting on it.\n"
    )

    return Response(
        content,
        mimetype="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename=report_{history_id}.txt"
        }
    )
