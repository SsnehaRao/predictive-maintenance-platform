import pandas as pd


SENSOR_COLUMNS = [
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
]


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the same features used during model training.
    """

    df = df.copy()

    df = df.sort_values(
        ["engine_id", "cycle"]
    ).reset_index(drop=True)

    for sensor in SENSOR_COLUMNS:

        # Previous-cycle change
        df[f"{sensor}_diff"] = (
            df.groupby("engine_id")[sensor]
            .diff()
        )

        # Rolling mean over 5 cycles
        df[f"{sensor}_rolling_mean_5"] = (
            df.groupby("engine_id")[sensor]
            .transform(
                lambda x: x.rolling(
                    window=5,
                    min_periods=1,
                ).mean()
            )
        )

        # Rolling standard deviation over 5 cycles
        df[f"{sensor}_rolling_std_5"] = (
            df.groupby("engine_id")[sensor]
            .transform(
                lambda x: x.rolling(
                    window=5,
                    min_periods=1,
                ).std()
            )
        )

    # Same NaN handling used during training
    feature_columns = [
        column
        for column in df.columns
        if column.endswith("_diff")
        or column.endswith("_rolling_std_5")
    ]

    df[feature_columns] = (
        df[feature_columns]
        .fillna(0)
    )

    return df