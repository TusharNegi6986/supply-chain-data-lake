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

function formatCurrency(value) {
  return `₹${Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}

function formatLakhs(value) {
  return `₹${(Number(value) / 100000).toFixed(1)}L`;
}

function CategoryPerformanceChart({ data }) {
  if (!data?.length) {
    return (
      <div className="chart-card">
        <p className="message">No category data available.</p>
      </div>
    );
  }

  const chartData = [...data]
    .sort(
      (a, b) =>
        Number(b.total_sales) - Number(a.total_sales)
    )
    .slice(0, 10)
    .map((item) => ({
      category_name: item.category_name,
      total_sales: Number(item.total_sales),
      total_profit: Number(item.total_profit),
    }))
    .reverse();

  return (
    <div className="chart-card">
      <div className="chart-header">
        <div>
          <h3>Top Product Categories</h3>

          <p>
            Top 10 categories ranked by total sales
          </p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height={360}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{
              top: 10,
              right: 70,
              left: 20,
              bottom: 10,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              horizontal={false}
              stroke="#e5e7eb"
            />

            <XAxis
              type="number"
              tickFormatter={formatLakhs}
              tick={{
                fontSize: 10,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
            />

            <YAxis
              type="category"
              dataKey="category_name"
              width={125}
              tick={{
                fontSize: 10,
                fill: "#4b5563",
              }}
              axisLine={false}
              tickLine={false}
            />

            <Tooltip
              cursor={{
                fill: "#f8fafc",
              }}
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
              formatter={(value) => [
                formatCurrency(value),
                "Sales",
              ]}
            />

            <Bar
              dataKey="total_sales"
              name="Sales"
              fill="#4f46e5"
              radius={[0, 5, 5, 0]}
              barSize={18}
            >
              <LabelList
                dataKey="total_sales"
                position="right"
                formatter={formatLakhs}
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

export default CategoryPerformanceChart;