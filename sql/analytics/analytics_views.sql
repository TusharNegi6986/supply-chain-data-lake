-- -- ============================================================
-- -- SUPPLY-CHAIN DATA PLATFORM
-- -- ANALYTICS VIEWS
-- -- ============================================================


-- -- ============================================================
-- -- 1. CATEGORY PERFORMANCE
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.category_performance AS
-- SELECT
--     c.category_id,
--     c.category_name,
--     d.department_id,
--     d.department_name,
--     COUNT(DISTINCT f.order_id) AS total_orders,
--     COUNT(*) AS total_items,
--     ROUND(SUM(f.sales), 2) AS total_sales,
--     ROUND(SUM(f.profit_per_order), 2) AS total_profit,
--     ROUND(AVG(f.product_price), 2) AS average_product_price,
--     ROUND(AVG(f.discount_rate), 4) AS average_discount_rate
-- FROM analytics.fact_order_items f
-- JOIN staging.categories c
--     ON f.category_id = c.category_id
-- JOIN staging.departments d
--     ON c.department_id = d.department_id
-- GROUP BY
--     c.category_id,
--     c.category_name,
--     d.department_id,
--     d.department_name
-- ORDER BY
--     ROUND(SUM(f.sales), 2) DESC;


-- -- ============================================================
-- -- 2. CUSTOMER SEGMENT PERFORMANCE
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.customer_segment_performance AS
-- SELECT
--     c.segment,
--     COUNT(DISTINCT f.customer_id) AS unique_customers,
--     COUNT(DISTINCT f.order_id) AS total_orders,
--     COUNT(*) AS total_items,
--     ROUND(SUM(f.sales), 2) AS total_sales,
--     ROUND(SUM(f.profit_per_order), 2) AS total_profit,
--     ROUND(AVG(f.sales), 2) AS average_sales_per_item
-- FROM analytics.fact_order_items f
-- JOIN staging.customers c
--     ON f.customer_id = c.customer_id
-- GROUP BY
--     c.segment
-- ORDER BY
--     ROUND(SUM(f.sales), 2) DESC;


-- -- ============================================================
-- -- 3. DELIVERY PERFORMANCE
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.delivery_performance AS
-- SELECT
--     delivery_status,
--     late_delivery_risk,
--     shipping_mode,
--     COUNT(DISTINCT order_id) AS total_orders,
--     ROUND(AVG(days_for_shipping_real), 2)
--         AS avg_actual_shipping_days,
--     ROUND(AVG(days_for_shipment_scheduled), 2)
--         AS avg_scheduled_shipping_days,
--     ROUND(
--         AVG(
--             days_for_shipping_real
--             - days_for_shipment_scheduled
--         ),
--         2
--     ) AS avg_shipping_delay_days
-- FROM analytics.fact_order_items
-- GROUP BY
--     delivery_status,
--     late_delivery_risk,
--     shipping_mode
-- ORDER BY
--     late_delivery_risk DESC,
--     COUNT(DISTINCT order_id) DESC;


-- -- ============================================================
-- -- 4. DEPARTMENT PERFORMANCE
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.department_performance AS
-- SELECT
--     d.department_id,
--     d.department_name,
--     COUNT(DISTINCT f.order_id) AS total_orders,
--     COUNT(*) AS total_items,
--     ROUND(SUM(f.sales), 2) AS total_sales,
--     ROUND(SUM(f.profit_per_order), 2) AS total_profit,
--     ROUND(AVG(f.discount_rate), 4)
--         AS average_discount_rate
-- FROM analytics.fact_order_items f
-- JOIN staging.categories c
--     ON f.category_id = c.category_id
-- JOIN staging.departments d
--     ON c.department_id = d.department_id
-- GROUP BY
--     d.department_id,
--     d.department_name
-- ORDER BY
--     ROUND(SUM(f.sales), 2) DESC;


-- -- ============================================================
-- -- 5. MONTHLY SALES
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.monthly_sales AS
-- SELECT
--     DATE_TRUNC('month', order_date)::date AS month,
--     COUNT(DISTINCT order_id) AS total_orders,
--     COUNT(*) AS total_order_items,
--     COUNT(DISTINCT customer_id) AS unique_customers,
--     ROUND(SUM(sales), 2) AS total_sales,
--     ROUND(SUM(discount), 2) AS total_discount,
--     ROUND(SUM(profit_per_order), 2) AS total_profit,
--     ROUND(AVG(sales), 2) AS average_sales_per_item
-- FROM analytics.fact_order_items
-- GROUP BY
--     DATE_TRUNC('month', order_date)
-- ORDER BY
--     DATE_TRUNC('month', order_date)::date;


-- -- ============================================================
-- -- 6. OVERALL KPIs
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.overall_kpis AS

-- WITH order_level AS (
--     SELECT
--         order_id,
--         MAX(profit_per_order) AS order_profit
--     FROM analytics.fact_order_items
--     GROUP BY order_id
-- ),

