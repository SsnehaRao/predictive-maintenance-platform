import pandas as pd

from sqlalchemy import text
from sqlalchemy.orm import Session

from fastapi import Depends
from app.database import get_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.predictor import get_health_status
from app.predictor import predict_rul
from app.predictor import FEATURE_COLUMNS
from app.schemas import PredictionResponse
from app.schemas import TelemetryRequest
from app.schemas import TelemetryResponse
from app.models import Telemetry
from app.models import Prediction
from app.feature_engineering import create_features
from app.simulation import get_next_telemetry


app = FastAPI(
    title="Predictive Maintenance Platform",
    description="AI-powered predictive maintenance backend",
    version="0.1.0",
)


# ============================================================
# CORS
# ============================================================

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Root endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Predictive Maintenance API is running"
    }


# ============================================================
# Health endpoint
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
# ============================================================
# Database test endpoint
# ============================================================

@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT current_database()")
    ).scalar_one()

    return {
        "database": result,
        "status": "connected",
    }

# ============================================================
# Telemetry endpoint
# ============================================================

@app.post(
    "/telemetry",
    response_model=TelemetryResponse,
)
def create_telemetry(
    request: TelemetryRequest,
    db: Session = Depends(get_db),
):
    telemetry = Telemetry(
        **request.model_dump()
    )

    db.add(telemetry)
    db.commit()

    return {
        "message": "Telemetry stored successfully",
        "engine_id": request.engine_id,
        "cycle": request.cycle,
    }
# ============================================================
# Latest telemetry endpoint
# ============================================================

@app.get("/telemetry/{engine_id}/latest")
def get_latest_telemetry(
    engine_id: int,
    db: Session = Depends(get_db),
):
    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.engine_id == engine_id)
        .order_by(Telemetry.cycle.desc())
        .first()
    )

    if not telemetry:
        return {
            "message": "No telemetry found",
            "engine_id": engine_id,
        }

    return {
        "id": telemetry.id,
        "engine_id": telemetry.engine_id,
        "cycle": telemetry.cycle,

        "setting_1": telemetry.setting_1,
        "setting_2": telemetry.setting_2,
        "setting_3": telemetry.setting_3,

        "sensor_2": telemetry.sensor_2,
        "sensor_3": telemetry.sensor_3,
        "sensor_4": telemetry.sensor_4,
        "sensor_6": telemetry.sensor_6,
        "sensor_7": telemetry.sensor_7,
        "sensor_8": telemetry.sensor_8,
        "sensor_9": telemetry.sensor_9,
        "sensor_11": telemetry.sensor_11,
        "sensor_12": telemetry.sensor_12,
        "sensor_13": telemetry.sensor_13,
        "sensor_14": telemetry.sensor_14,
        "sensor_15": telemetry.sensor_15,
        "sensor_17": telemetry.sensor_17,
        "sensor_20": telemetry.sensor_20,
        "sensor_21": telemetry.sensor_21,

        "recorded_at": telemetry.recorded_at,
    }

@app.get("/telemetry/{engine_id}/features")
def get_telemetry_features(
    engine_id: int,
    db: Session = Depends(get_db),
):
    telemetry_rows = (
        db.query(Telemetry)
        .filter(Telemetry.engine_id == engine_id)
        .order_by(Telemetry.cycle)
        .all()
    )

    if not telemetry_rows:
        return {
            "message": "No telemetry found",
            "engine_id": engine_id,
            "features": [],
        }

    data = [
        {
            column.name: getattr(row, column.name)
            for column in Telemetry.__table__.columns
        }
        for row in telemetry_rows
    ]

    df = pd.DataFrame(data)

    features_df = create_features(df)

    return {
        "engine_id": engine_id,
        "rows": len(features_df),
        "features": features_df.to_dict(
            orient="records"
        ),
    }
# ============================================================
# Prediction history endpoint
# ============================================================

@app.get("/predictions/{engine_id}")
def get_prediction_history(
    engine_id: int,
    db: Session = Depends(get_db),
):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.engine_id == engine_id)
        .order_by(Prediction.predicted_at.desc())
        .all()
    )

    return {
        "engine_id": engine_id,
        "count": len(predictions),
        "predictions": [
            {
                "id": prediction.id,
                "cycle": prediction.cycle,
                "predicted_rul": prediction.predicted_rul,
                "health_status": prediction.health_status,
                "model_name": prediction.model_name,
                "predicted_at": prediction.predicted_at,
            }
            for prediction in predictions
        ],
    }


# ============================================================
# Prediction endpoint
# ============================================================

