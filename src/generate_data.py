"""
Synthetic Indian District-Level Crop Dataset Generator
======================================================
Generates 5000 realistic records representing Indian district-level crop data
from 2010–2023. Includes regional weather patterns, soil correlations, real
historical MSP values, and a simulated drift batch for El Niño / drought testing.

Outputs:
    - data/raw/crop_data.csv          (5000 rows)
    - data/reference/reference_data.csv (500 rows — baseline)
    - data/reference/drift_batch.csv    (200 rows — drought simulation)
"""

import os
import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)

# ---------------------------------------------------------------------------
# District–State–Region mapping (30 real Indian districts)
# ---------------------------------------------------------------------------
DISTRICT_STATE_MAP = {
    # Punjab
    "Ludhiana": "Punjab", "Amritsar": "Punjab", "Patiala": "Punjab",
    # Haryana
    "Karnal": "Haryana", "Hisar": "Haryana",
    # Uttar Pradesh
    "Lucknow": "Uttar Pradesh", "Meerut": "Uttar Pradesh", "Gorakhpur": "Uttar Pradesh",
    # Bihar
    "Patna": "Bihar", "Muzaffarpur": "Bihar",
    # West Bengal
    "Bardhaman": "West Bengal", "Hooghly": "West Bengal",
    # Maharashtra
    "Nashik": "Maharashtra", "Pune": "Maharashtra", "Kolhapur": "Maharashtra",
    # Andhra Pradesh
    "Guntur": "Andhra Pradesh", "Krishna": "Andhra Pradesh",
    # Tamil Nadu
    "Coimbatore": "Tamil Nadu", "Thanjavur": "Tamil Nadu",
    # Karnataka
    "Belgaum": "Karnataka", "Mysore": "Karnataka",
    # Madhya Pradesh
    "Indore": "Madhya Pradesh", "Jabalpur": "Madhya Pradesh",
    # Rajasthan
    "Jaipur": "Rajasthan", "Jodhpur": "Rajasthan",
    # Odisha
    "Cuttack": "Odisha",
    # Chhattisgarh
    "Raipur": "Chhattisgarh",
    # Telangana
    "Warangal": "Telangana",
    # Gujarat
    "Ahmedabad": "Gujarat",
    # Assam
    "Nagaon": "Assam",
}

DISTRICTS = list(DISTRICT_STATE_MAP.keys())
STATES = list(DISTRICT_STATE_MAP.values())

# ---------------------------------------------------------------------------
# Soil type distribution per state (realistic)
# ---------------------------------------------------------------------------
STATE_SOIL_MAP = {
    "Punjab":           ["Alluvial"],
    "Haryana":          ["Alluvial", "Desert"],
    "Uttar Pradesh":    ["Alluvial"],
    "Bihar":            ["Alluvial"],
    "West Bengal":      ["Alluvial", "Laterite"],
    "Maharashtra":      ["Black", "Red"],
    "Andhra Pradesh":   ["Black", "Red", "Alluvial"],
    "Tamil Nadu":       ["Red", "Alluvial", "Laterite"],
    "Karnataka":        ["Red", "Black", "Laterite"],
    "Madhya Pradesh":   ["Black", "Alluvial"],
    "Rajasthan":        ["Desert", "Alluvial"],
    "Odisha":           ["Red", "Laterite", "Alluvial"],
    "Chhattisgarh":     ["Red", "Laterite"],
    "Telangana":        ["Black", "Red"],
    "Gujarat":          ["Black", "Alluvial", "Desert"],
    "Assam":            ["Alluvial", "Laterite"],
}

# ---------------------------------------------------------------------------
# Crop–Season mapping (realistic Indian agricultural calendar)
# ---------------------------------------------------------------------------
CROP_SEASON_MAP = {
    "Rice":       ["Kharif"],            # monsoon crop
    "Wheat":      ["Rabi"],              # winter crop
    "Sugarcane":  ["Kharif", "Zaid"],    # long-duration, planted in both
}

