import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function TelemetryChart({
  data,
  dataKey,
  title,
}) {
  return (
    <div className="bg-slate-900 p-4 rounded-xl border border-slate-700">
      <h2 className="text-xl font-semibold mb-4">
        {title}
      </h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="id"
            stroke="#ffffff"
          />

          <YAxis stroke="#ffffff" />

          <Tooltip />

          <Line
            type="monotone"
            dataKey={dataKey}
            stroke="#38bdf8"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TelemetryChart;