import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function OperationsLineChart({ data }) {
  const chartData = data.map((item) => ({
    time: new Date(item.timestamp).toLocaleTimeString(),
    hits: item.hits,
    misses: item.misses,
    evictions: item.evictions,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="hits" stroke="#10b981" strokeWidth={2} />
        <Line type="monotone" dataKey="misses" stroke="#ef4444" strokeWidth={2} />
        <Line type="monotone" dataKey="evictions" stroke="#f59e0b" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default OperationsLineChart;
