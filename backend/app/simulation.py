from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.models import Telemetry


DATA_PATH = Path(
    r"E:\predictive-maintenance-data\processed\fd001\train_fd001_processed.csv"
)


def get_next_telemetry(
    db: Session,
    engine_id: int,
):
    """
    Get the next real telemetry cycle from the NASA FD001 dataset.
    """

    latest = (
        db.query(Telemetry)
        .filter(Telemetry.engine_id == engine_id)
        .order_by(Telemetry.cycle.desc())
        .first()
    )

    if latest:
        next_cycle = latest.cycle + 1
    else:
        next_cycle = 1

    df = pd.read_csv(DATA_PATH)

    row = df[
        (df["engine_id"] == engine_id)
        & (df["cycle"] == next_cycle)
    ]

    if row.empty:
        return None

    return row.iloc[0].to_dict()