import { useEffect, useState } from "react";
import toast, { Toaster } from "react-hot-toast";

import api from "../services/api";
import socket from "../services/socket";

import AircraftMap from "../components/AircraftMap";
import TelemetryChart from "../components/TelemetryChart";
import AircraftStats from "../components/AircraftStats";
import AircraftDetails from "../components/AircraftDetails";

function Dashboard() {
  const [telemetry, setTelemetry] = useState([]);
  const [selectedAircraft, setSelectedAircraft] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState("Connecting...");

  useEffect(() => {
    fetchTelemetry();

    socket.on("connect", () => {
      console.log("Connected to Socket.IO server");

      setConnectionStatus("Live");
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from Socket.IO server");

      setConnectionStatus("Disconnected");
    });

    socket.on("telemetry_update", (data) => {
      console.log("Realtime telemetry:", data);

      setTelemetry((prev) => [data, ...prev].slice(0, 50));

      if (
        data.fuel_level !== null &&
        data.fuel_level !== undefined &&
        data.fuel_level < 15
      ) {
        toast.error(
          `Low Fuel Warning - Aircraft ${data.aircraft_id}`
        );
      }

      if (
        data.engine_temperature !== null &&
        data.engine_temperature !== undefined &&
        data.engine_temperature > 100
      ) {
        toast.error(
          `High Engine Temperature - Aircraft ${data.aircraft_id}`
        );
      }
    });

    socket.on("aircraft_alert", (alert) => {
      console.log("Aircraft alert:", alert);

      toast.error(alert.message);
    });

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("telemetry_update");
      socket.off("aircraft_alert");
    };
  }, []);

  const fetchTelemetry = async () => {
    try {
      const response = await api.get("/telemetry/history/1");

      setTelemetry(response.data.telemetry || []);
    } catch (error) {
      console.error("Failed to fetch telemetry:", error);

      toast.error("Failed to load telemetry data");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Toaster position="top-right" />

      {/* Navbar */}
      <div className="border-b border-slate-800 bg-slate-900/70 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-wide">
              Aircraft Telemetry Dashboard
            </h1>

            <p className="text-slate-400 text-sm mt-1">
              Realtime Aircraft Monitoring System
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div
              className={`
                h-3 w-3 rounded-full
                ${
                  connectionStatus === "Live"
                    ? "bg-green-400"
                    : "bg-red-500"
                }
              `}
            />

            <span className="text-sm text-slate-300">
              {connectionStatus}
            </span>
          </div>
        </div>
      </div>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto p-6">
        {/* Stats Section */}
        <AircraftStats telemetry={telemetry} />

        {/* Map + Details */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mt-8">
          {/* Map */}
          <div className="xl:col-span-2">
            <AircraftMap
              telemetry={telemetry}
              setSelectedAircraft={setSelectedAircraft}
            />
          </div>

          {/* Aircraft Details */}
          <div>
            <AircraftDetails aircraft={selectedAircraft} />
          </div>
        </div>

        {/* Charts */}
        <div className="grid md:grid-cols-2 gap-6 mt-8">
          <TelemetryChart
            data={telemetry}
            dataKey="altitude"
            title="Altitude Chart"
          />

          <TelemetryChart
            data={telemetry}
            dataKey="speed"
            title="Speed Chart"
          />

          <TelemetryChart
            data={telemetry}
            dataKey="fuel_level"
            title="Fuel Level Chart"
          />

          <TelemetryChart
            data={telemetry}
            dataKey="engine_temperature"
            title="Engine Temperature Chart"
          />
        </div>

        {/* Live Telemetry Feed */}
        <div className="mt-10">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-2xl font-semibold">
              Live Telemetry Feed
            </h2>

            <span className="text-sm text-slate-400">
              Showing latest {telemetry.length} records
            </span>
          </div>

          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-5">
            {telemetry.map((item) => (
          <div
            key={item.id}
            className="bg-slate-900 border border-slate-700 rounded-xl p-4"
          >

            <div className="flex items-center justify-between mb-3">

              <h2 className="text-lg font-bold text-cyan-400">
                Aircraft #{item.aircraft_id}
              </h2>

              <div
                className={`
                  h-3 w-3 rounded-full
                  ${
                    item.engine_temperature > 100
                      ? "bg-red-500"
                      : item.fuel_level < 15
                      ? "bg-yellow-400"
                      : "bg-green-400"
                  }
                `}
              />

            </div>

            <p>Altitude: {item.altitude} ft</p>
            <p>Speed: {item.speed} km/h</p>
            <p>Heading: {item.heading}°</p>
            <p>Fuel Level: {item.fuel_level ?? "N/A"}%</p>
            <p>Engine Temp: {item.engine_temperature ?? "N/A"}°C</p>
            <p>Latitude: {item.latitude}</p>
            <p>Longitude: {item.longitude}</p>

          </div>
        ))}
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-cyan-400">
                    Aircraft #{item.aircraft_id}
                  </h3>

                  <span className="text-xs text-slate-400">
                    LIVE
                  </span>
                </div>

                <div className="space-y-2 text-sm">
                  <p>
                    <span className="text-slate-400">
                      Altitude:
                    </span>{" "}
                    {item.altitude} ft
                  </p>

                  <p>
                    <span className="text-slate-400">
                      Speed:
                    </span>{" "}
                    {item.speed} km/h
                  </p>

                  <p>
                    <span className="text-slate-400">
                      Heading:
                    </span>{" "}
                    {item.heading}°
                  </p>

                  <p>
                    <span className="text-slate-400">
                      Fuel Level:
                    </span>{" "}
                    {item.fuel_level ?? "N/A"}%
                  </p>

                  <p>
                    <span className="text-slate-400">
                      Engine Temp:
                    </span>{" "}
                    {item.engine_temperature ?? "N/A"}°C
                  </p>

                  <p>
                    <span className="text-slate-400">
                      Latitude:
                    </span>{" "}
                    {item.latitude}
                  </p>

                  <p>
                    <span className="text-slate-400">
                      Longitude:
                    </span>{" "}
                    {item.longitude}
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-700">
                  <p className="text-xs text-slate-500">
                    {item.timestamp}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {telemetry.length === 0 && (
            <div className="text-center py-20 text-slate-500">
              No telemetry data available
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;