import {
  ShoppingCart,
  CheckCircle,
  Truck,
  Package,
  Warehouse,
  RefreshCw,
  AlertTriangle,
  Trophy,
} from "lucide-react";

const icons = {
  orders: ShoppingCart,
  fulfillment: CheckCircle,
  delivery: Truck,
  units: Package,
  inventory: Warehouse,
  turnover: RefreshCw,
  stockout: AlertTriangle,
  perfect: Trophy,
};

function KpiCard({ title, value, suffix = "", type }) {
  const Icon = icons[type] || Package;

  return (
    <div className="kpi-card">
      <div className="kpi-card-header">
        <span className="kpi-title">{title}</span>
        <div className="kpi-icon">
          <Icon size={20} />
        </div>
      </div>

      <div className="kpi-value">
        {value}
        {suffix && <span className="kpi-suffix">{suffix}</span>}
      </div>
    </div>
  );
}

export default KpiCard;
