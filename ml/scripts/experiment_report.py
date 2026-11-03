import pandas as pd


results = [
    {
        "experiment": "Random Forest Baseline",
        "target": "Raw RUL",
        "MAE": 23.47,
        "RMSE": 32.13,
        "R2": 0.7588,
    },
    {
        "experiment": "Random Forest Sensor Only",
        "target": "Raw RUL",
        "MAE": 25.34,
        "RMSE": 36.79,
        "R2": 0.6838,
    },
    {
        "experiment": "HistGradientBoosting",
        "target": "Raw RUL",
        "MAE": 24.18,
        "RMSE": 32.72,
        "R2": 0.7499,
    },
    {
        "experiment": "Random Forest Capped",
        "target": "RUL capped at 125",
        "MAE": 10.63,
        "RMSE": 15.55,
        "R2": 0.8609,
    },
]


df = pd.DataFrame(results)


print("=" * 70)
print("MODEL EXPERIMENT REPORT")
print("=" * 70)

print()

print(
    df.to_string(index=False)
)


print("\nBest capped-target MAE:")

print(
    df[df["target"] == "RUL capped at 125"]
    .sort_values("MAE")
    .iloc[0]["MAE"]
)


print("\n" + "=" * 70)
print("EXPERIMENT REPORT COMPLETE")
print("=" * 70)