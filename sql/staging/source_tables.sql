-- -- ============================================================
-- -- SUPPLY-CHAIN DATA PLATFORM
-- -- STAGING - SOURCE-DERIVED TABLES
-- -- ============================================================

-- -- ============================================================
-- -- DEPARTMENTS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.departments (
--     department_id INTEGER NOT NULL,
--     department_name TEXT,
--     CONSTRAINT departments_pkey PRIMARY KEY (department_id)
-- );


-- -- ============================================================
-- -- CATEGORIES
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.categories (
--     category_id INTEGER NOT NULL,
--     category_name TEXT,
--     department_id INTEGER,

--     CONSTRAINT categories_pkey
--         PRIMARY KEY (category_id),

--     CONSTRAINT categories_department_fk
--         FOREIGN KEY (department_id)
--         REFERENCES staging.departments(department_id)
-- );


-- -- ============================================================
-- -- CUSTOMERS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.customers (
--     customer_id TEXT NOT NULL,
--     first_name TEXT,
--     last_name TEXT,
--     email TEXT,
--     segment TEXT,
--     city TEXT,
--     state TEXT,
--     country TEXT,
--     street TEXT,
--     zipcode TEXT,

--     CONSTRAINT customers_pkey
--         PRIMARY KEY (customer_id)
-- );


-- -- ============================================================
-- -- PRODUCTS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.products (
--     product_id INTEGER NOT NULL,
--     product_category_id INTEGER,
--     category_id INTEGER,
--     product_name TEXT,
--     product_description TEXT,
--     product_image TEXT,
--     product_price NUMERIC,
--     product_status INTEGER,

--     CONSTRAINT products_pkey
--         PRIMARY KEY (product_id),

--     CONSTRAINT products_category_fk
--         FOREIGN KEY (category_id)
--         REFERENCES staging.categories(category_id)
-- );


-- -- ============================================================
-- -- ORDERS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.orders (
--     order_id INTEGER NOT NULL,
--     customer_id TEXT,
--     order_date TIMESTAMP,
--     order_status TEXT,
--     order_city TEXT,
--     order_state TEXT,
--     order_country TEXT,
--     order_region TEXT,
--     shipping_mode TEXT,
--     shipping_date TIMESTAMP,
--     days_for_shipping_real INTEGER,
--     days_for_shipment_scheduled INTEGER,
--     delivery_status TEXT,
--     late_delivery_risk INTEGER,

--     CONSTRAINT orders_pkey
--         PRIMARY KEY (order_id),

--     CONSTRAINT orders_customer_fk
--         FOREIGN KEY (customer_id)
--         REFERENCES staging.customers(customer_id)
-- );


-- -- ============================================================
-- -- ORDER ITEMS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.order_items (
--     order_item_id INTEGER NOT NULL,
--     order_id INTEGER,
--     product_id INTEGER,
--     product_category_id INTEGER,
--     quantity INTEGER,
--     product_price NUMERIC,
--     discount NUMERIC,
--     discount_rate NUMERIC,
--     sales NUMERIC,
--     order_item_total NUMERIC,
--     profit_per_order NUMERIC,
--     profit_ratio NUMERIC,

--     CONSTRAINT order_items_pkey
--         PRIMARY KEY (order_item_id),

--     CONSTRAINT order_items_order_fk
--         FOREIGN KEY (order_id)
--         REFERENCES staging.orders(order_id),

--     CONSTRAINT order_items_product_fk
--         FOREIGN KEY (product_id)
--         REFERENCES staging.products(product_id)
-- );


-- -- ============================================================
-- -- PROCESSED ORDERS
-- -- ============================================================

-- CREATE TABLE IF NOT EXISTS staging.orders_processed (
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