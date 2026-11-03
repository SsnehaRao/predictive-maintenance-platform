from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = (
    PROJECT_ROOT / "data" / "processed" / "fd001"
)

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


TRAIN_PATH = DATA_DIR / "train.csv"
VALIDATION_PATH = DATA_DIR / "validation.csv"

MODEL_PATH = (
    MODEL_DIR / "random_forest_capped_rul.joblib"
)


# ============================================================
# Configuration
# ============================================================

RUL_CAP = 125


# ============================================================
# Load datasets
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
validation_df = pd.read_csv(VALIDATION_PATH)


print("=" * 60)
print("CAPPED RUL RANDOM FOREST")
print("=" * 60)

print(f"\nRUL cap: {RUL_CAP}")


# ============================================================
# Cap RUL
# ============================================================

train_df["RUL_capped"] = (
    train_df["RUL"].clip(
        upper=RUL_CAP
    )
)

validation_df["RUL_capped"] = (
    validation_df["RUL"].clip(
        upper=RUL_CAP
    )
)


# ============================================================
# Prepare features
# ============================================================

DROP_COLUMNS = [
    "engine_id",
    "RUL",
    "RUL_capped",
]


X_train = train_df.drop(
    columns=DROP_COLUMNS
)

y_train = train_df["RUL_capped"]


X_validation = validation_df.drop(
    columns=DROP_COLUMNS
)

y_validation = validation_df["RUL_capped"]


print("\nTraining shape:")
print(X_train.shape)

print("\nValidation shape:")
print(X_validation.shape)


# ============================================================
# Create model
# ============================================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
)


# ============================================================
# Train
# ============================================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train,
)

print("Training complete.")


# ============================================================
# Predict
# ============================================================

predictions = model.predict(
    X_validation
)


# ============================================================
# Evaluate against capped target
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


print("\n--- VALIDATION RESULTS ---")

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
# Save model
# ============================================================

joblib.dump(
    model,
    MODEL_PATH,
)


print("\nModel saved to:")
print(MODEL_PATH)


print("\n" + "=" * 60)
print("CAPPED RUL TRAINING COMPLETE")
print("=" * 60)