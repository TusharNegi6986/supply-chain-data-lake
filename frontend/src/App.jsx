import { useEffect, useState } from "react";

import {
  LayoutDashboard,
  BarChart3,
  Truck,
  Warehouse,
  Database,
  Activity,
  RefreshCw,
  ArrowUpRight,
} from "lucide-react";

import {
  getKPIs,
  getMonthlySales,
  getCategories,
  getDelivery,
  getShippingModes,
  getWarehouses,
} from "./services/api";

import KpiGrid from "./components/KpiGrid";
import MonthlySalesChart from "./components/MonthlySalesChart";
import CategoryPerformanceChart from "./components/CategoryPerformanceChart";
import DeliveryPerformanceChart from "./components/DeliveryPerformanceChart";
import ShippingModeChart from "./components/ShippingModeChart";
import WarehouseInventoryChart from "./components/WarehouseInventoryChart";

import "./styles/dashboard.css";

function App() {
  const [activeView, setActiveView] = useState("dashboard");

  const [kpis, setKpis] = useState(null);
  const [monthlySales, setMonthlySales] = useState([]);
  const [categories, setCategories] = useState([]);
  const [delivery, setDelivery] = useState([]);
  const [shippingModes, setShippingModes] = useState([]);
  const [warehouses, setWarehouses] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [
        kpiData,
        salesData,
        categoryData,
        deliveryData,
        shippingData,
        warehouseData,
      ] = await Promise.all([
        getKPIs(),
        getMonthlySales(),
        getCategories(),
        getDelivery(),
        getShippingModes(),
        getWarehouses(),
      ]);

      setKpis(kpiData);
      setMonthlySales(salesData);
      setCategories(categoryData);
      setDelivery(deliveryData);
      setShippingModes(shippingData);
      setWarehouses(warehouseData);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the analytics API.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleNavigation = (view) => {
    setActiveView(view);
  };

  const renderDashboard = () => (
    <>
      <section className="dashboard-section overview-section">
        <div className="section-heading compact-heading">
          <div>
            <span className="section-kicker">OVERVIEW</span>
            <h2>Key Performance Indicators</h2>
            <p>
              Current operational health across the supply chain
            </p>
          </div>
        </div>

        <KpiGrid data={kpis} />
      </section>

      <section className="dashboard-section dashboard-charts-section">
        <div className="chart-grid dashboard-chart-grid">
          <div className="chart-grid-wide">
            <MonthlySalesChart data={monthlySales} />
          </div>

          <div className="chart-grid-wide">
            <CategoryPerformanceChart data={categories} />
          </div>
        </div>
      </section>

      <section className="business-signal">
        <div className="signal-content">
          <span className="signal-label">
            SUPPLY CHAIN SIGNAL
          </span>

          <h2>
            Fulfillment is strong, but delivery reliability needs attention
          </h2>

          <p>
            Orders are being fulfilled at{" "}
            <strong>
              {kpis?.order_fulfillment_rate}%
            </strong>
            , while on-time delivery is only{" "}
            <strong>
              {kpis?.on_time_delivery_rate}%
            </strong>
            .
          </p>
        </div>

        <div className="signal-metric">
          <span>On-Time Delivery</span>

          <strong>
            {kpis?.on_time_delivery_rate}%
          </strong>

          <ArrowUpRight
            size={17}
            className="signal-arrow"
          />
        </div>
      </section>
    </>
  );

  const renderSales = () => (
    <div className="view-layout">
      <div className="view-heading">
        <div>
          <span className="section-kicker">SALES ANALYTICS</span>
          <h2>Sales Performance</h2>
          <p>
            Revenue trends and category-level performance
          </p>
        </div>
      </div>

      <div className="chart-grid">
        <div className="chart-grid-wide">
          <MonthlySalesChart data={monthlySales} />
        </div>

        <div className="chart-grid-wide">
          <CategoryPerformanceChart data={categories} />
        </div>
      </div>
    </div>
  );

  const renderLogistics = () => (
    <div className="view-layout">
      <div className="view-heading">
        <div>
          <span className="section-kicker">LOGISTICS</span>
          <h2>Delivery & Shipping</h2>
          <p>
            Delivery reliability and shipping mode performance
          </p>
        </div>
      </div>

      <div className="chart-grid">
        <DeliveryPerformanceChart data={delivery} />

        <ShippingModeChart data={shippingModes} />
      </div>

      <div className="business-signal logistics-signal">
        <div className="signal-content">
          <span className="signal-label">
            LOGISTICS SIGNAL
          </span>

          <h2>
            On-time delivery is the primary operational opportunity
          </h2>

          <p>
            Overall on-time delivery currently stands at{" "}
            <strong>
              {kpis?.on_time_delivery_rate}%
            </strong>
            .
          </p>
        </div>

        <div className="signal-metric">
          <span>On-Time Rate</span>

          <strong>
            {kpis?.on_time_delivery_rate}%
          </strong>
        </div>
      </div>
    </div>
  );

  const renderInventory = () => (
    <div className="view-layout">
      <div className="view-heading">
        <div>
          <span className="section-kicker">INVENTORY</span>
          <h2>Warehouse Performance</h2>
          <p>
            Inventory levels, utilization and warehouse activity
          </p>
        </div>
      </div>

      <div className="inventory-main-chart">
        <WarehouseInventoryChart data={warehouses} />
      </div>

      <div className="inventory-summary-grid">
        <div className="inventory-summary-card">
          <span>Current Inventory</span>
          <strong>
            {kpis?.current_inventory_units?.toLocaleString()}
          </strong>
        </div>

        <div className="inventory-summary-card">
          <span>Inventory Turnover</span>
          <strong>
            {kpis?.inventory_turnover}
          </strong>
        </div>

        <div className="inventory-summary-card">
          <span>Stockout Rate</span>
          <strong>
            {kpis?.stockout_rate}%
          </strong>
        </div>

        <div className="inventory-summary-card">
          <span>Units Sold</span>
          <strong>
            {kpis?.units_sold?.toLocaleString()}
          </strong>
        </div>
      </div>
    </div>
  );

  const renderActiveView = () => {
    switch (activeView) {
      case "sales":
        return renderSales();

      case "logistics":
        return renderLogistics();

      case "inventory":
        return renderInventory();

      default:
        return renderDashboard();
    }
  };

  return (
    <div className="app-shell">

      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">
            <Database size={21} />
          </div>

          <div>
            <h2>SupplyChain</h2>
            <span>Data Platform</span>
          </div>
        </div>

        <nav className="sidebar-nav">

          <p className="nav-label">
            WORKSPACE
          </p>

          <button
            className={`nav-item ${
              activeView === "dashboard"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("dashboard")
            }
          >
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </button>

          <button
            className={`nav-item ${
              activeView === "sales"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("sales")
            }
          >
            <BarChart3 size={18} />
            <span>Sales Analytics</span>
          </button>

          <button
            className={`nav-item ${
              activeView === "logistics"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("logistics")
            }
          >
            <Truck size={18} />
            <span>Logistics</span>
          </button>

          <button
            className={`nav-item ${
              activeView === "inventory"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handleNavigation("inventory")
            }
          >
            <Warehouse size={18} />
            <span>Inventory</span>
          </button>

        </nav>

        <div className="sidebar-footer">

          <div className="system-status">
            <span className="status-indicator"></span>

            <div>
              <strong>
                System Online
              </strong>

              <span>
                Analytics API connected
              </span>
            </div>
          </div>

          <div className="project-info">
            <span>
              Supply Chain Data Lake
            </span>

            <span>
              v1.0.0
            </span>
          </div>

        </div>
      </aside>

      {/* =====================================================
          MAIN CONTENT
      ===================================================== */}

      <div className="main-content">

        {/* Header */}

        <header className="topbar">

          <div className="topbar-title">

            <p className="eyebrow">
              SUPPLY CHAIN DATA PLATFORM
            </p>

            <h1>
              {activeView === "dashboard" &&
                "Supply Chain Analytics"}

              {activeView === "sales" &&
                "Sales Analytics"}

              {activeView === "logistics" &&
                "Logistics Analytics"}

              {activeView === "inventory" &&
                "Inventory Analytics"}
            </h1>

            <p className="page-description">
              {activeView === "dashboard" &&
                "Executive overview of orders, fulfillment, delivery and inventory performance."}

              {activeView === "sales" &&
                "Revenue trends, category performance and sales insights."}

              {activeView === "logistics" &&
                "Delivery reliability and shipping performance across the supply chain."}

              {activeView === "inventory" &&
                "Warehouse inventory levels, utilization and stock movement."}
            </p>

          </div>

          <div className="topbar-actions">

            <button
              className="refresh-button"
              onClick={loadDashboardData}
              disabled={loading}
            >
              <RefreshCw
                size={15}
                className={
                  loading ? "spinning" : ""
                }
              />

              Refresh
            </button>

            <div className="live-status">

              <span className="live-dot"></span>

              <span>
                Live Analytics
              </span>

            </div>

          </div>

        </header>

        {/* Content */}

        <main className="dashboard-content">

          {loading && (
            <div className="loading-state">
              <Activity size={20} />
              <span>
                Loading analytics...
              </span>
            </div>
          )}

          {error && (
            <div className="error-state">
              <strong>
                Connection Error
              </strong>

              <span>
                {error}
              </span>
            </div>
          )}

          {!loading &&
            !error &&
            renderActiveView()}

        </main>

        {/* Footer */}

        <footer className="dashboard-footer">

          <span>
            Supply Chain Data Platform
          </span>

          <span>
            PostgreSQL • FastAPI • React
          </span>

        </footer>

      </div>
    </div>
  );
}

export default App;