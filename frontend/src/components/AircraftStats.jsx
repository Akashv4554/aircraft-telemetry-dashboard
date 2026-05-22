function AircraftStats({ telemetry }) {
  const latest = telemetry[0];

  const lowFuelCount = telemetry.filter(
    (t) => t.fuel_level !== null && t.fuel_level < 15
  ).length;

  const highTempCount = telemetry.filter(
    (t) =>
      t.engine_temperature !== null &&
      t.engine_temperature > 100
  ).length;

  return (
    <div className="grid md:grid-cols-4 gap-5 mt-6">
      
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-5">
        <p className="text-slate-400 text-sm">
          Total Telemetry
        </p>

        <h2 className="text-3xl font-bold mt-2">
          {telemetry.length}
        </h2>
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-5">
        <p className="text-slate-400 text-sm">
          Current Altitude
        </p>

        <h2 className="text-3xl font-bold mt-2 text-cyan-400">
          {latest?.altitude ?? 0} ft
        </h2>
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-5">
        <p className="text-slate-400 text-sm">
          Low Fuel Alerts
        </p>

        <h2 className="text-3xl font-bold mt-2 text-yellow-400">
          {lowFuelCount}
        </h2>
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-5">
        <p className="text-slate-400 text-sm">
          Engine Alerts
        </p>

        <h2 className="text-3xl font-bold mt-2 text-red-400">
          {highTempCount}
        </h2>
      </div>

    </div>
  );
}

export default AircraftStats;