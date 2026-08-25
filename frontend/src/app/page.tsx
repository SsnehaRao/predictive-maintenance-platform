"use client";

import { useEffect, useState } from "react";
import { checkBackendHealth } from "@/lib/api";

export default function Home() {
  const [status, setStatus] = useState("Checking backend...");
  const [error, setError] = useState("");

  useEffect(() => {
    checkBackendHealth()
      .then((data) => {
        setStatus(data.status);
      })
      .catch(() => {
        setError("Could not connect to backend");
      });
  }, []);

  return (
    <main className="min-h-screen p-10">
      <h1 className="text-3xl font-bold">
        Predictive Maintenance Platform
      </h1>

      <div className="mt-8">
        <h2 className="text-xl font-semibold">
          Backend Status
        </h2>

        {error ? (
          <p className="mt-2 text-red-600">
            {error}
          </p>
        ) : (
          <p className="mt-2 text-green-600">
            {status}
          </p>
        )}
      </div>
    </main>
  );
}