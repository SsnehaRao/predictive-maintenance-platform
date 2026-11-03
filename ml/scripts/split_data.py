from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


# ============================================================
# Paths
# ============================================================

INPUT_PATH = Path(
    r"E:\predictive-maintenance-data\processed\fd001\train_fd001_features.csv"
)

OUTPUT_DIR = Path(
    r"E:\predictive-maintenance-data\processed\fd001"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Configuration
# ============================================================

RANDOM_STATE = 42

TRAIN_SIZE = 0.70
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15


# ============================================================
# Load dataset
# ============================================================

df = pd.read_csv(INPUT_PATH)

print("=" * 60)
print("ENGINE-BASED DATASET SPLITTING")
print("=" * 60)

print(f"\nTotal rows: {len(df)}")
print(f"Total engines: {df['engine_id'].nunique()}")


# ============================================================
# Get unique engines
# ============================================================

engines = df["engine_id"].unique()


print("\nEngine IDs:")
print(engines)


# ============================================================
# First split: train vs temporary
# ============================================================

train_engines, temp_engines = train_test_split(
    engines,
    test_size=VALIDATION_SIZE + TEST_SIZE,
    random_state=RANDOM_STATE,
)


# ============================================================
# Second split: validation vs test
# ============================================================

validation_engines, test_engines = train_test_split(
    temp_engines,
    test_size=TEST_SIZE / (VALIDATION_SIZE + TEST_SIZE),
    random_state=RANDOM_STATE,
)


# ============================================================
# Create datasets
# ============================================================

train_df = df[
    df["engine_id"].isin(train_engines)
].copy()

validation_df = df[
    df["engine_id"].isin(validation_engines)
].copy()

test_df = df[
    df["engine_id"].isin(test_engines)
].copy()


# ============================================================
# Sort datasets
# ============================================================

train_df = train_df.sort_values(
    ["engine_id", "cycle"]
)

validation_df = validation_df.sort_values(
    ["engine_id", "cycle"]
)

test_df = test_df.sort_values(
    ["engine_id", "cycle"]
)


# ============================================================
# Print split information
# ============================================================

print("\n--- SPLIT INFORMATION ---")

print(
    f"Training engines: "
    f"{len(train_engines)}"
)

print(
    f"Validation engines: "
    f"{len(validation_engines)}"
)

print(
    f"Test engines: "
    f"{len(test_engines)}"
)


print("\nRows:")

print(
    f"Training:   {len(train_df)}"
)

print(
    f"Validation: {len(validation_df)}"
)

print(
    f"Test:       {len(test_df)}"
)


# ============================================================
# Check for engine overlap
# ============================================================

train_set = set(train_engines)
validation_set = set(validation_engines)
test_set = set(test_engines)


print("\n--- ENGINE OVERLAP CHECK ---")

print(
    "Train ∩ Validation:",
    train_set & validation_set
)

print(
    "Train ∩ Test:",
    train_set & test_set
)

print(
    "Validation ∩ Test:",
    validation_set & test_set
)


# ============================================================
# RUL distribution
# ============================================================

print("\n--- RUL DISTRIBUTION ---")

print("\nTraining:")
print(train_df["RUL"].describe())

print("\nValidation:")
print(validation_df["RUL"].describe())

print("\nTest:")
print(test_df["RUL"].describe())


# ============================================================
# Save datasets
# ============================================================

train_path = OUTPUT_DIR / "train.csv"
validation_path = OUTPUT_DIR / "validation.csv"
test_path = OUTPUT_DIR / "test.csv"


train_df.to_csv(
    train_path,
    index=False
)

validation_df.to_csv(
    validation_path,
    index=False
)

test_df.to_csv(
    test_path,
    index=False
)


print("\n--- FILES SAVED ---")

print(train_path)
print(validation_path)
print(test_path)


print("\n" + "=" * 60)
print("DATA SPLITTING COMPLETE")
print("=" * 60)