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

function ShippingModeChart({ data }) {
  if (!data?.length) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h3>Shipping Mode Performance</h3>
            <p>Order volume across shipping methods</p>
          </div>
        </div>

        <div className="chart-empty">
          No shipping mode data available.
        </div>
      </div>
    );
  }

  const chartData = data.map((item) => ({
    shipping_mode: item.shipping_mode,
    total_orders: Number(item.total_orders || 0),
    average_shipping_days: Number(
      item.average_shipping_days || 0
    ),
  }));

  return (
    <div className="chart-card logistics-chart-card">
      <div className="chart-header">
        <div>
          <h3>Shipping Mode Performance</h3>
          <p>Order volume across shipping methods</p>
        </div>
      </div>

      <div className="chart-container logistics-chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{
              top: 30,
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
              tickFormatter={(value) =>
                Number(value).toLocaleString()
              }
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
              formatter={(value, name) => {
                if (name === "Orders") {
                  return [
                    Number(value).toLocaleString(),
                    "Orders",
                  ];
                }

                return [
                  `${Number(value).toFixed(2)} days`,
                  "Avg shipping time",
                ];
              }}
            />

            <Bar
              dataKey="total_orders"
              name="Orders"
              fill="#0ea5e9"
              radius={[5, 5, 0, 0]}
              barSize={42}
            >
              <LabelList
                dataKey="total_orders"
                position="top"
                formatter={(value) =>
                  Number(value).toLocaleString()
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

export default ShippingModeChart;