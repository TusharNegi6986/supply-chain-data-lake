# Supply-Chain Data Platform — API Data Contract

## Purpose

This document defines the PostgreSQL analytics views that the FastAPI backend will consume.

The backend should query the analytics views rather than directly querying raw or staging tables.

---

## 1. KPI Endpoint

### Endpoint

GET /api/kpis

### Source

analytics.supply_chain_kpis

### Fields

| Field | Type | Description |
|---|---|---|
| total_orders | bigint | Total number of orders |
| fulfilled_orders | bigint | Orders that are not cancelled or suspected fraud |
| order_fulfillment_rate | numeric | Percentage of fulfilled orders |
| total_deliveries | bigint | Total deliveries |
| on_time_deliveries | bigint | Deliveries completed on time |
| on_time_delivery_rate | numeric | Percentage of on-time deliveries |
| units_sold | bigint | Total units sold |
| current_inventory_units | bigint | Current inventory quantity |
| inventory_turnover | numeric | Simplified inventory turnover proxy |
| stockout_products | bigint | Number of products with zero stock |
| stockout_rate | numeric | Percentage of stocked products that are out of stock |
| perfect_orders | bigint | Orders meeting the project's perfect-order conditions |
| perfect_order_rate | numeric | Percentage of perfect orders |

---

## 2. Monthly Sales

### Endpoint

GET /api/monthly-sales

### Source

analytics.monthly_sales

### Fields

- month
- total_orders
- total_order_items
- unique_customers
- total_sales
- total_discount
- total_profit
- average_sales_per_item

---

## 3. Category Performance

### Endpoint

GET /api/categories

### Source

analytics.category_performance

### Fields

- category_id
- category_name
- department_id
- department_name
- total_orders
- total_items
- total_sales
- total_profit
- average_product_price
- average_discount_rate

---

## 4. Delivery Performance

### Endpoint

GET /api/delivery

### Source

analytics.delivery_performance

### Fields

- delivery_status
- late_delivery_risk
- shipping_mode
- total_orders
- avg_actual_shipping_days
- avg_scheduled_shipping_days
- avg_shipping_delay_days

---

## 5. Shipping Mode Performance

### Endpoint

GET /api/shipping-modes

### Source

analytics.shipping_mode_performance

### Fields

- shipping_mode
- total_orders
- late_risk_orders
- late_risk_percentage
- avg_actual_shipping_days
- avg_scheduled_shipping_days

---

## 6. Warehouse Performance

### Endpoint

GET /api/warehouses

### Source

analytics.warehouse_inventory_performance

### Fields

- warehouse_id
- warehouse_name
- warehouse_city
- warehouse_state
- warehouse_capacity
- products_stocked
- current_inventory_units
- stockout_products
- low_stock_products
- inventory_utilization_percentage
- units_sold
- inventory_turnover_proxy

---

# Dashboard Filters

## Date

Applicable to:
- Monthly Sales
- Category Performance
- Delivery Performance
- Shipping Mode Performance

## Shipping Mode

Applicable to:
- Delivery Performance
- Shipping Mode Performance

## Warehouse

Applicable to:
- Warehouse Performance

---

# Important Data Notes

1. DataCo is the primary historical dataset.
2. Supplier, warehouse and inventory operational data are simulated project data.
3. Warehouse sales allocation is simulated because the original DataCo dataset does not contain a warehouse relationship.
4. `inventory_turnover` and `inventory_turnover_proxy` are simplified project metrics and should not be presented as standard accounting inventory turnover.
5. Raw data must remain unchanged.
6. Backend should consume analytics views rather than raw tables.