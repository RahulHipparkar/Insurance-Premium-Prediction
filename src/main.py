import pickle
import os
from pathlib import Path
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title = "Insurance Premium Prediction API")

# load model
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
model_path = MODELS_DIR / "insurance_lgbm_model.pkl"
with open(model_path, "rb") as f:
    model = pickle.load(f)

class InsuranceInput(BaseModel):
    Age: int = Field(..., ge = 0, le = 100)
    Diabetes: Literal['Yes', 'No']
    BloodPressureProblems: Literal['Yes','No']
    AnyTransplants: Literal['Yes', 'No']
    AnyChronicDiseases: Literal['Yes','No']
    Height: float = Field(..., ge=50, le=250)
    Weight: float = Field(..., ge=10, le=400)
    KnownAllergies: Literal["Yes", "No"]
    HistoryOfCancerInFamily: Literal["Yes", "No"]
    NumberOfMajorSurgeries: int = Field(..., ge=0, le=10)

@app.get("/health")
def health():
    return {'status':'ok', 'model_loaded': True}

@app.post("/predict")
def predict(data: InsuranceInput):
    # convert data to dataframe
    df = pd.DataFrame([data.model_dump()])
    df['BMI'] = df['Weight'] / ((df['Height'] / 100) ** 2)
    binary_map = {'Yes':1, 'No':0}
    df['Diabetes'] = df['Diabetes'].map(binary_map)
    df['BloodPressureProblems'] = df['BloodPressureProblems'].map(binary_map)
    df['AnyTransplants'] = df['AnyTransplants'].map(binary_map)
    df['AnyChronicDiseases'] = df['AnyChronicDiseases'].map(binary_map)
    df['KnownAllergies'] = df['KnownAllergies'].map(binary_map)
    df["HistoryOfCancerInFamily"] = df["HistoryOfCancerInFamily"].map(binary_map)
    prediction = model.predict(df)[0]
    return{
        "PredictedPremiumPrice": float(prediction)
    }






