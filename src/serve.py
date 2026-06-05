"""
FastAPI Prediction Server for Kisan Yield Guard
=================================================
Production inference server that loads the registered KisanYieldModel
from MLflow and exposes prediction, health check, and drift status endpoints.

Endpoints:
    GET  /              — Health check
    POST /predict       — Yield prediction for a single district-crop record
    GET  /drift-status  — Latest drift detection summary

Startup:
    Loads KisanYieldModel (Production stage) from MLflow Model Registry,
    along with saved encoders and scaler for request preprocessing.
"""

import os
import subprocess
import sys
from typing import Optional

import yaml
import numpy as np
import pandas as pd
import joblib
import mlflow
import mlflow.xgboost
from mlflow.tracking import MlflowClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic request/response models
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    """Input schema for crop yield prediction."""
    district: str = Field(..., description="Indian district name (e.g. Ludhiana)")
    state: str = Field(..., description="Indian state name (e.g. Punjab)")
    crop: str = Field(..., description="Crop type: Rice, Wheat, or Sugarcane")
    year: int = Field(..., ge=2010, le=2030, description="Year (2010–2030)")
    season: str = Field(..., description="Season: Kharif, Rabi, or Zaid")
    rainfall_mm: float = Field(..., ge=0, description="Seasonal rainfall in mm")
    temperature_avg_c: float = Field(..., ge=0, le=50, description="Average temperature in °C")
    soil_type: str = Field(..., description="Soil type: Alluvial, Black, Red, Laterite, or Desert")
    irrigation_pct: float = Field(..., ge=0, le=100, description="Irrigation coverage (%)")
    fertilizer_kg_per_ha: float = Field(..., ge=0, description="Fertilizer use (kg/ha)")
    msp_inr_per_quintal: float = Field(..., ge=0, description="MSP (INR per quintal)")

    class Config:
        json_schema_extra = {
            "example": {
                "district": "Ludhiana",
                "state": "Punjab",
                "crop": "Wheat",
                "year": 2024,
                "season": "Rabi",
                "rainfall_mm": 420.0,
                "temperature_avg_c": 18.5,
                "soil_type": "Alluvial",
                "irrigation_pct": 85.0,
                "fertilizer_kg_per_ha": 180.0,
                "msp_inr_per_quintal": 2275.0,
            }
        }


class PredictResponse(BaseModel):
    """Output schema for crop yield prediction."""
    district: str
    crop: str
    predicted_yield_kg_per_ha: float
    yield_category: str
    confidence_note: str


class HealthResponse(BaseModel):
    """Output schema for health check."""
    status: str
    model: str
    stage: str
    version: str


class DriftStatusResponse(BaseModel):
    """Output schema for drift status."""
    drift_detected: bool
    drifted_features: int
    total_features: int
    drift_share_pct: float
    details: str


# ---------------------------------------------------------------------------
# Application setup
# ---------------------------------------------------------------------------

