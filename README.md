# Predictive Maintenance Platform

An AI-powered full-stack application for monitoring engine health and predicting Remaining Useful Life (RUL) using NASA C-MAPSS telemetry data.

## Project Overview

The Predictive Maintenance Platform uses machine learning to estimate the remaining useful life of an aircraft engine based on historical sensor readings.

The application includes:

* NASA C-MAPSS FD001 telemetry data
* Data preprocessing and feature engineering
* Random Forest machine learning model
* FastAPI backend
* PostgreSQL database
* Next.js frontend dashboard
* Engine-cycle simulation
* RUL prediction and health-status classification
* Prediction history and trend visualization

## System Architecture

```text
NASA C-MAPSS FD001 Dataset
            |
            v
Data Processing and Feature Engineering
            |
            v
Random Forest Model
            |
            v
FastAPI Backend
            |
            v
PostgreSQL Database
            |
            v
Next.js Dashboard
            |
            v
Telemetry, RUL Predictions, and Health Status
```

## Technologies Used

| Component            | Technology                 |
| -------------------- | -------------------------- |
| Programming Language | Python                     |
| Machine Learning     | Scikit-learn Random Forest |
| Backend              | FastAPI                    |
| Database             | PostgreSQL                 |
| Frontend             | Next.js, React, TypeScript |
| Styling              | Tailwind CSS               |
| Dataset              | NASA C-MAPSS FD001         |
| API Server           | Uvicorn                    |

## Main Features

### 1. Telemetry Management

The system stores engine telemetry, including operating settings and sensor readings, in PostgreSQL.

### 2. Remaining Useful Life Prediction

The Random Forest model predicts the estimated number of remaining operating cycles for an engine.

### 3. Engine Health Classification

The predicted RUL is used to classify engine health as:

* Healthy
* Warning
* Critical

### 4. Engine-Cycle Simulation

The application loads the next available telemetry cycle and generates a new prediction.

### 5. Dashboard Visualization

The Next.js dashboard displays:

* Backend status
* Predicted RUL
* Engine health status
* Machine learning model name
* Latest telemetry readings
* RUL trend
* Prediction history
* Last-updated timestamp

## Project Structure

```text
predictive-maintenance-platform/
|
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── predictor.py
│   │   ├── feature_engineering.py
│   │   └── simulation.py
│   ├── load_sample_telemetry.py
│   └── generate_predictions.py
|
├── frontend/
│   ├── src/
│   │   └── app/
│   │       └── page.tsx
│   ├── src/lib/
│   │   └── api.ts
│   └── package.json
|
├── models/
│   └── random_forest_capped_rul.joblib
|
├── README.md
└── .gitignore
```

## Running the Project

### Backend

Open Command Prompt and navigate to the backend folder:

```cmd
cd C:\Users\sneha\Documents\predictive-maintenance-platform\backend
```

Activate the virtual environment:

```cmd
..\.venv\Scripts\activate
```

Start the FastAPI server:

```cmd
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Open another Command Prompt window and navigate to the frontend folder:

```cmd
cd C:\Users\sneha\Documents\predictive-maintenance-platform\frontend
```

Start the Next.js development server:

```cmd
npm run dev
```

The dashboard will be available at:

```text
http://localhost:3000
```

## Application Workflow

1. Engine telemetry is loaded into PostgreSQL.
2. The backend retrieves telemetry for an engine.
3. Feature engineering prepares the model input.
4. The Random Forest model predicts RUL.
5. The backend classifies engine health.
6. The prediction is stored in PostgreSQL.
7. The frontend retrieves and displays the results.
8. The simulation endpoint advances to the next engine cycle.

## Future Improvements

* Automated backend testing
* Improved error handling and validation
* Automated prediction cleanup and retention
* Docker deployment
* Cloud deployment
* Authentication
* Support for multiple engines
* Model monitoring and retraining
* More advanced machine learning models

## Project Status

The core full-stack MVP is implemented and working.

The application successfully connects telemetry data, machine learning predictions, database storage, backend APIs, and frontend visualization.
