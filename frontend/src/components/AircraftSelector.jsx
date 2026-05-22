function AircraftSelector({
  aircraft,
  selectedAircraft,
  setSelectedAircraft,
}) {
  return (
    <div className="mb-6">

      <label className="block mb-2 text-slate-400">
        Select Aircraft
      </label>

      <select
        value={selectedAircraft}
        onChange={(e) =>
          setSelectedAircraft(Number(e.target.value))
        }
        className="
          bg-slate-900
          border border-slate-700
          rounded-xl
          px-4 py-3
          text-white
          w-full md:w-[300px]
        "
      >

        {aircraft.length > 0 ? (
          aircraft.map((item) => (
            <option
              key={item.id}
              value={item.id}
            >
              {item.callsign} — {item.aircraft_type}
            </option>
          ))
        ) : (
          <option>No Aircraft Available</option>
        )}

      </select>
    </div>
  );
}

export default AircraftSelector;