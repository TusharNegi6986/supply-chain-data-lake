-- -- ============================================================
-- -- SUPPLY-CHAIN DATA PLATFORM
-- -- DATABASE VERIFICATION
-- -- ============================================================


-- -- ============================================================
-- -- RAW LAYER
-- -- ============================================================

-- SELECT
--     COUNT(*) AS raw_rows,
--     COUNT(DISTINCT order_id) AS unique_orders,
--     COUNT(DISTINCT order_item_id) AS unique_order_items,
--     COUNT(DISTINCT customer_id) AS unique_customers,
--     COUNT(DISTINCT product_card_id) AS unique_products
-- FROM raw.orders_raw;


-- -- ============================================================
-- -- STAGING COUNTS
-- -- ============================================================

-- SELECT 'orders_processed' AS table_name,
--        COUNT(*) AS row_count
-- FROM staging.orders_processed

-- UNION ALL

-- SELECT 'customers',
--        COUNT(*)
-- FROM staging.customers

-- UNION ALL

-- SELECT 'orders',
--        COUNT(*)
-- FROM staging.orders

-- UNION ALL

-- SELECT 'order_items',
--        COUNT(*)
-- FROM staging.order_items

-- UNION ALL

-- SELECT 'products',
--        COUNT(*)
-- FROM staging.products

-- UNION ALL

-- SELECT 'categories',
--        COUNT(*)
-- FROM staging.categories

-- UNION ALL

-- SELECT 'departments',
--        COUNT(*)
-- FROM staging.departments;


-- -- ============================================================
-- -- OPERATIONAL SEED COUNTS
-- -- ============================================================

-- SELECT 'suppliers' AS table_name,
--        COUNT(*) AS row_count
-- FROM staging.seed_suppliers

-- UNION ALL

-- SELECT 'warehouses',
--        COUNT(*)
-- FROM staging.seed_warehouses

-- UNION ALL

-- SELECT 'inventory',
--        COUNT(*)
-- FROM staging.seed_inventory

-- UNION ALL

-- SELECT 'shipments',
--        COUNT(*)
-- FROM staging.seed_shipments

-- UNION ALL

-- SELECT 'deliveries',
--        COUNT(*)
-- FROM staging.seed_deliveries

-- UNION ALL

-- SELECT 'supplier_products',
--        COUNT(*)
-- FROM staging.seed_supplier_products;


-- -- ============================================================
-- -- FACT TABLE
-- -- ============================================================

-- SELECT
--     COUNT(*) AS total_rows,
--     COUNT(DISTINCT order_item_id) AS unique_order_items,
--     COUNT(DISTINCT order_id) AS unique_orders
-- FROM analytics.fact_order_items;


-- -- ============================================================
-- -- FACT TABLE NULL CHECK
-- -- ============================================================

-- SELECT
--     COUNT(*) FILTER (
--         WHERE order_item_id IS NULL
--     ) AS null_order_item_ids,

--     COUNT(*) FILTER (
--         WHERE order_id IS NULL
--     ) AS null_order_ids,

--     COUNT(*) FILTER (
--         WHERE customer_id IS NULL
--     ) AS null_customer_ids,

--     COUNT(*) FILTER (
--         WHERE product_id IS NULL
--     ) AS null_product_ids,

--     COUNT(*) FILTER (
--         WHERE order_date IS NULL
--     ) AS null_order_dates
-- FROM analytics.fact_order_items;


-- -- ============================================================
-- -- ANALYTICS VIEW COUNTS
-- -- ============================================================

-- SELECT 'supply_chain_kpis' AS view_name,
--        COUNT(*) AS row_count
-- FROM analytics.supply_chain_kpis

-- UNION ALL

-- SELECT 'monthly_sales',
--        COUNT(*)
-- FROM analytics.monthly_sales

-- UNION ALL

-- SELECT 'category_performance',
--        COUNT(*)
-- FROM analytics.category_performance

-- UNION ALL

-- SELECT 'delivery_performance',
--        COUNT(*)
-- FROM analytics.delivery_performance

-- UNION ALL

-- SELECT 'shipping_mode_performance',
--        COUNT(*)
-- FROM analytics.shipping_mode_performance

-- UNION ALL

-- SELECT 'warehouse_inventory_performance',
--        COUNT(*)
-- FROM analytics.warehouse_inventory_performance;


-- -- ============================================================
-- -- MAIN SUPPLY-CHAIN KPIs
-- -- ============================================================

-- SELECT *
-- FROM analytics.supply_chain_kpis;


-- -- ============================================================
-- -- WAREHOUSE PERFORMANCE
-- -- ============================================================

-- SELECT *
-- FROM analytics.warehouse_inventory_performance
-- ORDER BY warehouse_id;


-- -- ============================================================
-- -- SHIPPING MODE PERFORMANCE
-- -- ============================================================

-- SELECT *
-- FROM analytics.shipping_mode_performance
-- ORDER BY total_orders DESC;


-- -- ============================================================
-- -- DELIVERY PERFORMANCE
-- -- ============================================================

-- SELECT *
-- FROM analytics.delivery_performance
-- ORDER BY total_orders DESC;


-- -- ============================================================
-- -- MONTHLY SALES
-- -- ============================================================

-- SELECT *
-- FROM analytics.monthly_sales
-- ORDER BY month;


-- -- ============================================================
-- -- CATEGORY PERFORMANCE
-- -- ============================================================

-- SELECT *
-- FROM analytics.category_performance
-- ORDER BY total_sales DESC;


-- -- ============================================================
-- -- FINAL RECONCILIATION
-- -- ============================================================

-- SELECT
--     (SELECT COUNT(*)
--      FROM raw.orders_raw) AS raw_rows,

--     (SELECT COUNT(*)
--      FROM staging.orders_processed) AS processed_rows,

--     (SELECT COUNT(*)
--      FROM analytics.fact_order_items) AS fact_rows;


-- -- Expected:
-- --
-- -- raw_rows       = 180519
-- -- processed_rows = 180519
-- -- fact_rows      = 180519