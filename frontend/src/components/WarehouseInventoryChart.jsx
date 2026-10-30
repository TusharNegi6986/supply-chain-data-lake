import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LabelList,
} from "recharts";

function WarehouseInventoryChart({ data }) {
  if (!data?.length) {
    return (
      <div className="chart-card">
        <p className="message">
          No warehouse data available.
        </p>
      </div>
    );
  }

  const chartData = data.map((item) => ({
    warehouse_name: item.warehouse_name,
    current_inventory_units: Number(
      item.current_inventory_units || 0
    ),
    units_sold: Number(item.units_sold || 0),
  }));

  return (
    <div className="chart-card warehouse-chart-card">
      <div className="chart-header">
        <div>
          <h3>Warehouse Inventory Performance</h3>
          <p>
            Current inventory versus units sold across warehouses
          </p>
        </div>
      </div>

      <div className="chart-container warehouse-chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{
              top: 35,
              right: 20,
              left: 5,
              bottom: 35,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#e5e7eb"
            />

            <XAxis
              dataKey="warehouse_name"
              tick={{
                fontSize: 10,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
              interval={0}
              height={35}
            />

            <YAxis
              yAxisId="inventory"
              orientation="left"
              tickFormatter={(value) =>
                Number(value).toLocaleString()
              }
              tick={{
                fontSize: 10,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
              width={55}
            />

            <YAxis
              yAxisId="sales"
              orientation="right"
              tickFormatter={(value) =>
                Number(value).toLocaleString()
              }
              tick={{
                fontSize: 10,
                fill: "#6b7280",
              }}
              axisLine={false}
              tickLine={false}
              width={55}
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
              formatter={(value, name) => [
                Number(value).toLocaleString(),
                name,
              ]}
            />

            <Legend
              verticalAlign="top"
              align="right"
              height={35}
              wrapperStyle={{
                fontSize: "11px",
                color: "#64748b",
              }}
            />

            <Bar
              yAxisId="inventory"
              dataKey="current_inventory_units"
              name="Current Inventory"
              fill="#6366f1"
              radius={[4, 4, 0, 0]}
              barSize={28}
            >
              <LabelList
                dataKey="current_inventory_units"
                position="top"
                formatter={(value) =>
                  Number(value).toLocaleString()
                }
                style={{
                  fill: "#4b5563",
                  fontSize: 9,
                  fontWeight: 600,
                }}
              />
            </Bar>

            <Bar
              yAxisId="sales"
              dataKey="units_sold"
              name="Units Sold"
              fill="#10b981"
              radius={[4, 4, 0, 0]}
              barSize={28}
            >
              <LabelList
                dataKey="units_sold"
                position="top"
                formatter={(value) =>
                  Number(value).toLocaleString()
                }
                style={{
                  fill: "#4b5563",
                  fontSize: 9,
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

export default WarehouseInventoryChart;