# ---------------------------------------------------------------------------
# Regional climate parameters (mean, std) for IMD-realistic weather
# ---------------------------------------------------------------------------
REGION_CLIMATE = {
    # state: (rainfall_mean_mm, rainfall_std, temp_mean_c, temp_std)
    "Punjab":           (550, 120, 24.0, 2.5),
    "Haryana":          (500, 130, 25.0, 2.8),
    "Uttar Pradesh":    (900, 200, 26.0, 2.0),
    "Bihar":            (1100, 250, 27.0, 1.8),
    "West Bengal":      (1600, 300, 27.5, 1.5),
    "Maharashtra":      (1200, 350, 27.0, 2.0),
    "Andhra Pradesh":   (950, 280, 28.5, 1.5),
    "Tamil Nadu":       (1000, 300, 29.0, 1.2),
    "Karnataka":        (1100, 320, 27.5, 1.8),
    "Madhya Pradesh":   (1050, 280, 26.5, 2.2),
    "Rajasthan":        (400, 150, 28.0, 3.0),
    "Odisha":           (1400, 300, 27.5, 1.5),
    "Chhattisgarh":     (1300, 280, 27.0, 1.8),
    "Telangana":        (950, 250, 28.0, 1.5),
    "Gujarat":          (800, 250, 28.0, 2.5),
    "Assam":            (2000, 400, 25.0, 1.5),
}

# ---------------------------------------------------------------------------
# Irrigation percentage ranges per district (realistic)
# ---------------------------------------------------------------------------
DISTRICT_IRRIGATION = {
    "Ludhiana": (80, 98), "Amritsar": (85, 98), "Patiala": (75, 95),
    "Karnal": (80, 95), "Hisar": (50, 75),
    "Lucknow": (55, 80), "Meerut": (70, 90), "Gorakhpur": (40, 65),
    "Patna": (45, 70), "Muzaffarpur": (35, 60),
    "Bardhaman": (40, 65), "Hooghly": (35, 60),
    "Nashik": (25, 55), "Pune": (30, 55), "Kolhapur": (30, 55),
    "Guntur": (45, 70), "Krishna": (50, 75),
    "Coimbatore": (50, 75), "Thanjavur": (60, 85),
    "Belgaum": (25, 50), "Mysore": (30, 55),
    "Indore": (35, 60), "Jabalpur": (25, 50),
    "Jaipur": (30, 55), "Jodhpur": (15, 40),
    "Cuttack": (35, 60), "Raipur": (25, 50),
    "Warangal": (40, 65), "Ahmedabad": (45, 70),
    "Nagaon": (25, 50),
}

# ---------------------------------------------------------------------------
# Real historical MSP values (INR per quintal) — India government data
# Source: Commission for Agricultural Costs & Prices (CACP)
# ---------------------------------------------------------------------------
MSP_DATA = {
    "Rice": {
        2010: 1000, 2011: 1080, 2012: 1250, 2013: 1310, 2014: 1360,
        2015: 1410, 2016: 1470, 2017: 1550, 2018: 1750, 2019: 1815,
        2020: 1868, 2021: 1940, 2022: 2040, 2023: 2183,
    },
    "Wheat": {
        2010: 1100, 2011: 1120, 2012: 1285, 2013: 1350, 2014: 1400,
        2015: 1450, 2016: 1525, 2017: 1625, 2018: 1735, 2019: 1840,
        2020: 1925, 2021: 1975, 2022: 2015, 2023: 2125,
    },
    "Sugarcane": {
        2010: 1450, 2011: 1450, 2012: 1700, 2013: 1800, 2014: 1900,
        2015: 2100, 2016: 2300, 2017: 2550, 2018: 2750, 2019: 2750,
        2020: 2850, 2021: 2900, 2022: 3050, 2023: 3150,
    },
}

# ---------------------------------------------------------------------------
# Yield ranges per crop (kg/ha) — baseline values
# ---------------------------------------------------------------------------
YIELD_RANGES = {
    "Rice":       (1500, 4500),
    "Wheat":      (1800, 5000),
    "Sugarcane":  (40000, 90000),
}


