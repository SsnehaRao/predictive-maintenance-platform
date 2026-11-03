const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function checkBackendHealth() {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend request failed");
  }

  return response.json();
}


export async function getLatestPrediction(engineId: number) {
  const response = await fetch(
    `${API_URL}/predictions/${engineId}/latest`
  );

  if (!response.ok) {
    throw new Error("Prediction request failed");
  }

  return response.json();
}


export async function getPredictionHistory(engineId: number) {
  const response = await fetch(
    `${API_URL}/predictions/${engineId}`
  );

  if (!response.ok) {
    throw new Error("Prediction history request failed");
  }

  return response.json();
}
export async function simulateNextCycle(engineId: number) {
  const response = await fetch(
    `${API_URL}/simulate/${engineId}`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error("Simulation request failed");
  }

  return response.json();
}

export async function getLatestTelemetry(engineId: number) {
  const response = await fetch(
    `${API_URL}/telemetry/${engineId}/latest`
  );

  if (!response.ok) {
    throw new Error("Telemetry request failed");
  }

  return response.json();
}