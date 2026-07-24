import os
import joblib
import pandas as pd
from services.recommendation import get_recommendation

# ==============================
# Project Paths
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "disease_prediction_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")
RECOMMENDATION_PATH = os.path.join(BASE_DIR, "models", "healthcare_recommendation_database.csv")

# ==============================
# Load Files
# ==============================

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)
recommendation_df = pd.read_csv(RECOMMENDATION_PATH)

print("✅ Model Loaded")
print("✅ Label Encoder Loaded")
print("✅ Recommendation Database Loaded")

# ==============================
# Get Feature Names
# ==============================

feature_names = model.feature_names_in_

print(f"Total Symptoms: {len(feature_names)}")

# ==============================
# Prediction Function
# ==============================

def predict_disease(selected_symptoms):

    # Create input vector
    input_data = pd.DataFrame(
        [[0] * len(feature_names)],
        columns=feature_names
    )

    # Mark selected symptoms
    for symptom in selected_symptoms:
        symptom = symptom.lower().strip()

        if symptom in input_data.columns:
            input_data.loc[0, symptom] = 1

    # Prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Sort probabilities
    top_indices = probabilities.argsort()[-3:][::-1]

    top_predictions = []

    for idx in top_indices:

        disease = label_encoder.inverse_transform([idx])[0]

        confidence = round(probabilities[idx] * 100, 2)

        top_predictions.append({
            "disease": disease,
            "confidence": confidence
        })

    best_prediction = top_predictions[0]["disease"]

    return best_prediction, top_predictions

def predict_and_recommend(selected_symptoms):

    disease, top_predictions = predict_disease(selected_symptoms)

    # Attach full details (description, medication, diet, precautions,
    # workouts) to EACH of the top 3 predictions so the result page
    # can show a card for every prediction, not just the best one.
    detailed_predictions = []

    for prediction in top_predictions:

        details = get_recommendation(prediction["disease"])

        if details is None:
            continue

        details["confidence"] = prediction["confidence"]

        detailed_predictions.append(details)

    return {
        "best_prediction": detailed_predictions[0] if detailed_predictions else None,
        "top_predictions": detailed_predictions
    }
    