-- -- ============================================================
-- -- SUPPLY-CHAIN DATA PLATFORM
-- -- RAW LAYER
-- -- ============================================================

-- DROP TABLE IF EXISTS raw.orders_raw;

-- CREATE TABLE raw.orders_raw (
--     row_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

--     type TEXT,
--     days_for_shipping_real INTEGER,
--     days_for_shipment_scheduled INTEGER,
--     benefit_per_order NUMERIC,
--     sales_per_customer NUMERIC,
--     delivery_status TEXT,
--     late_delivery_risk INTEGER,

--     category_id INTEGER,
--     category_name TEXT,

--     customer_city TEXT,
--     customer_country TEXT,
--     customer_email TEXT,
--     customer_fname TEXT,
--     customer_id INTEGER,
--     customer_lname TEXT,
--     customer_password TEXT,
--     customer_segment TEXT,
--     customer_state TEXT,
--     customer_street TEXT,
--     customer_zipcode TEXT,

--     department_id INTEGER,
--     department_name TEXT,

--     latitude NUMERIC,
--     longitude NUMERIC,

--     market TEXT,

--     order_city TEXT,
--     order_country TEXT,
--     order_customer_id INTEGER,
--     order_date TIMESTAMP,
--     order_id INTEGER,

--     order_item_cardprod_id INTEGER,
--     order_item_discount NUMERIC,
--     order_item_discount_rate NUMERIC,
--     order_item_id INTEGER,
--     order_item_product_price NUMERIC,
--     order_item_profit_ratio NUMERIC,
--     order_item_quantity INTEGER,

--     sales NUMERIC,
--     order_item_total NUMERIC,
--     order_profit_per_order NUMERIC,

--     order_region TEXT,
--     order_state TEXT,
--     order_status TEXT,
--     order_zipcode TEXT,

--     product_card_id INTEGER,
--     product_category_id INTEGER,
--     product_description TEXT,
--     product_image TEXT,
--     product_name TEXT,
--     product_price NUMERIC,
--     product_status INTEGER,

--     shipping_date TIMESTAMP,
--     shipping_mode TEXT
-- );