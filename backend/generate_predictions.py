import pandas as pd

from app.database import SessionLocal
from app.models import Telemetry, Prediction
from app.feature_engineering import create_features
from app.predictor import predict_rul, get_health_status, FEATURE_COLUMNS


ENGINE_ID = 1


def main():
    print("=" * 60)
    print("GENERATING PREDICTION HISTORY")
    print("=" * 60)

    db = SessionLocal()

    try:
        # ----------------------------------------------------
        # Get telemetry
        # ----------------------------------------------------

        telemetry_rows = (
            db.query(Telemetry)
            .filter(
                Telemetry.engine_id == ENGINE_ID
            )
            .order_by(Telemetry.cycle)
            .all()
        )

        if not telemetry_rows:
            raise ValueError(
                f"No telemetry found for Engine {ENGINE_ID}"
            )

        print(
            f"\nTelemetry rows found: "
            f"{len(telemetry_rows)}"
        )

        # ----------------------------------------------------
        # Convert database rows to DataFrame
        # ----------------------------------------------------

        data = [
            {
                column.name: getattr(
                    row,
                    column.name
                )
                for column in Telemetry.__table__.columns
            }
            for row in telemetry_rows
        ]

        df = pd.DataFrame(data)

        # ----------------------------------------------------
        # Generate model features
        # ----------------------------------------------------

        features_df = create_features(df)

        print(
            f"Feature rows generated: "
            f"{len(features_df)}"
        )

        # ----------------------------------------------------
        # Generate prediction for each cycle
        # ----------------------------------------------------

        added = 0
        skipped = 0

        for _, row in features_df.iterrows():

            cycle = int(row["cycle"])

            # Check if prediction already exists
            existing = (
                db.query(Prediction)
                .filter(
                    Prediction.engine_id == ENGINE_ID,
                    Prediction.cycle == cycle,
                )
                .first()
            )

            if existing:
                skipped += 1
                continue

            # Select exactly the features expected
            features = {
                column: row[column]
                for column in FEATURE_COLUMNS
            }

            # Generate RUL
            predicted_rul = predict_rul(
                features
            )

            # Determine health
            health_status = get_health_status(
                predicted_rul
            )

            # Save prediction
            prediction = Prediction(
                engine_id=ENGINE_ID,
                cycle=cycle,
                predicted_rul=predicted_rul,
                health_status=health_status,
                model_name="random_forest_capped_rul",
            )

            db.add(prediction)

            added += 1

            print(
                f"Cycle {cycle:3d} → "
                f"RUL {predicted_rul:6.2f} → "
                f"{health_status}"
            )

        db.commit()

        print("\n" + "-" * 60)

        print(
            f"New predictions added: {added}"
        )

        print(
            f"Existing predictions skipped: {skipped}"
        )

        total = (
            db.query(Prediction)
            .filter(
                Prediction.engine_id == ENGINE_ID
            )
            .count()
        )

        print(
            f"Total predictions: {total}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

    print("\n" + "=" * 60)
    print("PREDICTION HISTORY COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()