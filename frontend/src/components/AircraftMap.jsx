import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import L from "leaflet";


delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function AircraftMap({ telemetry }) {
  return (
    <div className="h-[500px] w-full rounded-xl overflow-hidden">
      <MapContainer
        center={[20.5937, 78.9629]}
        zoom={5}
        scrollWheelZoom={true}
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {telemetry.map((item) => (
          <Marker
            key={item.id}
            position={[item.latitude, item.longitude]}
          >
            <Popup>
              <div>
                <h2 className="font-bold">
                  Aircraft #{item.aircraft_id}
                </h2>

                <p>Altitude: {item.altitude} ft</p>
                <p>Speed: {item.speed} km/h</p>
                <p>Heading: {item.heading}°</p>
                <p>Fuel: {item.fuel_level ?? "N/A"}%</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Aircraft movement trail */}
        <Polyline
            positions={telemetry.map((t) => [
                t.latitude,
                t.longitude,
            ])}
            />

      </MapContainer>
    </div>
  );
}

export default AircraftMap;