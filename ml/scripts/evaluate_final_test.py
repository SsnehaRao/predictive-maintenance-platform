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
# Load model and test data
# ============================================================

print("=" * 60)
print("FINAL TEST EVALUATION")
print("=" * 60)

print("\nLoading model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")


test_df = pd.read_csv(
    DATA_DIR / "test.csv"
)


print("\nTest shape:")
print(test_df.shape)

print("\nTest engines:")
print(test_df["engine_id"].nunique())


# ============================================================
# Prepare features
# ============================================================

X_test = test_df.drop(
    columns=["engine_id", "RUL"]
)

actual_rul = test_df["RUL"]

actual_rul_capped = actual_rul.clip(
    upper=RUL_CAP
)


# ============================================================
# Predict
# ============================================================

print("\nGenerating test predictions...")

predictions = model.predict(
    X_test
)


# ============================================================
# Capped-RUL evaluation
# ============================================================

mae = mean_absolute_error(
    actual_rul_capped,
    predictions,
)

rmse = mean_squared_error(
    actual_rul_capped,
    predictions,
) ** 0.5

r2 = r2_score(
    actual_rul_capped,
    predictions,
)


# ============================================================
# Raw-RUL evaluation
# ============================================================

raw_mae = mean_absolute_error(
    actual_rul,
    predictions,
)

raw_rmse = mean_squared_error(
    actual_rul,
    predictions,
) ** 0.5

raw_r2 = r2_score(
    actual_rul,
    predictions,
)


# ============================================================
# Results
# ============================================================

print("\n--- FINAL TEST RESULTS: CAPPED RUL ---")

print(
    f"MAE:  {mae:.2f} cycles"
)

print(
    f"RMSE: {rmse:.2f} cycles"
)

print(
    f"R²:   {r2:.4f}"
)


print("\n--- FINAL TEST RESULTS: RAW RUL ---")

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
# Add predictions
# ============================================================

results = test_df[
    ["engine_id", "cycle", "RUL"]
].copy()

results["actual_RUL_capped"] = (
    actual_rul_capped
)

results["predicted_RUL"] = predictions

results["error"] = (
    results["predicted_RUL"]
    - results["actual_RUL_capped"]
)

results["absolute_error"] = (
    results["error"].abs()
)


# ============================================================
# Engine-level performance
# ============================================================

engine_mae = (
    results
    .groupby("engine_id")["absolute_error"]
    .mean()
    .sort_values(ascending=False)
)


print("\n--- TEST ENGINE PERFORMANCE ---")

print(engine_mae.to_string())


# ============================================================
# Worst predictions
# ============================================================

print("\n--- WORST 10 TEST PREDICTIONS ---")

worst = (
    results
    .sort_values(
        "absolute_error",
        ascending=False,
    )
    .head(10)
)

print(
    worst[
        [
            "engine_id",
            "cycle",
            "RUL",
            "actual_RUL_capped",
            "predicted_RUL",
            "error",
            "absolute_error",
        ]
    ].to_string(index=False)
)


# ============================================================
# Save predictions
# ============================================================

output_path = (
    DATA_DIR / "final_test_predictions.csv"
)

results.to_csv(
    output_path,
    index=False,
)


print("\nPredictions saved to:")

print(output_path)


print("\n" + "=" * 60)
print("FINAL TEST EVALUATION COMPLETE")
print("=" * 60)