-- base AS (
--     SELECT
--         COUNT(DISTINCT order_id) AS total_orders,

--         COUNT(DISTINCT order_item_id)
--             AS total_order_items,

--         COUNT(DISTINCT customer_id)
--             AS total_customers,

--         COUNT(DISTINCT product_id)
--             AS total_products,

--         ROUND(SUM(sales), 2)
--             AS total_sales,

--         ROUND(SUM(discount), 2)
--             AS total_discount,

--         ROUND(AVG(days_for_shipping_real), 2)
--             AS avg_shipping_days,

--         COUNT(
--             DISTINCT CASE
--                 WHEN late_delivery_risk = 1
--                 THEN order_id
--             END
--         ) AS late_risk_orders,

--         ROUND(
--             100.0 *
--             COUNT(
--                 DISTINCT CASE
--                     WHEN late_delivery_risk = 1
--                     THEN order_id
--                 END
--             )
--             /
--             NULLIF(COUNT(DISTINCT order_id), 0),
--             2
--         ) AS late_risk_percentage

--     FROM analytics.fact_order_items
-- )

-- SELECT
--     total_orders,
--     total_order_items,
--     total_customers,
--     total_products,
--     total_sales,
--     total_discount,

--     ROUND(
--         (
--             SELECT SUM(order_profit)
--             FROM order_level
--         ),
--         2
--     ) AS total_profit,

--     avg_shipping_days,
--     late_risk_orders,
--     late_risk_percentage

-- FROM base;


-- -- ============================================================
-- -- 7. SHIPPING MODE PERFORMANCE
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.shipping_mode_performance AS
-- SELECT
--     shipping_mode,

--     COUNT(DISTINCT order_id)
--         AS total_orders,

--     COUNT(
--         DISTINCT CASE
--             WHEN late_delivery_risk = 1
--             THEN order_id
--         END
--     ) AS late_risk_orders,

--     ROUND(
--         100.0 *
--         COUNT(
--             DISTINCT CASE
--                 WHEN late_delivery_risk = 1
--                 THEN order_id
--             END
--         )
--         /
--         NULLIF(COUNT(DISTINCT order_id), 0),
--         2
--     ) AS late_risk_percentage,

--     ROUND(
--         AVG(days_for_shipping_real),
--         2
--     ) AS avg_actual_shipping_days,

--     ROUND(
--         AVG(days_for_shipment_scheduled),
--         2
--     ) AS avg_scheduled_shipping_days

-- FROM analytics.fact_order_items

-- GROUP BY shipping_mode

-- ORDER BY
--     COUNT(DISTINCT order_id) DESC;


-- -- ============================================================
-- -- 8. STATE PERFORMANCE
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.state_performance AS
-- SELECT
--     order_state,

--     COUNT(DISTINCT order_id)
--         AS total_orders,

--     COUNT(DISTINCT customer_id)
--         AS unique_customers,

--     ROUND(SUM(sales), 2)
--         AS total_sales,

--     ROUND(SUM(profit_per_order), 2)
--         AS total_profit,

--     COUNT(
--         DISTINCT CASE
--             WHEN late_delivery_risk = 1
--             THEN order_id
--         END
--     ) AS late_risk_orders,

--     ROUND(
--         100.0 *
--         COUNT(
--             DISTINCT CASE
--                 WHEN late_delivery_risk = 1
--                 THEN order_id
--             END
--         )
--         /
--         NULLIF(COUNT(DISTINCT order_id), 0),
--         2
--     ) AS late_risk_percentage

-- FROM analytics.fact_order_items

-- GROUP BY order_state

-- ORDER BY
--     ROUND(SUM(sales), 2) DESC;


-- -- ============================================================
-- -- 9. SUPPLY-CHAIN KPIs
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.supply_chain_kpis AS

-- WITH order_metrics AS (
--     SELECT
--         COUNT(DISTINCT o.order_id)
--             AS total_orders,

--         COUNT(
--             DISTINCT CASE
--                 WHEN o.order_status NOT IN (
--                     'CANCELED',
--                     'SUSPECTED_FRAUD'
--                 )
--                 THEN o.order_id
--             END
--         ) AS fulfilled_orders

--     FROM staging.orders o
-- ),

-- delivery_metrics AS (
--     SELECT
--         COUNT(*) AS total_deliveries,

--         COUNT(*) FILTER (
--             WHERE seed_deliveries.on_time = TRUE
--         ) AS on_time_deliveries

--     FROM staging.seed_deliveries
-- ),

-- inventory_metrics AS (
--     SELECT
--         SUM(stock_quantity)
--             AS current_inventory_units,

--         COUNT(*) FILTER (
--             WHERE stock_quantity = 0
--         ) AS stockout_products,

--         COUNT(*) FILTER (
--             WHERE stock_quantity <= reorder_point
--         ) AS reorder_products

--     FROM staging.seed_inventory
-- ),