@app.post(
    "/predict/{engine_id}",
    response_model=PredictionResponse,
)
def predict(
    engine_id: int,
    db: Session = Depends(get_db),
):
    telemetry_rows = (
        db.query(Telemetry)
        .filter(Telemetry.engine_id == engine_id)
        .order_by(Telemetry.cycle)
        .all()
    )

    if not telemetry_rows:
        return {
            "predicted_rul": 0,
            "health_status": "critical",
            "model": "random_forest_capped_rul",
        }

    data = [
        {
            column.name: getattr(row, column.name)
            for column in Telemetry.__table__.columns
        }
        for row in telemetry_rows
    ]

    df = pd.DataFrame(data)

    # Generate the same features used during training
    features_df = create_features(df)

    # Use the latest telemetry cycle
    latest_features = features_df.iloc[-1]

    # Select exactly the 64 features expected by the model
    features = {
        column: latest_features[column]
        for column in FEATURE_COLUMNS
    }

    # Generate prediction
    predicted_rul = predict_rul(features)

    # Convert RUL to health status
    health_status = get_health_status(
        predicted_rul
    )

    # Get latest cycle
    latest_cycle = int(
        latest_features["cycle"]
    )

    # Save prediction to PostgreSQL
    prediction = Prediction(
        engine_id=engine_id,
        cycle=latest_cycle,
        predicted_rul=predicted_rul,
        health_status=health_status,
        model_name="random_forest_capped_rul",
    )

    db.add(prediction)
    db.commit()

    return {
        "predicted_rul": predicted_rul,
        "health_status": health_status,
        "model": "random_forest_capped_rul",
    }

# ============================================================
# Latest prediction endpoint
# ============================================================

@app.get("/predictions/{engine_id}/latest")
def get_latest_prediction(
    engine_id: int,
    db: Session = Depends(get_db),
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.engine_id == engine_id)
        .order_by(Prediction.predicted_at.desc())
        .first()
    )

    if not prediction:
        return {
            "message": "No predictions found",
            "engine_id": engine_id,
        }

    return {
        "engine_id": prediction.engine_id,
        "cycle": prediction.cycle,
        "predicted_rul": prediction.predicted_rul,
        "health_status": prediction.health_status,
        "model_name": prediction.model_name,
        "predicted_at": prediction.predicted_at,
    }

# ============================================================
# Simulation endpoint
# ============================================================

@app.post("/simulate/{engine_id}")
def simulate_next_cycle(
    engine_id: int,
    db: Session = Depends(get_db),
):
    # Get the next real telemetry row
    row = get_next_telemetry(
        db,
        engine_id,
    )

    if row is None:
        return {
            "message": "No more telemetry cycles available",
            "engine_id": engine_id,
        }

    # Create telemetry record
    telemetry = Telemetry(
        engine_id=engine_id,
        cycle=int(row["cycle"]),

        setting_1=float(row["setting_1"]),
        setting_2=float(row["setting_2"]),
        setting_3=float(row["setting_3"]),

        sensor_2=float(row["sensor_2"]),
        sensor_3=float(row["sensor_3"]),
        sensor_4=float(row["sensor_4"]),
        sensor_6=float(row["sensor_6"]),
        sensor_7=float(row["sensor_7"]),
        sensor_8=float(row["sensor_8"]),
        sensor_9=float(row["sensor_9"]),
        sensor_11=float(row["sensor_11"]),
        sensor_12=float(row["sensor_12"]),
        sensor_13=float(row["sensor_13"]),
        sensor_14=float(row["sensor_14"]),
        sensor_15=float(row["sensor_15"]),
        sensor_17=float(row["sensor_17"]),
        sensor_20=float(row["sensor_20"]),
        sensor_21=float(row["sensor_21"]),
    )

    db.add(telemetry)
    db.commit()

    # Get all telemetry for this engine
    telemetry_rows = (
        db.query(Telemetry)
        .filter(Telemetry.engine_id == engine_id)
        .order_by(Telemetry.cycle)
        .all()
    )

    data = [
        {
            column.name: getattr(row, column.name)
            for column in Telemetry.__table__.columns
        }
        for row in telemetry_rows
    ]

    df = pd.DataFrame(data)

    # Generate model features
    features_df = create_features(df)

    # Use latest cycle
    latest_features = features_df.iloc[-1]

    features = {
        column: latest_features[column]
        for column in FEATURE_COLUMNS
    }

    # Predict RUL
    predicted_rul = predict_rul(features)

    health_status = get_health_status(
        predicted_rul
    )

    # Save prediction
    prediction = Prediction(
        engine_id=engine_id,
        cycle=int(row["cycle"]),
        predicted_rul=predicted_rul,
        health_status=health_status,
        model_name="random_forest_capped_rul",
    )

    db.add(prediction)
    db.commit()

    return {
        "engine_id": engine_id,
        "cycle": int(row["cycle"]),
        "predicted_rul": predicted_rul,
        "health_status": health_status,
        "model": "random_forest_capped_rul",
    }