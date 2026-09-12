-- ============================================================
-- SUPPLY-CHAIN DATA PLATFORM
-- SIMULATED OPERATIONAL SEED DATA
-- ============================================================


-- ============================================================
-- SUPPLIERS
-- ============================================================

INSERT INTO staging.seed_suppliers (
    supplier_id,
    supplier_name,
    supplier_city,
    supplier_state,
    supplier_country,
    lead_time_days,
    supplier_status
)
VALUES
(1, 'Supplier A', 'Mumbai', 'Maharashtra', 'India', 4, 'Active'),
(2, 'Supplier B', 'Delhi', 'Delhi', 'India', 3, 'Active'),
(3, 'Supplier C', 'Bengaluru', 'Karnataka', 'India', 5, 'Active'),
(4, 'Supplier D', 'Chennai', 'Tamil Nadu', 'India', 6, 'Active'),
(5, 'Supplier E', 'Hyderabad', 'Telangana', 'India', 4, 'Active'),
(6, 'Supplier F', 'Pune', 'Maharashtra', 'India', 7, 'Active'),
(7, 'Supplier G', 'Kolkata', 'West Bengal', 'India', 5, 'Active'),
(8, 'Supplier H', 'Ahmedabad', 'Gujarat', 'India', 6, 'Active'),
(9, 'Supplier I', 'Jaipur', 'Rajasthan', 'India', 4, 'Active'),
(10, 'Supplier J', 'Lucknow', 'Uttar Pradesh', 'India', 5, 'Active')
ON CONFLICT (supplier_id)
DO UPDATE SET
    supplier_name = EXCLUDED.supplier_name,
    supplier_city = EXCLUDED.supplier_city,
    supplier_state = EXCLUDED.supplier_state,
    supplier_country = EXCLUDED.supplier_country,
    lead_time_days = EXCLUDED.lead_time_days,
    supplier_status = EXCLUDED.supplier_status;


-- ============================================================
-- WAREHOUSES
-- ============================================================

INSERT INTO staging.seed_warehouses (
    warehouse_id,
    warehouse_name,
    warehouse_city,
    warehouse_state,
    warehouse_country,
    warehouse_capacity,
    warehouse_status
)
VALUES
(1, 'WH-North', 'Delhi', 'Delhi', 'India', 10000, 'Active'),
(2, 'WH-West', 'Mumbai', 'Maharashtra', 'India', 12000, 'Active'),
(3, 'WH-South', 'Bengaluru', 'Karnataka', 'India', 11000, 'Active'),
(4, 'WH-East', 'Kolkata', 'West Bengal', 'India', 9000, 'Active'),
(5, 'WH-Central', 'Hyderabad', 'Telangana', 'India', 10000, 'Active')
ON CONFLICT (warehouse_id)
DO UPDATE SET
    warehouse_name = EXCLUDED.warehouse_name,
    warehouse_city = EXCLUDED.warehouse_city,
    warehouse_state = EXCLUDED.warehouse_state,
    warehouse_country = EXCLUDED.warehouse_country,
    warehouse_capacity = EXCLUDED.warehouse_capacity,
    warehouse_status = EXCLUDED.warehouse_status;


-- ============================================================
-- VERIFY SUPPLIERS
-- ============================================================

SELECT *
FROM staging.seed_suppliers
ORDER BY supplier_id;


-- ============================================================
-- VERIFY WAREHOUSES
-- ============================================================

SELECT *
FROM staging.seed_warehouses
ORDER BY warehouse_id;


-- ============================================================
-- VERIFY INVENTORY
-- ============================================================

SELECT
    warehouse_id,
    COUNT(*) AS products_stocked,
    SUM(stock_quantity) AS current_inventory_units,
    COUNT(*) FILTER (
        WHERE stock_quantity = 0
    ) AS stockout_products
FROM staging.seed_inventory
GROUP BY warehouse_id
ORDER BY warehouse_id;