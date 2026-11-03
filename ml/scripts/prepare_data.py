from pathlib import Path

import pandas as pd


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw"

OUTPUT_DIR = (
    PROJECT_ROOT / "data" / "processed" / "fd001"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


TRAIN_PATH = DATA_DIR / "train_FD001.txt"


# ============================================================
# Column names
# ============================================================

columns = [
    "engine_id",
    "cycle",
    "setting_1",
    "setting_2",
    "setting_3",
]

sensor_columns = [
    f"sensor_{i}"
    for i in range(1, 22)
]

columns.extend(sensor_columns)


# ============================================================
# Load training data
# ============================================================

df = pd.read_csv(
    TRAIN_PATH,
    sep=r"\s+",
    header=None,
    names=columns,
)


print("=" * 60)
print("PREPARING FD001 DATASET")
print("=" * 60)

print(f"\nOriginal shape: {df.shape}")


# ============================================================
# Calculate RUL
# ============================================================

max_cycle = (
    df.groupby("engine_id")["cycle"]
    .transform("max")
)

df["RUL"] = max_cycle - df["cycle"]


print("\nRUL created successfully.")

print("\nRUL statistics:")
print(df["RUL"].describe())


# ============================================================
# Identify low-variance sensors
# ============================================================

sensor_std = df[sensor_columns].std()

low_variance_sensors = sensor_std[
    sensor_std < 1e-6
].index.tolist()


print("\nLow-variance sensors:")

for sensor in low_variance_sensors:
    print(f"  - {sensor}")


# ============================================================
# Remove low-variance sensors
# ============================================================

df_clean = df.drop(
    columns=low_variance_sensors
)


print(
    f"\nShape after removing "
    f"low-variance sensors: {df_clean.shape}"
)


# ============================================================
# Save processed dataset
# ============================================================

output_path = (
    OUTPUT_DIR / "train_fd001_processed.csv"
)

df_clean.to_csv(
    output_path,
    index=False,
)


print("\nProcessed dataset saved to:")
print(output_path)


# ============================================================
# Final information
# ============================================================

print("\nFinal columns:")

print(df_clean.columns.tolist())


print("\nFirst 5 rows:")

print(df_clean.head())


print("\n" + "=" * 60)
print("DATA PREPARATION COMPLETE")
print("=" * 60)