def _compute_yield(
    crop: str,
    rainfall_mm: float,
    temperature_avg_c: float,
    irrigation_pct: float,
    fertilizer_kg_per_ha: float,
    soil_type: str,
) -> float:
    """
    Compute a realistic crop yield using weighted feature contributions
    with regional correlations:
        - Higher rainfall → higher yield (up to a point)
        - Higher irrigation → higher yield
        - Optimal temperature band per crop
        - Soil suitability multiplier
        - Fertilizer responsiveness
    """
    ymin, ymax = YIELD_RANGES[crop]
    base = (ymin + ymax) / 2.0

    # --- Rainfall contribution (diminishing returns, excess hurts) ---
    if crop == "Sugarcane":
        optimal_rain = 1500.0
    elif crop == "Rice":
        optimal_rain = 1200.0
    else:
        optimal_rain = 600.0
    rain_factor = 1.0 - abs(rainfall_mm - optimal_rain) / (optimal_rain * 2.0)
    rain_factor = np.clip(rain_factor, 0.3, 1.2)

    # --- Temperature contribution (crop-specific optima) ---
    optimal_temp = {"Rice": 27.0, "Wheat": 20.0, "Sugarcane": 30.0}[crop]
    temp_deviation = abs(temperature_avg_c - optimal_temp)
    temp_factor = 1.0 - (temp_deviation / 20.0)
    temp_factor = np.clip(temp_factor, 0.5, 1.1)

    # --- Irrigation contribution ---
    irr_factor = 0.7 + 0.3 * (irrigation_pct / 100.0)

    # --- Fertilizer contribution (diminishing returns) ---
    fert_factor = 0.6 + 0.4 * np.log1p(fertilizer_kg_per_ha) / np.log1p(300)

    # --- Soil suitability multiplier ---
    soil_bonus = {
        "Rice":       {"Alluvial": 1.10, "Black": 0.95, "Red": 0.90, "Laterite": 0.85, "Desert": 0.70},
        "Wheat":      {"Alluvial": 1.10, "Black": 1.00, "Red": 0.85, "Laterite": 0.80, "Desert": 0.75},
        "Sugarcane":  {"Alluvial": 1.05, "Black": 1.10, "Red": 0.90, "Laterite": 0.85, "Desert": 0.65},
    }
    soil_factor = soil_bonus[crop].get(soil_type, 0.85)

    # --- Combine factors ---
    combined = base * rain_factor * temp_factor * irr_factor * fert_factor * soil_factor

    # --- Add stochastic noise (±8%) ---
    noise = np.random.uniform(0.92, 1.08)
    yield_val = combined * noise

    return float(np.clip(yield_val, ymin, ymax))


def generate_dataset(n_rows: int = 5000) -> pd.DataFrame:
    """Generate a synthetic Indian district-level crop dataset."""
    records = []

    crops = list(CROP_SEASON_MAP.keys())
    years = list(range(2010, 2024))

    for _ in range(n_rows):
        district = np.random.choice(DISTRICTS)
        state = DISTRICT_STATE_MAP[district]
        crop = np.random.choice(crops)
        year = int(np.random.choice(years))
        season = np.random.choice(CROP_SEASON_MAP[crop])

        # --- Climate (IMD-realistic per region) ---
        r_mean, r_std, t_mean, t_std = REGION_CLIMATE[state]
        rainfall_mm = round(max(50, np.random.normal(r_mean, r_std)), 1)
        temperature_avg_c = round(np.random.normal(t_mean, t_std), 1)

        # --- Soil (realistic per state) ---
        soil_type = np.random.choice(STATE_SOIL_MAP[state])

        # --- Irrigation (realistic per district) ---
        irr_lo, irr_hi = DISTRICT_IRRIGATION[district]
        irrigation_pct = round(np.random.uniform(irr_lo, irr_hi), 1)

        # --- Fertilizer (realistic range 50–300 kg/ha) ---
        fertilizer_kg_per_ha = round(np.random.uniform(50, 300), 1)

        # --- MSP (real historical data) ---
        msp_inr_per_quintal = MSP_DATA[crop][year]

        # --- Yield (computed with correlations) ---
        yield_kg_per_ha = round(
            _compute_yield(
                crop, rainfall_mm, temperature_avg_c,
                irrigation_pct, fertilizer_kg_per_ha, soil_type,
            ),
            1,
        )

        records.append({
            "district": district,
            "state": state,
            "crop": crop,
            "year": year,
            "season": season,
            "rainfall_mm": rainfall_mm,
            "temperature_avg_c": temperature_avg_c,
            "soil_type": soil_type,
            "irrigation_pct": irrigation_pct,
            "fertilizer_kg_per_ha": fertilizer_kg_per_ha,
            "msp_inr_per_quintal": msp_inr_per_quintal,
            "yield_kg_per_ha": yield_kg_per_ha,
        })

    return pd.DataFrame(records)


