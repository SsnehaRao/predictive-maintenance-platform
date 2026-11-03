from pathlib import Path

import joblib
import matplotlib.pyplot as plt
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
    r"E:\predictive-maintenance-data\models\random_forest_baseline.joblib"
)

OUTPUT_DIR = Path(
    r"E:\predictive-maintenance-data\eda\plots"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


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

y_validation = validation_df["RUL"]


# ============================================================
# Predictions
# ============================================================

predictions = model.predict(
    X_validation
)


validation_df["predicted_RUL"] = predictions

validation_df["error"] = (
    validation_df["predicted_RUL"]
    - validation_df["RUL"]
)

validation_df["absolute_error"] = (
    validation_df["error"].abs()
)


# ============================================================
# Overall metrics
# ============================================================

mae = mean_absolute_error(
    y_validation,
    predictions,
)

rmse = mean_squared_error(
    y_validation,
    predictions,
) ** 0.5

r2 = r2_score(
    y_validation,
    predictions,
)


print("=" * 60)
print("BASELINE MODEL EVALUATION")
print("=" * 60)


print("\n--- OVERALL METRICS ---")

print(
    f"MAE:  {mae:.2f} cycles"
)

print(
    f"RMSE: {rmse:.2f} cycles"
)

print(
    f"R²:   {r2:.4f}"
)


# ============================================================
# Worst predictions
# ============================================================

print("\n--- WORST 10 PREDICTIONS ---")

worst_predictions = (
    validation_df[
        [
            "engine_id",
            "cycle",
            "RUL",
            "predicted_RUL",
            "error",
            "absolute_error",
        ]
    ]
    .sort_values(
        "absolute_error",
        ascending=False,
    )
    .head(10)
)

print(
    worst_predictions.to_string(
        index=False
    )
)


# ============================================================
# Engine-level MAE
# ============================================================

engine_errors = (
    validation_df
    .groupby("engine_id")["absolute_error"]
    .mean()
    .sort_values(ascending=False)
)


print("\n--- WORST ENGINES ---")

print(
    engine_errors.head(10)
)


# ============================================================
# Actual vs predicted plot
# ============================================================

plt.figure(figsize=(8, 8))

plt.scatter(
    y_validation,
    predictions,
    alpha=0.3,
)

min_value = min(
    y_validation.min(),
    predictions.min(),
)

max_value = max(
    y_validation.max(),
    predictions.max(),
)

plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linestyle="--",
)

plt.xlabel("Actual RUL")
plt.ylabel("Predicted RUL")

plt.title(
    "Actual vs Predicted RUL - Baseline"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "baseline_actual_vs_predicted.png",
    dpi=150,
)

plt.close()


# ============================================================
# Error distribution
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    validation_df["error"],
    bins=40,
)

plt.axvline(
    0,
    linestyle="--",
)

plt.xlabel("Prediction Error")
plt.ylabel("Number of Predictions")

plt.title(
    "Baseline RUL Prediction Error Distribution"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "baseline_error_distribution.png",
    dpi=150,
)

plt.close()


# ============================================================
# Finished
# ============================================================

print("\nEvaluation plots saved to:")

print(OUTPUT_DIR)

print("\n" + "=" * 60)
print("BASELINE EVALUATION COMPLETE")
print("=" * 60)