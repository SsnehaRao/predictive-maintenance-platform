from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ============================================================
# Paths
# ============================================================

DATA_PATH = Path(
    r"E:\predictive-maintenance-data\raw\train_FD001.txt"
)

OUTPUT_DIR = Path(
    r"E:\predictive-maintenance-data\eda\plots"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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
# Load data
# ============================================================

df = pd.read_csv(
    DATA_PATH,
    sep=r"\s+",
    header=None,
    names=columns,
)


print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ============================================================
# 1. Check sensor uniqueness
# ============================================================

print("\n--- SENSOR UNIQUENESS ---")

for sensor in sensor_columns:
    unique_count = df[sensor].nunique()

    print(
        f"{sensor:10s} -> "
        f"{unique_count:5d} unique values"
    )


# ============================================================
# 2. Engine lifetime distribution
# ============================================================

engine_lifetime = (
    df.groupby("engine_id")["cycle"]
    .max()
)


plt.figure(figsize=(10, 6))

plt.hist(
    engine_lifetime,
    bins=15,
)

plt.xlabel("Engine lifetime (cycles)")
plt.ylabel("Number of engines")
plt.title("Distribution of Engine Lifetimes")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "engine_lifetime_distribution.png",
    dpi=150,
)

plt.close()


# ============================================================
# 3. Sensor trends for Engine 1
# ============================================================

engine_1 = df[df["engine_id"] == 1]


for sensor in sensor_columns:

    plt.figure(figsize=(10, 5))

    plt.plot(
        engine_1["cycle"],
        engine_1[sensor],
    )

    plt.xlabel("Cycle")
    plt.ylabel(sensor)
    plt.title(
        f"{sensor} behavior - Engine 1"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"engine_1_{sensor}.png",
        dpi=120,
    )

    plt.close()

# ============================================================
# 3B. Sensor trends for Engine 56
# ============================================================

engine_56 = df[df["engine_id"] == 56]


for sensor in sensor_columns:

    plt.figure(figsize=(10, 5))

    plt.plot(
        engine_56["cycle"],
        engine_56[sensor],
    )

    plt.xlabel("Cycle")
    plt.ylabel(sensor)
    plt.title(
        f"{sensor} behavior - Engine 56"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"engine_56_{sensor}.png",
        dpi=120,
    )

    plt.close()


# ============================================================
# 4. Sensor correlation with cycle
# ============================================================

correlations = (
    df[["cycle"] + sensor_columns]
    .corr()["cycle"]
    .drop("cycle")
    .sort_values()
)


print("\n--- SENSOR / CYCLE CORRELATION ---")

print(correlations)


plt.figure(figsize=(10, 7))

correlations.plot(
    kind="bar",
)

plt.xlabel("Sensor")
plt.ylabel("Correlation with cycle")
plt.title(
    "Sensor Correlation with Operating Cycle"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "sensor_cycle_correlation.png",
    dpi=150,
)

plt.close()


# ============================================================
# 5. Sensor standard deviation
# ============================================================

sensor_std = (
    df[sensor_columns]
    .std()
    .sort_values()
)


print("\n--- SENSOR STANDARD DEVIATION ---")

print(sensor_std)


plt.figure(figsize=(10, 7))

sensor_std.plot(
    kind="bar",
)

plt.xlabel("Sensor")
plt.ylabel("Standard deviation")
plt.title("Sensor Variability")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "sensor_variability.png",
    dpi=150,
)

plt.close()


# ============================================================
# Finished
# ============================================================

print("\nEDA plots saved to:")

print(OUTPUT_DIR)

print("\n" + "=" * 60)
print("EDA COMPLETE")
print("=" * 60)