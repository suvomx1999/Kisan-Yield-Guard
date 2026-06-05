"""
Model Evaluation & Registration for Kisan Yield Guard
======================================================
Evaluates the latest MLflow run on the held-out test set and registers
the model to MLflow Model Registry if it passes quality gates.

Inputs:
    - data/processed/test.csv
    - MLflow experiment: kisan-yield-guard (latest run)

Quality Gate:
    - test_r2 >= 0.75 → register as KisanYieldModel → Production

Outputs:
    - Test metrics logged to the same MLflow run
    - Model registered in MLflow Model Registry (if quality gate passes)
"""

import warnings

import yaml
import numpy as np
import pandas as pd
import mlflow
import mlflow.xgboost
from mlflow.tracking import MlflowClient
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def load_params(path: str = "params.yaml") -> dict:
    """Load project parameters from YAML config."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_latest_run(experiment_name: str) -> mlflow.entities.Run:
    """
    Retrieve the latest completed run from an MLflow experiment.

    Parameters
    ----------
    experiment_name : str
        Name of the MLflow experiment.

    Returns
    -------
    mlflow.entities.Run
        The most recent run object.

    Raises
    ------
    ValueError
        If no runs are found in the experiment.
    """
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment '{experiment_name}' not found. Run train.py first.")

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=1,
    )
    if not runs:
        raise ValueError(f"No runs found in experiment '{experiment_name}'. Run train.py first.")

    return runs[0]


def main() -> None:
    """Evaluate the latest model and register if it passes quality gates."""
    # --- Load params ---
    params = load_params()
    model_name = params["serving"]["model_name"]
    quality_threshold = 0.75

    print("=" * 60)
    print("  Kisan Yield Guard — Model Evaluation & Registration")
    print("=" * 60)

    # --- Configure MLflow ---
    mlflow.set_tracking_uri("mlruns")

    # --- Get latest run ---
    experiment_name = "kisan-yield-guard"
    print(f"\n  Fetching latest run from '{experiment_name}'...")
    latest_run = get_latest_run(experiment_name)
    run_id = latest_run.info.run_id
    print(f"  Latest Run ID: {run_id}")

    # --- Print train metrics from the run ---
    train_metrics = latest_run.data.metrics
    print(f"\n  Train Metrics (from run):")
    print(f"    RMSE:     {train_metrics.get('rmse', 'N/A')}")
    print(f"    MAE:      {train_metrics.get('mae', 'N/A')}")
    print(f"    R² Score: {train_metrics.get('r2_score', 'N/A')}")

    # --- Load test data ---
    test_path = "data/processed/test.csv"
    print(f"\n  Loading test data from {test_path}...")
    test_df = pd.read_csv(test_path)

    target_col = "yield_kg_per_ha"
    feature_cols = [col for col in test_df.columns if col not in [target_col, "year"]]

    X_test = test_df[feature_cols]
    y_test = test_df[target_col]
    print(f"  Test samples: {len(X_test)}")

    # --- Load model from MLflow ---
    model_uri = f"runs:/{run_id}/model"
    print(f"\n  Loading model from: {model_uri}")
    model = mlflow.xgboost.load_model(model_uri)

    # --- Run inference on test set ---
    print("  Running inference on test set...")
    y_pred = model.predict(X_test)

    # --- Compute test metrics ---
    test_rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    test_mae = float(mean_absolute_error(y_test, y_pred))
    test_r2 = float(r2_score(y_test, y_pred))

    print(f"\n  Test Metrics:")
    print(f"    RMSE:     {test_rmse:.4f}")
    print(f"    MAE:      {test_mae:.4f}")
    print(f"    R² Score: {test_r2:.4f}")

    # --- Log test metrics back to the same run ---
    client = MlflowClient()
    client.log_metric(run_id, "test_rmse", round(test_rmse, 4))
    client.log_metric(run_id, "test_mae", round(test_mae, 4))
    client.log_metric(run_id, "test_r2", round(test_r2, 4))
    print(f"\n  Test metrics logged to MLflow run {run_id}")

    # --- Quality gate check ---
    print(f"\n{'='*60}")
    print(f"  Quality Gate: test_r2 >= {quality_threshold}")
    print(f"  Actual:       test_r2  = {test_r2:.4f}")
    print(f"{'='*60}")

    if test_r2 >= quality_threshold:
        print(f"\n  ✅ Quality gate PASSED (R² = {test_r2:.4f} >= {quality_threshold})")
        print(f"  Registering model as '{model_name}'...")

        # Register model
        model_uri = f"runs:/{run_id}/model"
        registered_model = mlflow.register_model(model_uri, model_name)

        # Transition to Production stage
        client.transition_model_version_stage(
            name=model_name,
            version=registered_model.version,
            stage="Production",
            archive_existing_versions=True,
        )

        print(f"\n  ✅ Model registered as {model_name} → Production (version {registered_model.version})")
        print(f"\n  Summary:")
        print(f"    Model Name:    {model_name}")
        print(f"    Version:       {registered_model.version}")
        print(f"    Stage:         Production")
        print(f"    Run ID:        {run_id}")
        print(f"    Test RMSE:     {test_rmse:.4f}")
        print(f"    Test MAE:      {test_mae:.4f}")
        print(f"    Test R²:       {test_r2:.4f}")
    else:
        print(f"\n  ⚠️ Quality gate FAILED (R² = {test_r2:.4f} < {quality_threshold})")
        print(f"  Model NOT registered. Consider:")
        print(f"    - Adjusting hyperparameters in params.yaml")
        print(f"    - Adding more training data")
        print(f"    - Reviewing feature engineering pipeline")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
