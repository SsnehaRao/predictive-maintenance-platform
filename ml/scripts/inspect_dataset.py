from pathlib import Path

import pandas as pd


# ============================================================
# 1. Dataset location
# ============================================================

DATA_PATH = Path(
    r"E:\predictive-maintenance-data\raw\train_FD001.txt"
)


# ============================================================
# 2. Column names
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
# 3. Load dataset
# ============================================================

df = pd.read_csv(
    DATA_PATH,
    sep=r"\s+",
    header=None,
    names=columns,
)


print("=" * 60)
print("PREDICTIVE MAINTENANCE DATASET INSPECTION")
print("=" * 60)


# ============================================================
# 4. Basic information
# ============================================================

print("\n--- BASIC INFORMATION ---")

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Number of engines: {df['engine_id'].nunique()}")


# ============================================================
# 5. Missing values
# ============================================================

print("\n--- MISSING VALUES ---")

missing_values = df.isnull().sum()

print(missing_values)

print(
    f"\nTotal missing values: {missing_values.sum()}"
)


# ============================================================
# 6. Duplicate rows
# ============================================================

print("\n--- DUPLICATE ROWS ---")

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count}")


# ============================================================
# 7. Engine lifetime
# ============================================================

print("\n--- ENGINE LIFETIME ---")

engine_lifetime = (
    df.groupby("engine_id")["cycle"]
    .max()
)

print(engine_lifetime.describe())


# ============================================================
# 8. Shortest and longest engine lives
# ============================================================

print("\nShortest engine lifetimes:")

print(
    engine_lifetime
    .sort_values()
    .head(5)
)

print("\nLongest engine lifetimes:")

print(
    engine_lifetime
    .sort_values(ascending=False)
    .head(5)
)


# ============================================================
# 9. Constant sensors
# ============================================================

print("\n--- SENSOR VARIABILITY ---")

sensor_std = df[sensor_columns].std()

constant_sensors = sensor_std[
    sensor_std == 0
]

print("Constant sensors:")

if len(constant_sensors) == 0:
    print("None")
else:
    print(constant_sensors)


# ============================================================
# 10. Sensor statistics
# ============================================================

print("\n--- SENSOR STATISTICS ---")

sensor_statistics = df[sensor_columns].describe().T

print(sensor_statistics)


# ============================================================
# 11. Finished
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY ANALYSIS COMPLETE")
print("=" * 60)