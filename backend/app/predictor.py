from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# Model configuration
# ============================================================

RUL_CAP = 125

MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "models"
    / "random_forest_capped_rul.joblib"
)


# ============================================================
# Load model once when application starts
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )


model = joblib.load(MODEL_PATH)


# ============================================================
# Feature order
# ============================================================

FEATURE_COLUMNS = [
    "cycle",
    "setting_1",
    "setting_2",
    "setting_3",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_17",
    "sensor_20",
    "sensor_21",
    "sensor_2_diff",
    "sensor_2_rolling_mean_5",
    "sensor_2_rolling_std_5",
    "sensor_3_diff",
    "sensor_3_rolling_mean_5",
    "sensor_3_rolling_std_5",
    "sensor_4_diff",
    "sensor_4_rolling_mean_5",
    "sensor_4_rolling_std_5",
    "sensor_6_diff",
    "sensor_6_rolling_mean_5",
    "sensor_6_rolling_std_5",
    "sensor_7_diff",
    "sensor_7_rolling_mean_5",
    "sensor_7_rolling_std_5",
    "sensor_8_diff",
    "sensor_8_rolling_mean_5",
    "sensor_8_rolling_std_5",
    "sensor_9_diff",
    "sensor_9_rolling_mean_5",
    "sensor_9_rolling_std_5",
    "sensor_11_diff",
    "sensor_11_rolling_mean_5",
    "sensor_11_rolling_std_5",
    "sensor_12_diff",
    "sensor_12_rolling_mean_5",
    "sensor_12_rolling_std_5",
    "sensor_13_diff",
    "sensor_13_rolling_mean_5",
    "sensor_13_rolling_std_5",
    "sensor_14_diff",
    "sensor_14_rolling_mean_5",
    "sensor_14_rolling_std_5",
    "sensor_15_diff",
    "sensor_15_rolling_mean_5",
    "sensor_15_rolling_std_5",
    "sensor_17_diff",
    "sensor_17_rolling_mean_5",
    "sensor_17_rolling_std_5",
    "sensor_20_diff",
    "sensor_20_rolling_mean_5",
    "sensor_20_rolling_std_5",
    "sensor_21_diff",
    "sensor_21_rolling_mean_5",
    "sensor_21_rolling_std_5",
]


# ============================================================
# Prediction function
# ============================================================

def predict_rul(features: dict) -> float:
    """
    Generate a capped RUL prediction.

    Parameters
    ----------
    features:
        Dictionary containing all model input features.

    Returns
    -------
    float
        Predicted RUL, capped between 0 and 125.
    """

    input_data = pd.DataFrame(
        [features],
        columns=FEATURE_COLUMNS,
    )

    prediction = model.predict(
        input_data
    )[0]

    prediction = max(
        0.0,
        min(float(prediction), RUL_CAP),
    )

    return round(
        prediction,
        2,
    )


# ============================================================
# Health status
# ============================================================

def get_health_status(predicted_rul: float) -> str:
    """
    Convert predicted RUL into a human-readable status.
    """

    if predicted_rul > 80:
        return "healthy"

    if predicted_rul > 40:
        return "warning"

    return "critical"