import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  LabelList,
} from "recharts";

function DeliveryPerformanceChart({ data }) {
  if (!data?.length) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h3>Delivery Performance</h3>
            <p>Average shipping delay by shipping mode</p>
          </div>
        </div>

        <div className="chart-empty">
          No delivery data available.
        </div>
      </div>
    );
  }

  const shippingModes = [
    "Standard Class",
    "Second Class",
    "First Class",
    "Same Day",
  ];

  const chartData = shippingModes.map((mode) => {
    const rows = data.filter(
      (item) =>
        item.shipping_mode === mode &&
        item.delivery_status !== "Shipping canceled"
    );

    const totalOrders = rows.reduce(
      (sum, item) =>
        sum + Number(item.total_orders || 0),
      0
    );

    const weightedDelay =
      totalOrders > 0
        ? rows.reduce(
            (sum, item) =>
              sum +
              Number(item.avg_shipping_delay_days || 0) *
                Number(item.total_orders || 0),
            0
          ) / totalOrders
        : 0;

    return {
      shipping_mode: mode,
      avg_delay: Number(weightedDelay.toFixed(2)),
    };
  });

  return (
    <div className="chart-card logistics-chart-card">
      <div className="chart-header">
        <div>
          <h3>Delivery Performance</h3>
          <p>Average shipping delay by shipping mode</p>
        </div>
      </div>

      <div className="chart-container logistics-chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{
              top: 25,
              right: 20,
              left: 5,
              bottom: 10,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#e5e7eb"
            />

            <XAxis
              dataKey="shipping_mode"
              tick={{
                fontSize: 10,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
            />

            <YAxis
              tickFormatter={(value) => `${value}d`}
              tick={{
                fontSize: 10,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
            />

            <Tooltip
              cursor={{ fill: "#f8fafc" }}
              contentStyle={{
                border: "1px solid #e5e7eb",
                borderRadius: "10px",
                background: "#ffffff",
                boxShadow:
                  "0 8px 24px rgba(15, 23, 42, 0.10)",
              }}
              formatter={(value) => [
                `${Number(value).toFixed(2)} days`,
                "Average delay",
              ]}
            />

            <Bar
              dataKey="avg_delay"
              name="Average delay"
              fill="#f59e0b"
              radius={[5, 5, 0, 0]}
              barSize={42}
            >
              <LabelList
                dataKey="avg_delay"
                position="top"
                formatter={(value) =>
                  `${Number(value).toFixed(1)}d`
                }
                style={{
                  fill: "#4b5563",
                  fontSize: 10,
                  fontWeight: 600,
                }}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default DeliveryPerformanceChart;