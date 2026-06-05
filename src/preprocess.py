"""
Preprocessing Pipeline for Kisan Yield Guard
=============================================
Reads raw crop data, applies feature engineering, encodes categoricals,
scales numerical features, and produces train/test splits.

Inputs:
    - data/raw/crop_data.csv
    - params.yaml

Outputs:
    - data/processed/train.csv
    - data/processed/test.csv
    - data/processed/encoders.joblib
    - data/processed/scaler.joblib
"""

import os
from typing import Dict, List, Optional, Tuple

import yaml
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


def load_params(path: str = "params.yaml") -> dict:
    """Load project parameters from YAML config."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def encode_categoricals(
    df: pd.DataFrame,
    categorical_cols: List[str],
    encoders: Optional[Dict[str, LabelEncoder]] = None,
    fit: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    """
    Encode categorical columns using LabelEncoder.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    categorical_cols : list[str]
        Columns to encode.
    encoders : dict or None
        Pre-fitted encoders for transform-only mode.
    fit : bool
        If True, fit new encoders. If False, use provided encoders.

    Returns
    -------
    df : pd.DataFrame
        DataFrame with encoded columns (original columns replaced).
    encoders : dict[str, LabelEncoder]
        Fitted encoder per column.
    """
    df = df.copy()
    if encoders is None:
        encoders = {}

    for col in categorical_cols:
        if fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        else:
            le = encoders[col]
            # Handle unseen labels gracefully: map to -1
            known = set(le.classes_)
            df[col] = df[col].astype(str).apply(
                lambda x: le.transform([x])[0] if x in known else -1
            )

    return df, encoders


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features:
        - rainfall_yield_ratio: rainfall / (yield + 1)
        - fertilizer_efficiency: yield / (fertilizer + 1)
        - msp_normalized: MSP scaled by year's average MSP across crops
    """
    df = df.copy()

    # Rainfall-to-yield ratio
    df["rainfall_yield_ratio"] = (
        df["rainfall_mm"] / (df["yield_kg_per_ha"] + 1)
    ).round(6)

    # Fertilizer efficiency
    df["fertilizer_efficiency"] = (
        df["yield_kg_per_ha"] / (df["fertilizer_kg_per_ha"] + 1)
    ).round(4)

    # MSP normalized by year average
    year_avg_msp = df.groupby("year")["msp_inr_per_quintal"].transform("mean")
    df["msp_normalized"] = (df["msp_inr_per_quintal"] / year_avg_msp).round(6)

    return df


def scale_numerical(
    df: pd.DataFrame,
    numerical_cols: List[str],
    scaler: Optional[StandardScaler] = None,
    fit: bool = True,
) -> Tuple[pd.DataFrame, StandardScaler]:
    """
    Apply StandardScaler to numerical columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    numerical_cols : list[str]
        Columns to scale.
    scaler : StandardScaler or None
        Pre-fitted scaler for transform-only mode.
    fit : bool
        If True, fit a new scaler. If False, use the provided scaler.

    Returns
    -------
    df : pd.DataFrame
        DataFrame with scaled numerical columns.
    scaler : StandardScaler
        Fitted scaler.
    """
    df = df.copy()
    if fit:
        scaler = StandardScaler()
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    else:
        df[numerical_cols] = scaler.transform(df[numerical_cols])

    return df, scaler


def main() -> None:
    """Run the full preprocessing pipeline."""
    # --- Load params ---
    params = load_params()
    test_size = params["data"]["test_size"]
    random_state = params["model"]["random_state"]

    # --- Load raw data ---
    raw_path = "data/raw/crop_data.csv"
    print(f"Loading raw data from {raw_path}...")
    df = pd.read_csv(raw_path)
    print(f"  Raw data shape: {df.shape}")

    # --- Define column groups ---
    categorical_cols = ["crop", "season", "soil_type", "state", "district"]
    numerical_cols = [
        "rainfall_mm",
        "temperature_avg_c",
        "irrigation_pct",
        "fertilizer_kg_per_ha",
        "msp_inr_per_quintal",
    ]
    target_col = "yield_kg_per_ha"

    # --- Feature engineering (before encoding/scaling) ---
    print("Engineering features...")
    df = engineer_features(df)

    # --- Encode categoricals ---
    print("Encoding categorical variables...")
    df, encoders = encode_categoricals(df, categorical_cols, fit=True)

    # --- Scale numerical features ---
    print("Scaling numerical features...")
    df, scaler = scale_numerical(df, numerical_cols, fit=True)

    # --- Define feature columns (all except target and 'year') ---
    feature_cols = [
        col for col in df.columns
        if col not in [target_col, "year"]
    ]

    # --- Train/test split (stratified by encoded 'crop') ---
    print(f"Splitting data: test_size={test_size}, random_state={random_state}...")
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df["crop"],
    )

    # --- Ensure output directory exists ---
    os.makedirs("data/processed", exist_ok=True)

    # --- Save train and test sets ---
    train_path = "data/processed/train.csv"
    test_path = "data/processed/test.csv"
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"✅ Saved: {train_path} (shape: {train_df.shape})")
    print(f"✅ Saved: {test_path} (shape: {test_df.shape})")

    # --- Save encoders and scaler ---
    encoders_path = "data/processed/encoders.joblib"
    scaler_path = "data/processed/scaler.joblib"
    joblib.dump(encoders, encoders_path)
    joblib.dump(scaler, scaler_path)
    print(f"✅ Saved: {encoders_path}")
    print(f"✅ Saved: {scaler_path}")

    # --- Print final feature columns ---
    print(f"\nFinal feature columns ({len(feature_cols)}):")
    for i, col in enumerate(feature_cols, 1):
        print(f"  {i:2d}. {col}")

    print(f"\nTarget column: {target_col}")
    print(f"\nTrain shape: {train_df.shape}")
    print(f"Test shape:  {test_df.shape}")
    print("\nPreprocessing pipeline complete.")


if __name__ == "__main__":
    main()
