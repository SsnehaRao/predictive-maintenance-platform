"use client";

import { useEffect, useMemo, useState } from "react";
import {
  checkBackendHealth,
  getLatestPrediction,
  getPredictionHistory,
  getLatestTelemetry,
  simulateNextCycle,
} from "@/lib/api";

type Prediction = {
  id: number;
  cycle: number;
  predicted_rul: number;
  health_status: string;
  model_name: string;
  predicted_at: string;
};

type Telemetry = {
  cycle: number;
  setting_1: number;
  setting_2: number;
  setting_3: number;
  sensor_2: number;
  sensor_3: number;
  sensor_4: number;
  sensor_6: number;
  sensor_7: number;
  sensor_8: number;
  sensor_9: number;
  sensor_11: number;
  sensor_12: number;
  sensor_13: number;
  sensor_14: number;
  sensor_15: number;
  sensor_17: number;
  sensor_20: number;
  sensor_21: number;
};

export default function Home() {
  const [backendStatus, setBackendStatus] =
    useState("Checking backend...");

  const [latestPrediction, setLatestPrediction] =
    useState<Prediction | null>(null);

  const [predictions, setPredictions] =
    useState<Prediction[]>([]);

  const [latestTelemetry, setLatestTelemetry] =
    useState<Telemetry | null>(null);

  const [error, setError] = useState("");
const [isSimulating, setIsSimulating] = useState(false);

  const engineId = 1;
async function handleSimulate() {
  try {
    setIsSimulating(true);
    setError("");

    await simulateNextCycle(engineId);

    const latest = await getLatestPrediction(engineId);
    setLatestPrediction(latest);

    const telemetry = await getLatestTelemetry(engineId);
    setLatestTelemetry(telemetry);

    const history = await getPredictionHistory(engineId);

    setPredictions(history.predictions);
  } catch (err) {
    console.error(err);
    setError("Could not simulate next cycle");
  } finally {
    setIsSimulating(false);
  }
}

  useEffect(() => {
    async function loadDashboard() {
      try {
        const health = await checkBackendHealth();

        setBackendStatus(health.status);

        const latest = await getLatestPrediction(engineId);
        setLatestPrediction(latest);

        const telemetry = await getLatestTelemetry(engineId);
        setLatestTelemetry(telemetry);

        const history = await getPredictionHistory(engineId);

        setPredictions(history.predictions);
      } catch (err) {
        console.error(err);
        setError("Could not load dashboard data");
      }
    }

    loadDashboard();
  }, []);

  const chartData = useMemo(() => {
    const latestByCycle = new Map<number, Prediction>();

    predictions.forEach((prediction) => {
      latestByCycle.set(prediction.cycle, prediction);
    });

    return Array.from(latestByCycle.values()).sort(
      (a, b) => a.cycle - b.cycle
    );
  }, [predictions]);

  const chartWidth = 900;
  const chartHeight = 280;
  const padding = 45;

  const maxRul = 125;

  const points = chartData
    .map((prediction, index) => {
      const x =
        chartData.length === 1
          ? chartWidth / 2
          : padding +
            (index / (chartData.length - 1)) *
              (chartWidth - padding * 2);

      const y =
        chartHeight -
        padding -
        (prediction.predicted_rul / maxRul) *
          (chartHeight - padding * 2);

      return `${x},${y}`;
    })
    .join(" ");

  return (
    <main className="min-h-screen bg-slate-100 px-6 py-10">
      <div className="mx-auto max-w-7xl">

        {/* Header */}
        <header>
          <h1 className="text-4xl font-bold text-slate-900">
            Predictive Maintenance Platform
          </h1>

          <p className="mt-2 text-lg text-slate-600">
            AI-powered engine health monitoring
          </p>
        </header>


        {/* Error */}
        {error && (
          <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}


        {/* System Status */}
        <section className="mt-8 rounded-2xl bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-semibold text-slate-900">
            System Status
          </h2>

          <p className="mt-4 text-lg text-green-600">
            ● Backend: {backendStatus}
          </p>
        </section>


        {/* Engine */}
        <section className="mt-10">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 className="text-3xl font-bold text-slate-900">
                Engine {engineId}
              </h2>

      {latestPrediction && (
        <p className="mt-2 text-sm text-slate-500">
          Last updated:{" "}
          {new Date(
            latestPrediction.predicted_at
          ).toLocaleString()}
        </p>
      )}
    </div>

    <button
      onClick={handleSimulate}
      disabled={isSimulating}
      className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {isSimulating
        ? "Simulating..."
        : "▶ Simulate Next Cycle"}
    </button>
  </div>


          {/* Current Prediction Cards */}
          <div className="mt-5 grid gap-6 md:grid-cols-3">

            {/* RUL */}
            <div className="rounded-2xl bg-white p-7 shadow-sm">
              <p className="text-sm font-medium text-slate-500">
                Predicted Remaining Useful Life
              </p>

              <p className="mt-4 text-4xl font-bold text-slate-900">
                {latestPrediction
                  ? latestPrediction.predicted_rul.toFixed(2)
                  : "--"}
              </p>

              <p className="mt-1 text-slate-500">
                cycles
              </p>
            </div>


            {/* Health */}
            <div className="rounded-2xl bg-white p-7 shadow-sm">
              <p className="text-sm font-medium text-slate-500">
                Health Status
              </p>

              <p
                className={`mt-4 text-4xl font-bold ${
                  latestPrediction?.health_status === "healthy"
                    ? "text-green-600"
                    : latestPrediction?.health_status ===
                        "warning"
                    ? "text-yellow-600"
                    : "text-red-600"
                }`}
              >
                {latestPrediction
                  ? latestPrediction.health_status
                  : "--"}
              </p>
            </div>


            {/* Model */}
            <div className="rounded-2xl bg-white p-7 shadow-sm">
              <p className="text-sm font-medium text-slate-500">
                ML Model
              </p>

              <p className="mt-5 break-words text-xl font-bold text-slate-900">
                {latestPrediction
                  ? latestPrediction.model_name
                  : "--"}
              </p>
            </div>
          </div>
        </section>
        
                {/* Latest Telemetry */}
        <section className="mt-10 rounded-2xl bg-white p-8 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-semibold text-slate-900">
                Latest Telemetry
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Most recent sensor readings from the engine
              </p>
            </div>

            <div className="text-sm text-slate-500">
              {latestTelemetry
                ? `Cycle ${latestTelemetry.cycle}`
                : "No data"}
            </div>
          </div>

          {latestTelemetry ? (
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-lg bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Sensor 2</p>
                <p className="mt-2 text-xl font-semibold text-slate-900">
                  {latestTelemetry.sensor_2.toFixed(2)}
                </p>
              </div>

              <div className="rounded-lg bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Sensor 4</p>
                <p className="mt-2 text-xl font-semibold text-slate-900">
                  {latestTelemetry.sensor_4.toFixed(2)}
                </p>
              </div>

              <div className="rounded-lg bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Sensor 15</p>
                <p className="mt-2 text-xl font-semibold text-slate-900">
                  {latestTelemetry.sensor_15.toFixed(4)}
                </p>
              </div>

              <div className="rounded-lg bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Sensor 21</p>
                <p className="mt-2 text-xl font-semibold text-slate-900">
                  {latestTelemetry.sensor_21.toFixed(4)}
                </p>
              </div>
            </div>
          ) : (
            <p className="mt-6 text-slate-500">
              No telemetry data available.
            </p>
          )}
        </section>


        {/* RUL Trend */}
        <section className="mt-10 rounded-2xl bg-white p-8 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-semibold text-slate-900">
                RUL Trend
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Predicted remaining useful life by engine cycle
              </p>
            </div>

            <div className="text-sm text-slate-500">
              {chartData.length} cycles
            </div>
          </div>


          {chartData.length > 0 ? (
            <div className="mt-6 overflow-x-auto">
              <svg
                viewBox={`0 0 ${chartWidth} ${chartHeight}`}
                className="h-auto min-w-[700px] w-full"
              >
                {/* Horizontal grid lines */}
                {[0, 25, 50, 75, 100, 125].map(
                  (value) => {
                    const y =
                      chartHeight -
                      padding -
                      (value / maxRul) *
                        (chartHeight - padding * 2);

                    return (
                      <g key={value}>
                        <line
                          x1={padding}
                          x2={chartWidth - padding}
                          y1={y}
                          y2={y}
                          stroke="#e2e8f0"
                        />

                        <text
                          x="10"
                          y={y + 5}
                          fontSize="12"
                          fill="#64748b"
                        >
                          {value}
                        </text>
                      </g>
                    );
                  }
                )}


                {/* Trend line */}
                {chartData.length > 1 && (
                  <polyline
                    fill="none"
                    stroke="#2563eb"
                    strokeWidth="4"
                    points={points}
                  />
                )}


                {/* Data points */}
                {chartData.map(
                  (prediction, index) => {
                    const x =
                      chartData.length === 1
                        ? chartWidth / 2
                        : padding +
                          (index /
                            (chartData.length - 1)) *
                            (chartWidth -
                              padding * 2);

                    const y =
                      chartHeight -
                      padding -
                      (prediction.predicted_rul /
                        maxRul) *
                        (chartHeight -
                          padding * 2);

                    return (
                      <g key={prediction.cycle}>
                        <circle
                          cx={x}
                          cy={y}
                          r="6"
                          fill="#2563eb"
                        />

                        {(
                          index === 0 ||
                          prediction.cycle % 10 === 0 ||
                          index === chartData.length - 1
                        ) && (
                        <text
                        x={x}
                        y={chartHeight - 15}
                        textAnchor="middle"
                        fontSize="12"
                        fill="#475569"
                        >
                          {prediction.cycle}
                          </text>
                        )}
                      </g>
                    );
                  }
                )}
              </svg>
            </div>
          ) : (
            <p className="mt-6 text-slate-500">
              No prediction history available.
            </p>
          )}
        </section>


        {/* Prediction History */}
        <section className="mt-10 rounded-2xl bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-semibold text-slate-900">
            Prediction History
          </h2>

          <div className="mt-6 overflow-x-auto">
            <table className="w-full min-w-[700px] text-left">
              <thead>
                <tr className="border-b border-slate-200 text-sm text-slate-500">
                  <th className="px-4 py-3">
                    Cycle
                  </th>

                  <th className="px-4 py-3">
                    Predicted RUL
                  </th>

                  <th className="px-4 py-3">
                    Health
                  </th>

                  <th className="px-4 py-3">
                    Model
                  </th>

                  <th className="px-4 py-3">
                    Predicted At
                  </th>
                </tr>
              </thead>

              <tbody>
                {predictions.map(
                  (prediction) => (
                    <tr
                      key={prediction.id}
                      className="border-b border-slate-100"
                    >
                      <td className="px-4 py-4 font-medium">
                        {prediction.cycle}
                      </td>

                      <td className="px-4 py-4">
                        {prediction.predicted_rul.toFixed(2)}
                        {" "}
                        cycles
                      </td>

                      <td
                        className={`px-4 py-4 font-semibold ${
                          prediction.health_status ===
                          "healthy"
                            ? "text-green-600"
                            : prediction.health_status ===
                                "warning"
                            ? "text-yellow-600"
                            : "text-red-600"
                        }`}
                      >
                        {prediction.health_status}
                      </td>

                      <td className="px-4 py-4 text-sm">
                        {prediction.model_name}
                      </td>

                      <td className="px-4 py-4 text-sm text-slate-500">
                        {new Date(
                          prediction.predicted_at
                        ).toLocaleString()}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>
  );
}