-- demand_metrics AS (
--     SELECT
--         SUM(quantity) AS units_sold

--     FROM analytics.fact_order_items
-- ),

-- perfect_order_metrics AS (
--     SELECT
--         COUNT(*) AS total_orders,

--         COUNT(*) FILTER (
--             WHERE
--                 o.order_status NOT IN (
--                     'CANCELED',
--                     'SUSPECTED_FRAUD'
--                 )
--                 AND d.on_time = TRUE
--                 AND d.delivery_status = 'Shipping on time'
--         ) AS perfect_orders

--     FROM staging.orders o

--     JOIN staging.seed_shipments s
--         ON o.order_id = s.order_id

--     JOIN staging.seed_deliveries d
--         ON s.shipment_id = d.shipment_id
-- )

-- SELECT

--     om.total_orders,

--     om.fulfilled_orders,

--     ROUND(
--         100.0 *
--         om.fulfilled_orders
--         /
--         NULLIF(om.total_orders, 0),
--         2
--     ) AS order_fulfillment_rate,

--     dm.total_deliveries,

--     dm.on_time_deliveries,

--     ROUND(
--         100.0 *
--         dm.on_time_deliveries
--         /
--         NULLIF(dm.total_deliveries, 0),
--         2
--     ) AS on_time_delivery_rate,

--     demand.units_sold,

--     inv.current_inventory_units,

--     ROUND(
--         demand.units_sold::NUMERIC
--         /
--         NULLIF(inv.current_inventory_units, 0),
--         2
--     ) AS inventory_turnover,

--     inv.stockout_products,

--     ROUND(
--         100.0 *
--         inv.stockout_products
--         /
--         NULLIF(
--             (
--                 SELECT COUNT(*)
--                 FROM staging.seed_inventory
--             ),
--             0
--         ),
--         2
--     ) AS stockout_rate,

--     pom.perfect_orders,

--     ROUND(
--         100.0 *
--         pom.perfect_orders
--         /
--         NULLIF(pom.total_orders, 0),
--         2
--     ) AS perfect_order_rate

-- FROM order_metrics om

-- CROSS JOIN delivery_metrics dm

-- CROSS JOIN inventory_metrics inv

-- CROSS JOIN demand_metrics demand

-- CROSS JOIN perfect_order_metrics pom;


-- -- ============================================================
-- -- 10. WAREHOUSE INVENTORY PERFORMANCE
-- -- ============================================================

-- CREATE OR REPLACE VIEW analytics.warehouse_inventory_performance AS

-- WITH inventory_metrics AS (
--     SELECT
--         i.warehouse_id,

--         COUNT(*) AS products_stocked,

--         SUM(i.stock_quantity)
--             AS current_inventory_units,

--         COUNT(*) FILTER (
--             WHERE i.stock_quantity = 0
--         ) AS stockout_products,

--         COUNT(*) FILTER (
--             WHERE i.stock_quantity <= i.reorder_point
--         ) AS low_stock_products

--     FROM staging.seed_inventory i

--     GROUP BY i.warehouse_id
-- ),

-- warehouse_sales AS (
--     SELECT
--         i.warehouse_id,

--         SUM(oi.quantity)
--             AS units_sold

--     FROM staging.seed_inventory i

--     JOIN staging.order_items oi
--         ON i.product_id = oi.product_id

--     GROUP BY i.warehouse_id
-- )

-- SELECT

--     w.warehouse_id,

--     w.warehouse_name,

--     w.warehouse_city,

--     w.warehouse_state,

--     w.warehouse_capacity,

--     COALESCE(
--         im.products_stocked,
--         0
--     ) AS products_stocked,

--     COALESCE(
--         im.current_inventory_units,
--         0
--     ) AS current_inventory_units,

--     COALESCE(
--         im.stockout_products,
--         0
--     ) AS stockout_products,

--     COALESCE(
--         im.low_stock_products,
--         0
--     ) AS low_stock_products,

--     ROUND(
--         100.0 *
--         COALESCE(
--             im.current_inventory_units,
--             0
--         )::NUMERIC
--         /
--         NULLIF(
--             w.warehouse_capacity,
--             0
--         ),
--         2
--     ) AS inventory_utilization_percentage,

--     COALESCE(
--         ws.units_sold,
--         0
--     ) AS units_sold,

--     ROUND(
--         COALESCE(
--             ws.units_sold,
--             0
--         )::NUMERIC
--         /
--         NULLIF(
--             im.current_inventory_units,
--             0
--         ),
--         2
--     ) AS inventory_turnover_proxy

-- FROM staging.seed_warehouses w

-- LEFT JOIN inventory_metrics im
--     ON w.warehouse_id = im.warehouse_id

-- LEFT JOIN warehouse_sales ws
--     ON w.warehouse_id = ws.warehouse_id

-- ORDER BY
--     COALESCE(
--         im.current_inventory_units,
--         0
--     ) DESC;