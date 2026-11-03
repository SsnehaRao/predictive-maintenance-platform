from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# ============================================================
# Paths
# ============================================================

DATA_DIR = Path(
    r"E:\predictive-maintenance-data\processed\fd001"
)

MODEL_PATH = Path(
    r"E:\predictive-maintenance-data\models\random_forest_capped_rul.joblib"
)


# ============================================================
# Configuration
# ============================================================

RUL_CAP = 125


# ============================================================
# Load model and validation data
# ============================================================

model = joblib.load(MODEL_PATH)

validation_df = pd.read_csv(
    DATA_DIR / "validation.csv"
)


# ============================================================
# Prepare features
# ============================================================

X_validation = validation_df.drop(
    columns=["engine_id", "RUL"]
)

actual_rul = validation_df["RUL"]


# ============================================================
# Create capped target
# ============================================================

actual_rul_capped = actual_rul.clip(
    upper=RUL_CAP
)


# ============================================================
# Predict
# ============================================================

predicted_rul = model.predict(
    X_validation
)


# ============================================================
# Metrics against capped RUL
# ============================================================

capped_mae = mean_absolute_error(
    actual_rul_capped,
    predicted_rul,
)

capped_rmse = mean_squared_error(
    actual_rul_capped,
    predicted_rul,
) ** 0.5

capped_r2 = r2_score(
    actual_rul_capped,
    predicted_rul,
)


# ============================================================
# Metrics against raw RUL
# ============================================================

raw_mae = mean_absolute_error(
    actual_rul,
    predicted_rul,
)

raw_rmse = mean_squared_error(
    actual_rul,
    predicted_rul,
) ** 0.5

raw_r2 = r2_score(
    actual_rul,
    predicted_rul,
)


# ============================================================
# Results
# ============================================================

print("=" * 60)
print("CAPPED RUL MODEL — DETAILED EVALUATION")
print("=" * 60)


print("\n--- AGAINST CAPPED RUL ---")

print(
    f"MAE:  {capped_mae:.2f} cycles"
)

print(
    f"RMSE: {capped_rmse:.2f} cycles"
)

print(
    f"R²:   {capped_r2:.4f}"
)


print("\n--- AGAINST RAW RUL ---")

print(
    f"MAE:  {raw_mae:.2f} cycles"
)

print(
    f"RMSE: {raw_rmse:.2f} cycles"
)

print(
    f"R²:   {raw_r2:.4f}"
)


# ============================================================
# Prediction examples
# ============================================================

results = pd.DataFrame(
    {
        "actual_RUL": actual_rul,
        "actual_RUL_capped": actual_rul_capped,
        "predicted_RUL": predicted_rul,
    }
)


results["error_vs_raw"] = (
    results["predicted_RUL"]
    - results["actual_RUL"]
)

results["absolute_error_vs_raw"] = (
    results["error_vs_raw"].abs()
)


print("\n--- EXAMPLE PREDICTIONS ---")

print(
    results.head(10).to_string(
        index=False
    )
)


# ============================================================
# Worst predictions against raw RUL
# ============================================================

print("\n--- WORST 10 RAW-RUL PREDICTIONS ---")

worst = (
    results
    .sort_values(
        "absolute_error_vs_raw",
        ascending=False,
    )
    .head(10)
)

print(
    worst.to_string(
        index=False
    )
)


print("\n" + "=" * 60)
print("DETAILED EVALUATION COMPLETE")
print("=" * 60)