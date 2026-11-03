from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Engine(Base):
    __tablename__ = "engines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    engine_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    engine_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("engines.engine_id"),
        nullable=False,
    )

    cycle: Mapped[int] = mapped_column(Integer, nullable=False)

    setting_1: Mapped[float | None] = mapped_column(Float)
    setting_2: Mapped[float | None] = mapped_column(Float)
    setting_3: Mapped[float | None] = mapped_column(Float)

    sensor_2: Mapped[float | None] = mapped_column(Float)
    sensor_3: Mapped[float | None] = mapped_column(Float)
    sensor_4: Mapped[float | None] = mapped_column(Float)
    sensor_6: Mapped[float | None] = mapped_column(Float)
    sensor_7: Mapped[float | None] = mapped_column(Float)
    sensor_8: Mapped[float | None] = mapped_column(Float)
    sensor_9: Mapped[float | None] = mapped_column(Float)
    sensor_11: Mapped[float | None] = mapped_column(Float)
    sensor_12: Mapped[float | None] = mapped_column(Float)
    sensor_13: Mapped[float | None] = mapped_column(Float)
    sensor_14: Mapped[float | None] = mapped_column(Float)
    sensor_15: Mapped[float | None] = mapped_column(Float)
    sensor_17: Mapped[float | None] = mapped_column(Float)
    sensor_20: Mapped[float | None] = mapped_column(Float)
    sensor_21: Mapped[float | None] = mapped_column(Float)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    __table_args__ = (
        UniqueConstraint(
            "engine_id",
            "cycle",
            name="telemetry_engine_id_cycle_key",
        ),
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    engine_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("engines.engine_id"),
        nullable=False,
    )

    cycle: Mapped[int] = mapped_column(Integer, nullable=False)

    predicted_rul: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    health_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    predicted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )