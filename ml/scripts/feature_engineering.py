from pathlib import Path

import pandas as pd


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    PROJECT_ROOT / "data" / "processed" / "fd001"
)

INPUT_PATH = (
    OUTPUT_DIR / "train_fd001_processed.csv"
)
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


OUTPUT_PATH = OUTPUT_DIR / "train_fd001_features.csv"


# ============================================================
# Load processed dataset
# ============================================================

df = pd.read_csv(INPUT_PATH)

print("=" * 60)
print("FEATURE ENGINEERING")
print("=" * 60)

print(f"\nInput shape: {df.shape}")


# ============================================================
# Identify sensor columns
# ============================================================

sensor_columns = [
    column
    for column in df.columns
    if column.startswith("sensor_")
]

print(f"\nNumber of sensors: {len(sensor_columns)}")


# ============================================================
# Sort data correctly
# ============================================================

df = df.sort_values(
    ["engine_id", "cycle"]
).reset_index(drop=True)


# ============================================================
# Create features
# ============================================================

for sensor in sensor_columns:

    # --------------------------------------------------------
    # Previous-cycle change
    # --------------------------------------------------------

    df[f"{sensor}_diff"] = (
        df.groupby("engine_id")[sensor]
        .diff()
    )


    # --------------------------------------------------------
    # Rolling mean over previous 5 cycles
    # --------------------------------------------------------

    df[f"{sensor}_rolling_mean_5"] = (
        df.groupby("engine_id")[sensor]
        .transform(
            lambda x: x.rolling(
                window=5,
                min_periods=1
            ).mean()
        )
    )


    # --------------------------------------------------------
    # Rolling standard deviation over previous 5 cycles
    # --------------------------------------------------------

    df[f"{sensor}_rolling_std_5"] = (
        df.groupby("engine_id")[sensor]
        .transform(
            lambda x: x.rolling(
                window=5,
                min_periods=1
            ).std()
        )
    )


# ============================================================
# Fill NaN values created by diff/std calculations
# ============================================================

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


# ============================================================
# Check result
# ============================================================

print(f"\nOutput shape: {df.shape}")

print("\nMissing values after feature engineering:")

print(
    df.isnull().sum().sum()
)


# ============================================================
# Save
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nFeature-engineered dataset saved to:")

print(OUTPUT_PATH)


# ============================================================
# Show example
# ============================================================

print("\nExample columns:")

print(
    df.columns.tolist()[:30]
)


print("\nFirst 5 rows:")

print(
    df.head()
)


print("\n" + "=" * 60)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 60)