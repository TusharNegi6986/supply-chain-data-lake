import KpiCard from "./KpiCard";

function KpiGrid({ data }) {
  if (!data) {
    return <p>Loading KPIs...</p>;
  }

  const kpis = [
    {
      title: "Total Orders",
      value: data.total_orders?.toLocaleString(),
      type: "orders",
    },
    {
      title: "Fulfillment Rate",
      value: data.order_fulfillment_rate,
      suffix: "%",
      type: "fulfillment",
    },
    {
      title: "On-Time Delivery",
      value: data.on_time_delivery_rate,
      suffix: "%",
      type: "delivery",
    },
    {
      title: "Units Sold",
      value: data.units_sold?.toLocaleString(),
      type: "units",
    },
    {
      title: "Current Inventory",
      value: data.current_inventory_units?.toLocaleString(),
      type: "inventory",
    },
    {
      title: "Inventory Turnover",
      value: data.inventory_turnover,
      type: "turnover",
    },
    {
      title: "Stockout Rate",
      value: data.stockout_rate,
      suffix: "%",
      type: "stockout",
    },
    {
      title: "Perfect Order Rate",
      value: data.perfect_order_rate,
      suffix: "%",
      type: "perfect",
    },
  ];

  return (
    <div className="kpi-grid">
      {kpis.map((kpi) => (
        <KpiCard key={kpi.title} {...kpi} />
      ))}
    </div>
  );
}

export default KpiGrid;