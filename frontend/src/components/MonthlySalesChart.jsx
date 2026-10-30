import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

function formatMonth(value) {
  const date = new Date(value);

  return date.toLocaleDateString("en-US", {
    month: "short",
    year: "2-digit",
  });
}

function formatCurrencyAxis(value) {
  return `₹${(Number(value) / 100000).toFixed(0)}L`;
}

function formatCurrency(value) {
  return `₹${Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}

function MonthlySalesChart({ data }) {
  if (!data?.length) {
    return (
      <div className="chart-card">
        <p className="message">No monthly sales data available.</p>
      </div>
    );
  }

  const chartData = data.map((item) => ({
    monthLabel: formatMonth(item.month),
    total_sales: Number(item.total_sales),
    total_profit: Number(item.total_profit),
  }));

  return (
    <div className="chart-card">
      <div className="chart-header">
        <div>
          <h3>Monthly Sales & Profit</h3>

          <p>
            Revenue and profit performance over time
          </p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height={360}>
          <LineChart
            data={chartData}
            margin={{
              top: 15,
              right: 20,
              left: 5,
              bottom: 5,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#e5e7eb"
            />

            <XAxis
              dataKey="monthLabel"
              interval={2}
              tick={{
                fontSize: 11,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
            />

            <YAxis
              tickFormatter={formatCurrencyAxis}
              tick={{
                fontSize: 11,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
              width={55}
            />

            <Tooltip
              contentStyle={{
                border: "1px solid #e5e7eb",
                borderRadius: "10px",
                background: "#ffffff",
                boxShadow:
                  "0 8px 24px rgba(15, 23, 42, 0.10)",
                padding: "10px 12px",
              }}
              labelStyle={{
                color: "#374151",
                fontWeight: 700,
                marginBottom: "5px",
              }}
              formatter={(value, name) => [
                formatCurrency(value),
                name === "total_sales" ? "Sales" : "Profit",
              ]}
              labelFormatter={(label) => `Month: ${label}`}
            />

            <Legend
              verticalAlign="top"
              align="right"
              height={35}
              iconType="line"
              wrapperStyle={{
                fontSize: "11px",
                color: "#64748b",
              }}
            />

            <Line
              type="monotone"
              dataKey="total_sales"
              name="Sales"
              stroke="#4f46e5"
              strokeWidth={3}
              dot={false}
              activeDot={{
                r: 5,
              }}
            />

            <Line
              type="monotone"
              dataKey="total_profit"
              name="Profit"
              stroke="#16a34a"
              strokeWidth={3}
              dot={false}
              activeDot={{
                r: 5,
              }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default MonthlySalesChart;