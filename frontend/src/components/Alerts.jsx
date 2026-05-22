function Navbar({ connectionStatus, aircraftCount }) {
  return (
    <div className="border-b border-slate-800 bg-slate-900/70 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        
        <div>
          <h1 className="text-3xl font-bold tracking-wide text-cyan-400">
            SkyPulse Mission Control
          </h1>

          <p className="text-slate-400 text-sm">
            Realtime Aircraft Telemetry Monitoring
          </p>
        </div>

        <div className="flex items-center gap-6">
          
          <div className="bg-slate-800 px-4 py-2 rounded-xl border border-slate-700">
            <p className="text-xs text-slate-400">
              Aircraft
            </p>

            <p className="text-lg font-bold">
              {aircraftCount}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div
              className={`
                h-3 w-3 rounded-full animate-pulse
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
    </div>
  );
}

export default Navbar;