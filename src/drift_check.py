"""
Evidently AI Drift Detection for Kisan Yield Guard
====================================================
Compares a reference baseline dataset against incoming (potentially drifted)
data to detect distributional shifts in features. Generates an HTML report
and a per-feature drift summary.

Inputs:
    - data/reference/reference_data.csv  (baseline)
    - data/reference/drift_batch.csv     (current / incoming data)
    - data/processed/scaler.joblib       (fitted StandardScaler)
    - data/processed/encoders.joblib     (fitted LabelEncoders)
    - params.yaml

Outputs:
    - reports/drift_report.html (Evidently visual drift report)
    - Console: per-feature drift table + overall verdict
    - Exit code: 1 if drift detected, 0 otherwise
"""

import os
import sys
from typing import Dict, Tuple

import yaml
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def load_params(path: str = "params.yaml") -> dict:
    """Load project parameters from YAML config."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def preprocess_for_drift(
    df: pd.DataFrame,
    encoders: Dict[str, LabelEncoder],
    scaler: StandardScaler,
) -> pd.DataFrame:
    """
    Apply the same preprocessing used during training so drift detection
    compares like-for-like distributions.

    Steps:
        1. Encode categoricals using saved LabelEncoders
        2. Engineer features (rainfall_yield_ratio, fertilizer_efficiency, msp_normalized)
        3. Scale numerical features using saved StandardScaler
    """
    df = df.copy()

    # --- Encode categoricals ---
    categorical_cols = ["crop", "season", "soil_type", "state", "district"]
    for col in categorical_cols:
        if col in encoders:
            le = encoders[col]
            known = set(le.classes_)
            df[col] = df[col].astype(str).apply(
                lambda x, _known=known, _le=le: (
                    _le.transform([x])[0] if x in _known else -1
                )
            )

    # --- Feature engineering ---
    df["rainfall_yield_ratio"] = (
        df["rainfall_mm"] / (df["yield_kg_per_ha"] + 1)
    ).round(6)

    df["fertilizer_efficiency"] = (
        df["yield_kg_per_ha"] / (df["fertilizer_kg_per_ha"] + 1)
    ).round(4)

    year_avg_msp = df.groupby("year")["msp_inr_per_quintal"].transform("mean")
    df["msp_normalized"] = (df["msp_inr_per_quintal"] / year_avg_msp).round(6)

    # --- Scale numerical features ---
    numerical_cols = [
        "rainfall_mm",
        "temperature_avg_c",
        "irrigation_pct",
        "fertilizer_kg_per_ha",
        "msp_inr_per_quintal",
    ]
    df[numerical_cols] = scaler.transform(df[numerical_cols])

    return df


def run_drift_detection(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    report_path: str,
) -> Tuple[dict, bool]:
    """
    Run Evidently DataDriftPreset and return per-feature results.

    Parameters
    ----------
    reference_df : pd.DataFrame
        Preprocessed reference/baseline data.
    current_df : pd.DataFrame
        Preprocessed current/incoming data.
    report_path : str
        Path to save the HTML drift report.

    Returns
    -------
    feature_results : dict
        {feature_name: {"drifted": bool, "p_value": float, "statistic": float}}
    dataset_drift : bool
        True if overall dataset drift is detected.
    """
    # Drop non-feature columns for drift analysis
    exclude_cols = ["year", "yield_kg_per_ha"]
    analysis_cols = [c for c in reference_df.columns if c not in exclude_cols]

    ref = reference_df[analysis_cols].copy()
    cur = current_df[analysis_cols].copy()

    # Build and run the Evidently report
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref, current_data=cur)

    # Save HTML report
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    report.save_html(report_path)

    # Extract results from the report
    report_dict = report.as_dict()

    # Navigate Evidently's result structure
    metrics = report_dict["metrics"]

    # Find the DataDriftTable metric for per-feature results
    feature_results = {}
    dataset_drift = False

    for metric in metrics:
        metric_id = metric.get("metric", "")

        # Dataset-level drift
        if metric_id == "DatasetDriftMetric":
            result = metric.get("result", {})
            dataset_drift = result.get("dataset_drift", False)
            drift_share = result.get("share_of_drifted_columns", 0.0)

        # Per-column drift
        elif metric_id == "DataDriftTable":
            result = metric.get("result", {})
            drift_by_columns = result.get("drift_by_columns", {})
            for col_name, col_data in drift_by_columns.items():
                feature_results[col_name] = {
                    "drifted": col_data.get("drift_detected", False),
                    "drift_score": col_data.get("drift_score", None),
                    "stattest": col_data.get("stattest_name", "unknown"),
                }

    return feature_results, dataset_drift


def print_drift_summary(
    feature_results: dict,
    dataset_drift: bool,
    drift_threshold: float,
) -> None:
    """Print a formatted per-feature drift summary table."""
    print(f"\n{'='*70}")
    print(f"  Per-Feature Drift Summary")
    print(f"{'='*70}")
    print(f"  {'Feature':<28s} {'Drifted':<10s} {'Score':<12s} {'Test':<15s}")
    print(f"  {'-'*65}")

    drifted_count = 0
    total_count = len(feature_results)

    for feat, info in sorted(feature_results.items()):
        drifted = info["drifted"]
        score = info["drift_score"]
        stattest = info["stattest"]

        if drifted:
            drifted_count += 1

        marker = "⚠️ YES" if drifted else "✅ No"
        score_str = f"{score:.6f}" if score is not None else "N/A"

        print(f"  {feat:<28s} {marker:<10s} {score_str:<12s} {stattest:<15s}")

    drift_pct = (drifted_count / total_count * 100) if total_count > 0 else 0
    print(f"  {'-'*65}")
    print(f"  Drifted features: {drifted_count}/{total_count} ({drift_pct:.1f}%)")
    print(f"  Drift threshold:  {drift_threshold * 100:.0f}% of features")
    print(f"  Dataset drift:    {'YES' if dataset_drift else 'No'}")
    print(f"{'='*70}")


def main() -> None:
    """Run the full drift detection pipeline."""
    # --- Load params ---
    params = load_params()
    drift_threshold = params["data"]["drift_threshold"]

    print("=" * 70)
    print("  Kisan Yield Guard — Evidently AI Drift Detection")
    print("=" * 70)

    # --- Load saved preprocessing artifacts ---
    print("\n  Loading preprocessing artifacts...")
    encoders = joblib.load("data/processed/encoders.joblib")
    scaler = joblib.load("data/processed/scaler.joblib")
    print("  ✅ Loaded encoders.joblib and scaler.joblib")

    # --- Load reference and current datasets ---
    ref_path = "data/reference/reference_data.csv"
    cur_path = "data/reference/drift_batch.csv"

    print(f"\n  Reference data: {ref_path}")
    ref_raw = pd.read_csv(ref_path)
    print(f"    Shape: {ref_raw.shape}")

    print(f"  Current data:   {cur_path}")
    cur_raw = pd.read_csv(cur_path)
    print(f"    Shape: {cur_raw.shape}")

    # --- Preprocess both datasets identically ---
    print("\n  Preprocessing datasets for drift analysis...")
    ref_processed = preprocess_for_drift(ref_raw, encoders, scaler)
    cur_processed = preprocess_for_drift(cur_raw, encoders, scaler)

    # --- Run drift detection ---
    report_path = "reports/drift_report.html"
    print(f"\n  Running Evidently DataDriftPreset...")
    feature_results, dataset_drift = run_drift_detection(
        ref_processed, cur_processed, report_path
    )
    print(f"  ✅ Drift report saved: {report_path}")

    # --- Print summary ---
    print_drift_summary(feature_results, dataset_drift, drift_threshold)

    # --- Determine exit based on drift share ---
    drifted_count = sum(1 for v in feature_results.values() if v["drifted"])
    total_count = len(feature_results)
    drift_share = drifted_count / total_count if total_count > 0 else 0

    if dataset_drift or drift_share > drift_threshold:
        print(f"\n  ⚠️ DRIFT DETECTED — retraining recommended")
        print(f"  Drifted share: {drift_share:.2%} (threshold: {drift_threshold:.0%})")
        print(f"  Possible causes: monsoon anomaly, El Niño event, policy change\n")
        sys.exit(1)
    else:
        print(f"\n  ✅ No significant drift detected")
        print(f"  Drifted share: {drift_share:.2%} (threshold: {drift_threshold:.0%})\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
