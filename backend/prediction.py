import numpy as np
import os
import pandas as pd
from flask import Flask, request, jsonify
import joblib
from pydantic import BaseModel

# For prediction endpoint
class PredictionInput(BaseModel):
    Price: float
    Discount: float
    Category_Amino_Acid: int
    Category_Fat_Burner: int
    Category_Herbal: int
    Category_Hydration: int
    Category_Mineral: int
    Category_Omega: int
    Category_Performance: int
    Category_Protein: int
    Category_Sleep_Aid: int
    Category_Vitamin: int


# Load your trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "DataModel", "supplemet_revenue_predictor.pkl")

model = joblib.load(MODEL_PATH)

# Define the expected features (same order used in training!)
FEATURES = [
    'Price', 'Units Sold', 'Discount', 'Units Returned',
    'Category_Amino Acid', 'Category_Fat Burner', 'Category_Herbal',
    'Category_Hydration', 'Category_Mineral', 'Category_Omega',
    'Category_Performance', 'Category_Protein', 'Category_Sleep Aid',
    'Category_Vitamin'
]

def predict_rev(data: PredictionInput):
    # Convert to DataFrame
    input_dict = {
        'Price': data.Price,
        'Discount': data.Discount,
        'Category_Amino Acid': data.Category_Amino_Acid,
        'Category_Fat Burner': data.Category_Fat_Burner,
        'Category_Herbal': data.Category_Herbal,
        'Category_Hydration': data.Category_Hydration,
        'Category_Mineral': data.Category_Mineral,
        'Category_Omega': data.Category_Omega,
        'Category_Performance': data.Category_Performance,
        'Category_Protein': data.Category_Protein,
        'Category_Sleep Aid': data.Category_Sleep_Aid,
        'Category_Vitamin': data.Category_Vitamin
    }
    columns=[
        'Price', 'Discount', 'Category_Amino Acid',
        'Category_Fat Burner', 'Category_Herbal', 'Category_Hydration', 'Category_Mineral',
        'Category_Omega', 'Category_Performance', 'Category_Protein', 'Category_Sleep Aid',
        'Category_Vitamin'
    ]

    input_df = pd.DataFrame([input_dict], columns=columns)

    prediction = model.predict(input_df)

    print(f"Predicted Revenue: ${prediction[0]:.2f}")

    return {f"Predicted Revenue: ${prediction[0]:.2f}"}