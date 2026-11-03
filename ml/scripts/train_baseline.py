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

DATA_DIR = Path(
    r"E:\predictive-maintenance-data\processed\fd001"
)

MODEL_DIR = Path(
    r"E:\predictive-maintenance-data\models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


TRAIN_PATH = DATA_DIR / "train.csv"
VALIDATION_PATH = DATA_DIR / "validation.csv"


MODEL_PATH = (
    MODEL_DIR / "random_forest_baseline.joblib"
)


# ============================================================
# Load datasets
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
validation_df = pd.read_csv(VALIDATION_PATH)


print("=" * 60)
print("BASELINE MODEL TRAINING")
print("=" * 60)

print("\nTraining shape:")
print(train_df.shape)

print("\nValidation shape:")
print(validation_df.shape)


# ============================================================
# Prepare features and target
# ============================================================

TARGET = "RUL"

DROP_COLUMNS = [
    "engine_id",
    TARGET,
]


X_train = train_df.drop(
    columns=DROP_COLUMNS
)

y_train = train_df[TARGET]


X_validation = validation_df.drop(
    columns=DROP_COLUMNS
)

y_validation = validation_df[TARGET]


print("\nNumber of features:")
print(X_train.shape[1])


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

print("\nTraining Random Forest...")

model.fit(
    X_train,
    y_train,
)


print("Training complete.")


# ============================================================
# Validation prediction
# ============================================================

print("\nGenerating validation predictions...")

predictions = model.predict(
    X_validation
)


# ============================================================
# Evaluation
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


# ============================================================
# Feature importance
# ============================================================

feature_importance = pd.DataFrame(
    {
        "feature": X_train.columns,
        "importance": model.feature_importances_,
    }
).sort_values(
    "importance",
    ascending=False,
)


print("\n--- TOP 15 FEATURES ---")

print(
    feature_importance.head(15).to_string(
        index=False
    )
)


print("\n" + "=" * 60)
print("BASELINE TRAINING COMPLETE")
print("=" * 60)