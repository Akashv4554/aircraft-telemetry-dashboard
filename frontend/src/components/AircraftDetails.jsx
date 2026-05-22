function AircraftDetails({ aircraft }) {
  if (!aircraft) {
    return (
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 h-full">
        <p className="text-slate-400">
          Select an aircraft from map or feed
        </p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6">
      
      <h2 className="text-2xl font-bold text-cyan-400 mb-6">
        Aircraft #{aircraft.aircraft_id}
      </h2>

      <div className="space-y-4 text-sm">
        
        <div className="flex justify-between">
          <span className="text-slate-400">
            Altitude
          </span>

          <span>{aircraft.altitude} ft</span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">
            Speed
          </span>

          <span>{aircraft.speed} km/h</span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">
            Heading
          </span>

          <span>{aircraft.heading}°</span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">
            Fuel
          </span>

          <span>{aircraft.fuel_level ?? "N/A"}%</span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">
            Engine Temp
          </span>

          <span>
            {aircraft.engine_temperature ?? "N/A"}°C
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">
            Latitude
          </span>

          <span>{aircraft.latitude}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-slate-400">
            Longitude
          </span>

          <span>{aircraft.longitude}</span>
        </div>

      </div>
    </div>
  );
}

export default AircraftDetails;