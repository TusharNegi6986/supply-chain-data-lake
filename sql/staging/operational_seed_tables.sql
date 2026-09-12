-- -- ============================================================
-- -- SUPPLY-CHAIN DATA PLATFORM
-- -- STAGING - SIMULATED OPERATIONAL TABLES
-- -- ============================================================
-- --
-- -- IMPORTANT:
-- -- These tables contain simulated operational data because
-- -- the DataCo dataset does not provide complete supplier,
-- -- warehouse and inventory relationships.
-- --


-- -- ============================================================
-- -- SUPPLIERS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.seed_suppliers (
--     supplier_id INTEGER NOT NULL,
--     supplier_name TEXT,
--     supplier_city TEXT,
--     supplier_state TEXT,
--     supplier_country TEXT,
--     lead_time_days INTEGER,
--     supplier_status TEXT,

--     CONSTRAINT seed_suppliers_pkey
--         PRIMARY KEY (supplier_id)
-- );


-- -- ============================================================
-- -- WAREHOUSES
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.seed_warehouses (
--     warehouse_id INTEGER NOT NULL,
--     warehouse_name TEXT,
--     warehouse_city TEXT,
--     warehouse_state TEXT,
--     warehouse_country TEXT,
--     warehouse_capacity INTEGER,
--     warehouse_status TEXT,

--     CONSTRAINT seed_warehouses_pkey
--         PRIMARY KEY (warehouse_id)
-- );


-- -- ============================================================
-- -- INVENTORY
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.seed_inventory (
--     inventory_id BIGINT NOT NULL,
--     warehouse_id INTEGER,
--     product_id INTEGER,
--     stock_quantity INTEGER,
--     reorder_point INTEGER,
--     reorder_quantity INTEGER,
--     last_updated TIMESTAMP,

--     CONSTRAINT seed_inventory_pkey
--         PRIMARY KEY (inventory_id)
-- );


-- -- ============================================================
-- -- SHIPMENTS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.seed_shipments (
--     shipment_id BIGINT NOT NULL,
--     order_id INTEGER,
--     warehouse_id INTEGER,
--     carrier TEXT,
--     tracking_number TEXT,
--     shipping_mode TEXT,
--     dispatch_date TIMESTAMP,
--     expected_delivery_date TIMESTAMP,
--     actual_delivery_date TIMESTAMP,

--     CONSTRAINT seed_shipments_pkey
--         PRIMARY KEY (shipment_id)
-- );


-- -- ============================================================
-- -- DELIVERIES
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.seed_deliveries (
--     delivery_id BIGINT NOT NULL,
--     shipment_id BIGINT,
--     order_id INTEGER,
--     delivery_status TEXT,
--     scheduled_delivery_date TIMESTAMP,
--     actual_delivery_date TIMESTAMP,
--     days_late INTEGER,
--     on_time BOOLEAN,

--     CONSTRAINT seed_deliveries_pkey
--         PRIMARY KEY (delivery_id)
-- );


-- -- ============================================================
-- -- SUPPLIER-PRODUCT RELATIONSHIP
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.seed_supplier_products (
--     supplier_id INTEGER NOT NULL,
--     product_id INTEGER NOT NULL,
--     supplier_unit_cost NUMERIC,
--     lead_time_days INTEGER,

--     CONSTRAINT seed_supplier_products_pkey
--         PRIMARY KEY (supplier_id, product_id),

--     CONSTRAINT seed_supplier_products_supplier_fk
--         FOREIGN KEY (supplier_id)
--         REFERENCES staging.seed_suppliers(supplier_id),

--     CONSTRAINT seed_supplier_products_product_fk
--         FOREIGN KEY (product_id)
--         REFERENCES staging.products(product_id),

--     CONSTRAINT supplier_unit_cost_check
--         CHECK (supplier_unit_cost >= 0),

--     CONSTRAINT supplier_lead_time_check
--         CHECK (lead_time_days >= 0)
-- );