def generate_drift_batch(reference_df: pd.DataFrame, n_rows: int = 200) -> pd.DataFrame:
    """
    Create a simulated drought / El Niño drift batch:
        - Rainfall reduced by 25%
        - Temperature increased by 2°C
        - Yield recomputed under stressed conditions
    """
    drift_df = reference_df.sample(n=n_rows, random_state=SEED).copy()

    drift_df["rainfall_mm"] = (drift_df["rainfall_mm"] * 0.75).round(1)
    drift_df["temperature_avg_c"] = (drift_df["temperature_avg_c"] + 2.0).round(1)

    # Recompute yield under drought stress
    drift_df["yield_kg_per_ha"] = drift_df.apply(
        lambda row: round(
            _compute_yield(
                row["crop"], row["rainfall_mm"], row["temperature_avg_c"],
                row["irrigation_pct"], row["fertilizer_kg_per_ha"], row["soil_type"],
            ),
            1,
        ),
        axis=1,
    )

    return drift_df.reset_index(drop=True)


def print_summary(df: pd.DataFrame, label: str = "Dataset") -> None:
    """Print a concise summary of the dataset."""
    print(f"\n{'='*60}")
    print(f"  {label} Summary")
    print(f"{'='*60}")
    print(f"  Rows           : {len(df)}")
    print(f"  Columns        : {list(df.columns)}")
    print(f"\n  Yield Statistics per Crop (kg/ha):")
    print(f"  {'-'*50}")
    for crop in ["Rice", "Wheat", "Sugarcane"]:
        subset = df[df["crop"] == crop]["yield_kg_per_ha"]
        if len(subset) > 0:
            print(
                f"  {crop:12s} | count={len(subset):4d} | "
                f"mean={subset.mean():10.1f} | "
                f"min={subset.min():10.1f} | "
                f"max={subset.max():10.1f}"
            )
    print(f"{'='*60}\n")


def main() -> None:
    """Generate all datasets and save to disk."""
    # --- Ensure output directories exist ---
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/reference", exist_ok=True)

    # --- Generate main dataset (5000 rows) ---
    print("Generating synthetic Indian crop dataset (5000 rows)...")
    df = generate_dataset(n_rows=5000)

    # --- Save main dataset ---
    raw_path = "data/raw/crop_data.csv"
    df.to_csv(raw_path, index=False)
    print(f"✅ Saved: {raw_path} ({len(df)} rows)")

    # --- Save reference baseline (first 500 rows) ---
    reference_df = df.head(500).copy()
    ref_path = "data/reference/reference_data.csv"
    reference_df.to_csv(ref_path, index=False)
    print(f"✅ Saved: {ref_path} ({len(reference_df)} rows)")

    # --- Generate and save drift batch (200 rows, drought simulation) ---
    drift_df = generate_drift_batch(reference_df, n_rows=200)
    drift_path = "data/reference/drift_batch.csv"
    drift_df.to_csv(drift_path, index=False)
    print(f"✅ Saved: {drift_path} ({len(drift_df)} rows)")

    # --- Print summaries ---
    print_summary(df, "Full Dataset (data/raw/crop_data.csv)")
    print_summary(drift_df, "Drift Batch (data/reference/drift_batch.csv)")

    print("All 3 files saved successfully.")


if __name__ == "__main__":
    main()
