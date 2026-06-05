"""
XGBoost Training Script with MLflow Tracking
=============================================
Trains an XGBoost regressor for crop yield prediction and logs all
parameters, metrics, feature importance, and the model to MLflow.

Inputs:
    - data/processed/train.csv
    - params.yaml

Outputs (logged to MLflow):
    - Parameters from params.yaml
    - Metrics: rmse, mae, r2_score (on train set)
    - Artifact: reports/feature_importance.png
    - Model: XGBoost model with signature and input example
"""

import os
import warnings

import yaml
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for CI/server environments
import matplotlib.pyplot as plt
import mlflow
import mlflow.xgboost
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

warnings.filterwarnings("ignore", category=UserWarning)


def load_params(path: str = "params.yaml") -> dict:
    """Load project parameters from YAML config."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def plot_feature_importance(model: XGBRegressor, feature_names: list, save_path: str) -> None:
    """
    Generate and save a horizontal bar chart of XGBoost feature importances.
    """
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(
        range(len(sorted_idx)),
        importances[sorted_idx],
        color="#2ecc71",
        edgecolor="#27ae60",
        height=0.7,
    )
    ax.set_yticks(range(len(sorted_idx)))
    ax.set_yticklabels([feature_names[i] for i in sorted_idx], fontsize=11)
    ax.set_xlabel("Feature Importance (Gain)", fontsize=12)
    ax.set_title("Kisan Yield Guard — XGBoost Feature Importance", fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Feature importance plot saved: {save_path}")


def main() -> None:
    """Train XGBoost model and log everything to MLflow."""
    # --- Load params ---
    params = load_params()
    model_params = params["model"]

    print("=" * 60)
    print("  Kisan Yield Guard — XGBoost Training")
    print("=" * 60)
    print(f"\n  Hyperparameters:")
    for k, v in model_params.items():
        print(f"    {k}: {v}")

    # --- Load training data ---
    train_path = "data/processed/train.csv"
    print(f"\n  Loading training data from {train_path}...")
    train_df = pd.read_csv(train_path)

    target_col = "yield_kg_per_ha"
    feature_cols = [col for col in train_df.columns if col not in [target_col, "year"]]

    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    print(f"  Training samples: {len(X_train)}")
    print(f"  Features: {len(feature_cols)}")

    # --- Configure MLflow ---
    mlflow.set_tracking_uri("mlruns")
    mlflow.set_experiment("kisan-yield-guard")

    print("\n  Starting MLflow run...")
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        print(f"  MLflow Run ID: {run_id}")

        # --- Log all hyperparameters ---
        mlflow.log_params({
            "n_estimators": model_params["n_estimators"],
            "max_depth": model_params["max_depth"],
            "learning_rate": model_params["learning_rate"],
            "subsample": model_params["subsample"],
            "colsample_bytree": model_params["colsample_bytree"],
            "random_state": model_params["random_state"],
            "num_features": len(feature_cols),
            "train_samples": len(X_train),
        })

        # --- Train XGBoost ---
        print("\n  Training XGBoost regressor...")
        model = XGBRegressor(
            n_estimators=model_params["n_estimators"],
            max_depth=model_params["max_depth"],
            learning_rate=model_params["learning_rate"],
            subsample=model_params["subsample"],
            colsample_bytree=model_params["colsample_bytree"],
            random_state=model_params["random_state"],
            objective="reg:squarederror",
            n_jobs=-1,
            verbosity=0,
        )
        model.fit(X_train, y_train)
        print("  Training complete.")

        # --- Compute train metrics ---
        y_pred_train = model.predict(X_train)
        train_rmse = float(np.sqrt(mean_squared_error(y_train, y_pred_train)))
        train_mae = float(mean_absolute_error(y_train, y_pred_train))
        train_r2 = float(r2_score(y_train, y_pred_train))

        # --- Log metrics ---
        mlflow.log_metrics({
            "rmse": round(train_rmse, 4),
            "mae": round(train_mae, 4),
            "r2_score": round(train_r2, 4),
        })

        print(f"\n  Train Metrics:")
        print(f"    RMSE:     {train_rmse:.4f}")
        print(f"    MAE:      {train_mae:.4f}")
        print(f"    R² Score: {train_r2:.4f}")

        # --- Feature importance plot ---
        fi_path = "reports/feature_importance.png"
        plot_feature_importance(model, feature_cols, fi_path)
        mlflow.log_artifact(fi_path, artifact_path="plots")

        # --- Log model with signature and input example ---
        input_example = X_train.head(3)
        from mlflow.models.signature import infer_signature
        signature = infer_signature(X_train, y_pred_train)

        mlflow.xgboost.log_model(
            model,
            artifact_path="model",
            signature=signature,
            input_example=input_example,
        )
        print(f"\n  Model logged to MLflow (artifact_path='model')")

    # --- Final summary ---
    print(f"\n{'='*60}")
    print(f"  ✅ Training complete!")
    print(f"  MLflow Run ID: {run_id}")
    print(f"  Experiment:    kisan-yield-guard")
    print(f"  RMSE: {train_rmse:.4f} | MAE: {train_mae:.4f} | R²: {train_r2:.4f}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
