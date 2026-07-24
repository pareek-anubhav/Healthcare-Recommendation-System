import os
import pandas as pd
import ast

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RECOMMENDATION_PATH = os.path.join(
    BASE_DIR,
    "models",
    "healthcare_recommendation_database.csv"
)

recommendation_df = pd.read_csv(RECOMMENDATION_PATH)


def get_recommendation(disease):

    disease = disease.lower().strip()

    result = recommendation_df[
        recommendation_df["disease"] == disease
    ]

    if result.empty:
        return None

    row = result.iloc[0]

    return {
    "disease": row["disease"],
    "description": row["description"],
    "medication": ast.literal_eval(row["medication"]) if pd.notna(row["medication"]) else [],
    "diet": ast.literal_eval(row["diet"]) if pd.notna(row["diet"]) else [],
    "precaution_1": row["precaution_1"],
    "precaution_2": row["precaution_2"],
    "precaution_3": row["precaution_3"],
    "precaution_4": row["precaution_4"],
    "workouts": ast.literal_eval(row["workouts"]) if pd.notna(row["workouts"]) else []
}