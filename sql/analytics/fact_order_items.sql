-- -- ============================================================
-- -- SUPPLY-CHAIN DATA PLATFORM
-- -- ANALYTICS FACT TABLE
-- -- ============================================================

-- DROP TABLE IF EXISTS analytics.fact_order_items;

-- CREATE TABLE analytics.fact_order_items (
--     order_item_id INTEGER NOT NULL,
--     order_id INTEGER NOT NULL,
--     customer_id TEXT NOT NULL,
--     product_id INTEGER NOT NULL,

--     product_category_id INTEGER,
--     category_id INTEGER,

--     order_date TIMESTAMP NOT NULL,
--     shipping_date TIMESTAMP,

--     quantity INTEGER,
--     product_price NUMERIC,
--     discount NUMERIC,
--     discount_rate NUMERIC,

--     sales NUMERIC,
--     order_item_total NUMERIC,
--     profit_per_order NUMERIC,
--     profit_ratio NUMERIC,

--     days_for_shipping_real INTEGER,
--     days_for_shipment_scheduled INTEGER,

--     delivery_status TEXT,
--     late_delivery_risk INTEGER,
--     shipping_mode TEXT,

--     order_city TEXT,
--     order_state TEXT,
--     order_country TEXT,
--     order_region TEXT,

--     CONSTRAINT fact_order_items_pkey
--         PRIMARY KEY (order_item_id)
-- );