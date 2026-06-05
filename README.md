# Kisan Yield Guard 🌾🚜

**An end-to-end MLOps pipeline for Indian district-level crop yield prediction with automated data drift detection and CI/CD retraining.**

---

## 🏛️ Architecture

```text
       [1] Data Generator ──────────────────────┐
       (IMD Weather, CACP MSP, Soil Data)       │
                                                ▼
       [2] Preprocessing Pipeline ──────▶ [3] XGBoost Training
       (Encoders, Scaler, Features)       (MLflow Tracking URI)
                                                │
                                                ▼
       [4] MLflow Model Registry ◀────── [5] Evaluation & Quality Gates
       (Production / Staging)             (R² > 0.75 threshold)
                                                │
                                                ▼
       [6] FastAPI Serving Endpoint ◀─── [7] Evidently AI Drift Detection
       (uvicorn, Docker, Render)          (Drought / El Niño simulator)
                                                │
                                                ▼
       [8] GitHub Actions CI/CD ──────────(Trigger Retrain)
```

---

## 🇮🇳 The Indian Context

Kisan Yield Guard is tailored to the realities of Indian agriculture:
- **IMD Weather Patterns**: Simulates realistic seasonal rainfall and temperature profiles across **16 Indian States** and **30 Districts** (e.g., Ludhiana, Nashik, Guntur).
- **CACP Historical MSP Data**: Incorporates real historical Minimum Support Price (MSP) data (2010–2023) for **Rice, Wheat, and Sugarcane**.
- **Agronomic Factors**: Models yield based on optimal crop-specific temperature bands, irrigation percentages, fertilizer efficiency, and state-specific soil types (Alluvial, Black, Red, Laterite).

---

## 🚀 Quickstart

Clone the repository and run the pipeline locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate the synthetic Indian agricultural dataset (raw, reference, and drift batch)
python src/generate_data.py

# 3. Run the preprocessing pipeline (scales numericals, encodes categoricals)
python src/preprocess.py

# 4. Train the XGBoost model and log to MLflow
python src/train.py

# 5. Evaluate the model and register to MLflow Production stage
python src/evaluate.py

# 6. Check for data drift (will detect simulated drought conditions)
python src/drift_check.py

# 7. Start the FastAPI server
uvicorn src.serve:app --reload --port 8000
```

---

## 🔌 API Usage

Once the FastAPI server is running (`uvicorn src.serve:app --port 8000`), you can hit the `/predict` endpoint.

**Curl Example:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "msp_inr_per_quintal": 2275.0
  }'
```

**Expected Response:**
```json
{
  "district": "Ludhiana",
  "crop": "Wheat",
  "predicted_yield_kg_per_ha": 4231.7,
  "yield_category": "High",
  "confidence_note": "Based on MLflow model KisanYieldModel v1"
}
```

---

## 📊 MLflow UI Instructions

To view the training runs, metrics, parameters, and registered models:

1. Ensure you have run `python src/train.py` at least once.
2. Open a new terminal and run:
   ```bash
   mlflow ui
   ```
3. Navigate to `http://localhost:5000` in your browser.
4. Click on the **`kisan-yield-guard`** experiment to view the logged metrics (RMSE, MAE, R²) and feature importance plots.
5. Click on the **Models** tab to see the registered `KisanYieldModel` at the `Production` stage.

---

## ☁️ Render Deployment

Deploying the FastAPI endpoint to Render is completely automated using the provided `Dockerfile` and `render.yaml`.

1. Push this repository to GitHub.
2. Create a free account on [Render.com](https://render.com).
3. Go to **Dashboard** → **New** → **Blueprint**.
4. Connect your GitHub repository. Render will automatically detect the `render.yaml` configuration.
5. Render will build the Docker image, run the full ML training pipeline inside the container, and start the FastAPI uvicorn server.
6. Your API is now live! (Note: Free tier instances spin down after 15 minutes of inactivity).

---

## ⚠️ Drift Detection & Retraining

Kisan Yield Guard includes built-in drift detection using **Evidently AI**.

- **Why it matters**: In India, shifting monsoon patterns or El Niño events can drastically alter crop yields, rendering older ML models obsolete.
- **How it works**: `src/drift_check.py` compares a baseline reference dataset against incoming data. The provided `drift_batch.csv` simulates a severe drought (rainfall reduced by 25%, temperature increased by 2°C).
- **Triggers**: When >15% of features drift significantly (using Kolmogorov-Smirnov and Chi-Square tests), the script throws an alert and exits with code 1.
- **CI/CD Integration**: The GitHub Actions workflow (`.github/workflows/retrain.yml`) runs this drift check quarterly. If drift is detected, it automatically retrains the XGBoost model, registers the new version, and uploads the Evidently HTML report.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Machine Learning** | XGBoost, scikit-learn |
| **Experiment Tracking** | MLflow |
| **Data Drift Detection**| Evidently AI |
| **Model Serving** | FastAPI, Uvicorn, Pydantic |
| **CI/CD & Automation** | GitHub Actions |
| **Containerization** | Docker |
| **Cloud Deployment** | Render |

---

## 💼 Portfolio Talking Points (For Hiring Managers)

This project is designed to demonstrate full-stack MLOps capabilities:

- **End-to-End ML Engineering Lifecycle**: Proves the ability to not just train a model in a Jupyter Notebook, but to structure a modular pipeline (`preprocess.py` → `train.py` → `evaluate.py`) that handles its own data scaling, encoding, and quality gating.
- **Production-Ready Serving**: Showcases the ability to package a model securely using FastAPI and Docker, complete with Pydantic schema validation to prevent garbage-in-garbage-out errors in a live environment.
- **Automated Monitoring & Retraining**: Demonstrates understanding of model decay (concept/data drift) by implementing Evidently AI and linking it to a GitHub Actions CI/CD workflow that automatically retrains the model when environmental variables (like drought) shift significantly.
