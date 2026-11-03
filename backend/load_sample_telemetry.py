import pandas as pd

from app.database import SessionLocal
from app.models import Engine, Telemetry


DATA_PATH = (
    r"E:\predictive-maintenance-data\processed\fd001"
    r"\train_fd001_processed.csv"
)

ENGINE_ID = 1

# Load more real engine cycles
START_CYCLE = 1
END_CYCLE = 50


def main():
    print("=" * 60)
    print("LOADING REAL FD001 TELEMETRY")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    sample = df[
        (df["engine_id"] == ENGINE_ID)
        & (df["cycle"].between(START_CYCLE, END_CYCLE))
    ].copy()

    print(f"\nCycles requested: {START_CYCLE} - {END_CYCLE}")
    print(f"Rows found in dataset: {len(sample)}")

    if sample.empty:
        raise ValueError("No telemetry rows found.")

    db = SessionLocal()

    try:
        # ----------------------------------------------------
        # Make sure engine exists
        # ----------------------------------------------------

        engine = (
            db.query(Engine)
            .filter(
                Engine.engine_id == ENGINE_ID
            )
            .first()
        )

        if not engine:
            engine = Engine(
                engine_id=ENGINE_ID
            )

            db.add(engine)
            db.commit()

            print(
                f"\nCreated Engine {ENGINE_ID}"
            )

        else:
            print(
                f"\nEngine {ENGINE_ID} already exists"
            )

        # ----------------------------------------------------
        # Load telemetry without deleting existing rows
        # ----------------------------------------------------

        added = 0
        skipped = 0

        for _, row in sample.iterrows():

            cycle = int(row["cycle"])

            existing = (
                db.query(Telemetry)
                .filter(
                    Telemetry.engine_id == ENGINE_ID,
                    Telemetry.cycle == cycle,
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            telemetry = Telemetry(
                engine_id=ENGINE_ID,
                cycle=cycle,

                setting_1=float(
                    row["setting_1"]
                ),
                setting_2=float(
                    row["setting_2"]
                ),
                setting_3=float(
                    row["setting_3"]
                ),

                sensor_2=float(
                    row["sensor_2"]
                ),
                sensor_3=float(
                    row["sensor_3"]
                ),
                sensor_4=float(
                    row["sensor_4"]
                ),
                sensor_6=float(
                    row["sensor_6"]
                ),
                sensor_7=float(
                    row["sensor_7"]
                ),
                sensor_8=float(
                    row["sensor_8"]
                ),
                sensor_9=float(
                    row["sensor_9"]
                ),
                sensor_11=float(
                    row["sensor_11"]
                ),
                sensor_12=float(
                    row["sensor_12"]
                ),
                sensor_13=float(
                    row["sensor_13"]
                ),
                sensor_14=float(
                    row["sensor_14"]
                ),
                sensor_15=float(
                    row["sensor_15"]
                ),
                sensor_17=float(
                    row["sensor_17"]
                ),
                sensor_20=float(
                    row["sensor_20"]
                ),
                sensor_21=float(
                    row["sensor_21"]
                ),
            )

            db.add(telemetry)
            added += 1

        db.commit()

        # ----------------------------------------------------
        # Show result
        # ----------------------------------------------------

        print(
            f"\nNew telemetry rows added: {added}"
        )

        print(
            f"Existing rows skipped: {skipped}"
        )

        total = (
            db.query(Telemetry)
            .filter(
                Telemetry.engine_id == ENGINE_ID
            )
            .count()
        )

        print(
            f"Total Engine {ENGINE_ID} telemetry rows: {total}"
        )

        print("\nLatest telemetry:")

        latest_rows = (
            db.query(Telemetry)
            .filter(
                Telemetry.engine_id == ENGINE_ID
            )
            .order_by(
                Telemetry.cycle.desc()
            )
            .limit(5)
            .all()
        )

        for row in reversed(latest_rows):
            print(
                f"Cycle {row.cycle}: "
                f"sensor_2={row.sensor_2}, "
                f"sensor_4={row.sensor_4}, "
                f"sensor_15={row.sensor_15}"
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

    print("\n" + "=" * 60)
    print("TELEMETRY LOAD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()