from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import HistGradientBoostingRegressor
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
    MODEL_DIR / "hist_gradient_boosting.joblib"
)


# ============================================================
# Load data
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
validation_df = pd.read_csv(VALIDATION_PATH)


print("=" * 60)
print("HISTOGRAM GRADIENT BOOSTING")
print("=" * 60)


# ============================================================
# Prepare features
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


print("\nTraining shape:")
print(X_train.shape)

print("\nValidation shape:")
print(X_validation.shape)

print("\nNumber of features:")
print(X_train.shape[1])


# ============================================================
# Create model
# ============================================================

model = HistGradientBoostingRegressor(
    max_iter=300,
    learning_rate=0.08,
    max_leaf_nodes=31,
    l2_regularization=1.0,
    random_state=42,
)


# ============================================================
# Train
# ============================================================

print("\nTraining HistGradientBoosting...")

model.fit(
    X_train,
    y_train,
)

print("Training complete.")


# ============================================================
# Predict
# ============================================================

print("\nGenerating validation predictions...")

predictions = model.predict(
    X_validation
)


# ============================================================
# Evaluate
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
print("BOOSTING TRAINING COMPLETE")
print("=" * 60)