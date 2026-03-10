from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import mlflow.sklearn
import numpy as np
import os

app = FastAPI(
    title="Diabetes Prediction Service",
    description="ML service for diabetes progression prediction",
    version="1.0.0"
)

class PredictionRequest(BaseModel):
    age: float = Field(..., description="Age")
    sex: float = Field(..., description="Sex")
    bmi: float = Field(..., description="Body mass index")
    bp: float = Field(..., description="Average blood pressure")
    s1: float = Field(..., description="TC, total serum cholesterol")
    s2: float = Field(..., description="LDL, low-density lipoproteins")
    s3: float = Field(..., description="HDL, high-density lipoproteins")
    s4: float = Field(..., description="TCH, total cholesterol / HDL")
    s5: float = Field(..., description="LTG, log of serum triglycerides level")
    s6: float = Field(..., description="GLU, blood sugar level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 59.0,
                "sex": 2.0,
                "bmi": 32.1,
                "bp": 101.0,
                "s1": 157.0,
                "s2": 93.2,
                "s3": 38.0,
                "s4": 4.0,
                "s5": 4.8598,
                "s6": 87.0
            }
        }

class PredictionResponse(BaseModel):
    predict: float

model = None

@app.on_event("startup")
async def load_model():
    global model
    try:
        model_path = os.getenv("MODEL_PATH", "../model/diabetes_model")
        
        if os.path.exists(model_path):
            model = mlflow.sklearn.load_model(model_path)
            print(f"Model loaded from {model_path}")
        else:
            model_uri = "models:/diabetes/1"
            model = mlflow.sklearn.load_model(model_uri)
            print(f"Model loaded from MLflow: {model_uri}")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

@app.get("/")
def root():
    return {
        "service": "Diabetes Prediction API",
        "version": "1.0.0",
        "model_loaded": model is not None
    }

@app.get("/health")
def health():
    return {
        "status": "healthy" if model is not None else "model not loaded",
        "model_loaded": model is not None
    }

@app.post("/api/v1/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        features = np.array([[
            request.age,
            request.sex,
            request.bmi,
            request.bp,
            request.s1,
            request.s2,
            request.s3,
            request.s4,
            request.s5,
            request.s6
        ]])
        
        prediction = model.predict(features)
        
        return PredictionResponse(predict=float(prediction[0]))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