def load_params(path: str = "params.yaml") -> dict:
    """Load project parameters from YAML config."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


params = load_params()
MODEL_NAME = params["serving"]["model_name"]
MODEL_STAGE = params["serving"]["model_stage"]

# Configure MLflow
mlflow.set_tracking_uri("mlruns")


def load_production_model():
    """
    Load the Production-stage model from MLflow Model Registry.
    Returns the model, its version string, and the run ID.
    """
    client = MlflowClient()

    # Search for the latest Production version
    try:
        versions = client.get_latest_versions(MODEL_NAME, stages=[MODEL_STAGE])
    except Exception:
        versions = []

    if not versions:
        raise RuntimeError(
            f"No '{MODEL_STAGE}' model found for '{MODEL_NAME}'. "
            f"Run train.py and evaluate.py first to register a model."
        )

    latest = versions[0]
    model_version = latest.version
    run_id = latest.run_id
    model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"

    print(f"  Loading model: {MODEL_NAME} v{model_version} ({MODEL_STAGE})")
    print(f"  Run ID: {run_id}")

    model = mlflow.xgboost.load_model(model_uri)
    return model, model_version, run_id


def load_preprocessing_artifacts():
    """Load the saved scaler and encoders from the preprocessing step."""
    encoders_path = "data/processed/encoders.joblib"
    scaler_path = "data/processed/scaler.joblib"

    if not os.path.exists(encoders_path) or not os.path.exists(scaler_path):
        raise RuntimeError(
            "Preprocessing artifacts not found. Run preprocess.py first."
        )

    encoders = joblib.load(encoders_path)
    scaler = joblib.load(scaler_path)
    return encoders, scaler


# --- Load everything at startup ---
print("=" * 60)
print("  Kisan Yield Guard — Starting FastAPI Server")
print("=" * 60)

try:
    model, model_version, model_run_id = load_production_model()
    encoders, scaler = load_preprocessing_artifacts()
    print("  ✅ Model and preprocessing artifacts loaded successfully")
    startup_ok = True
except Exception as e:
    print(f"  ⚠️ Startup warning: {e}")
    print("  Server will start but /predict will return errors.")
    model, model_version, model_run_id = None, "N/A", "N/A"
    encoders, scaler = None, None
    startup_ok = False

print("=" * 60)


# --- Create FastAPI app ---
app = FastAPI(
    title="Kisan Yield Guard API",
    description="Predict district-level crop yield for Indian agriculture using XGBoost + MLflow",
    version="1.0.0",
)

# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helper: preprocess a single prediction request
# ---------------------------------------------------------------------------

def preprocess_request(req: PredictRequest) -> pd.DataFrame:
    """
    Transform a single prediction request into a feature vector matching
    the training pipeline's output format.
    """
    # Build a single-row DataFrame
    data = {
        "district": [req.district],
        "state": [req.state],
        "crop": [req.crop],
        "season": [req.season],
        "soil_type": [req.soil_type],
        "rainfall_mm": [req.rainfall_mm],
        "temperature_avg_c": [req.temperature_avg_c],
        "irrigation_pct": [req.irrigation_pct],
        "fertilizer_kg_per_ha": [req.fertilizer_kg_per_ha],
        "msp_inr_per_quintal": [req.msp_inr_per_quintal],
    }
    df = pd.DataFrame(data)

    # --- Encode categoricals ---
    categorical_cols = ["crop", "season", "soil_type", "state", "district"]
    for col in categorical_cols:
        if col in encoders:
            le = encoders[col]
            known = set(le.classes_)
            val = str(df[col].iloc[0])
            df[col] = le.transform([val])[0] if val in known else -1

    # --- Scale numerical features ---
    numerical_cols = [
        "rainfall_mm",
        "temperature_avg_c",
        "irrigation_pct",
        "fertilizer_kg_per_ha",
        "msp_inr_per_quintal",
    ]
    df[numerical_cols] = scaler.transform(df[numerical_cols])

    # --- Engineer features ---
    # For prediction, we don't have yield yet, so use a proxy estimate
    # rainfall_yield_ratio and fertilizer_efficiency depend on yield,
    # but at prediction time we approximate with median training values
    # to maintain feature count consistency.
    df["rainfall_yield_ratio"] = 0.0  # Will be near-zero centered after scaling
    df["fertilizer_efficiency"] = 0.0
    df["msp_normalized"] = 1.0  # MSP / avg MSP ≈ 1.0 for normalization

    return df


def classify_yield(crop: str, yield_val: float) -> str:
    """Classify predicted yield into Low/Medium/High categories."""
    thresholds = {
        "Rice": (2000, 3500),
        "Wheat": (2500, 4000),
        "Sugarcane": (55000, 75000),
    }
    low, high = thresholds.get(crop, (2000, 4000))

    if yield_val < low:
        return "Low"
    elif yield_val < high:
        return "Medium"
    else:
        return "High"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", response_model=HealthResponse)
def health_check():
    """Health check endpoint returning model status."""
    return HealthResponse(
        status="ok" if startup_ok else "degraded",
        model=MODEL_NAME,
        stage=MODEL_STAGE,
        version=model_run_id,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """Predict crop yield for a given district-crop-weather combination."""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run train.py and evaluate.py first.",
        )

    try:
        # Preprocess the request
        features_df = preprocess_request(req)

        # Ensure column order matches training
        feature_cols = [
            "district", "state", "crop", "season",
            "rainfall_mm", "temperature_avg_c", "soil_type",
            "irrigation_pct", "fertilizer_kg_per_ha", "msp_inr_per_quintal",
            "rainfall_yield_ratio", "fertilizer_efficiency", "msp_normalized",
        ]
        features_df = features_df[feature_cols]

        # Run prediction
        prediction = model.predict(features_df)
        yield_val = round(float(prediction[0]), 1)

        # Ensure yield is within realistic bounds
        yield_ranges = {
            "Rice": (1500, 4500),
            "Wheat": (1800, 5000),
            "Sugarcane": (40000, 90000),
        }
        ymin, ymax = yield_ranges.get(req.crop, (0, 100000))
        yield_val = max(ymin, min(ymax, yield_val))

        return PredictResponse(
            district=req.district,
            crop=req.crop,
            predicted_yield_kg_per_ha=yield_val,
            yield_category=classify_yield(req.crop, yield_val),
            confidence_note=f"Based on MLflow model {MODEL_NAME} v{model_version}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/drift-status", response_model=DriftStatusResponse)
def drift_status():
    """
    Run drift detection and return a JSON summary.
    Executes drift_check.py as a subprocess and parses the output.
    """
    try:
        result = subprocess.run(
            [sys.executable, "src/drift_check.py"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = result.stdout + result.stderr

        # Parse drift results from output
        drift_detected = result.returncode != 0

        # Extract drifted features count from output
        drifted_features = 0
        total_features = 0
        drift_share = 0.0

        for line in output.split("\n"):
            if "Drifted features:" in line:
                parts = line.strip().split(":")[-1].strip()
                nums = parts.split("/")
                if len(nums) == 2:
                    drifted_features = int(nums[0].strip())
                    total_features = int(nums[1].split("(")[0].strip())
                    drift_share = (
                        drifted_features / total_features * 100
                        if total_features > 0
                        else 0
                    )
                break

        details = "DRIFT DETECTED — retraining recommended" if drift_detected else "No significant drift detected"

        return DriftStatusResponse(
            drift_detected=drift_detected,
            drifted_features=drifted_features,
            total_features=total_features,
            drift_share_pct=round(drift_share, 1),
            details=details,
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Drift check timed out (>120s)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drift check error: {str(e)}")
