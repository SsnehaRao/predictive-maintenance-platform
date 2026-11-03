from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    engine_id: int = Field(
        ...,
        ge=1,
        description="Engine ID",
    )

    cycle: float = Field(
        ...,
        ge=1,
        description="Current engine cycle",
    )

    setting_1: float
    setting_2: float
    setting_3: float

    sensor_2: float
    sensor_3: float
    sensor_4: float
    sensor_6: float
    sensor_7: float
    sensor_8: float
    sensor_9: float
    sensor_11: float
    sensor_12: float
    sensor_13: float
    sensor_14: float
    sensor_15: float
    sensor_17: float
    sensor_20: float
    sensor_21: float

    sensor_2_diff: float
    sensor_2_rolling_mean_5: float
    sensor_2_rolling_std_5: float

    sensor_3_diff: float
    sensor_3_rolling_mean_5: float
    sensor_3_rolling_std_5: float

    sensor_4_diff: float
    sensor_4_rolling_mean_5: float
    sensor_4_rolling_std_5: float

    sensor_6_diff: float
    sensor_6_rolling_mean_5: float
    sensor_6_rolling_std_5: float

    sensor_7_diff: float
    sensor_7_rolling_mean_5: float
    sensor_7_rolling_std_5: float

    sensor_8_diff: float
    sensor_8_rolling_mean_5: float
    sensor_8_rolling_std_5: float

    sensor_9_diff: float
    sensor_9_rolling_mean_5: float
    sensor_9_rolling_std_5: float

    sensor_11_diff: float
    sensor_11_rolling_mean_5: float
    sensor_11_rolling_std_5: float

    sensor_12_diff: float
    sensor_12_rolling_mean_5: float
    sensor_12_rolling_std_5: float

    sensor_13_diff: float
    sensor_13_rolling_mean_5: float
    sensor_13_rolling_std_5: float

    sensor_14_diff: float
    sensor_14_rolling_mean_5: float
    sensor_14_rolling_std_5: float

    sensor_15_diff: float
    sensor_15_rolling_mean_5: float
    sensor_15_rolling_std_5: float

    sensor_17_diff: float
    sensor_17_rolling_mean_5: float
    sensor_17_rolling_std_5: float

    sensor_20_diff: float
    sensor_20_rolling_mean_5: float
    sensor_20_rolling_std_5: float

    sensor_21_diff: float
    sensor_21_rolling_mean_5: float
    sensor_21_rolling_std_5: float


class PredictionResponse(BaseModel):
    predicted_rul: float
    health_status: str
    model: str


class TelemetryRequest(BaseModel):
    engine_id: int = Field(
        ...,
        ge=1,
        description="Engine ID must be at least 1",
    )

    cycle: int = Field(
        ...,
        ge=1,
        description="Engine cycle must be at least 1",
    )

    setting_1: float | None = None
    setting_2: float | None = None
    setting_3: float | None = None

    sensor_2: float | None = None
    sensor_3: float | None = None
    sensor_4: float | None = None
    sensor_6: float | None = None
    sensor_7: float | None = None
    sensor_8: float | None = None
    sensor_9: float | None = None
    sensor_11: float | None = None
    sensor_12: float | None = None
    sensor_13: float | None = None
    sensor_14: float | None = None
    sensor_15: float | None = None
    sensor_17: float | None = None
    sensor_20: float | None = None
    sensor_21: float | None = None


class TelemetryResponse(BaseModel):
    message: str
    engine_id: int
    cycle: int