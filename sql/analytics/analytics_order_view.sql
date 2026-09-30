CREATE SCHEMA IF NOT EXISTS analytics;

CREATE OR REPLACE VIEW analytics.analytics_order_view AS
SELECT
    row_number() OVER () AS id,
    supplier_name AS fields,
    supplier_city::text AS description
FROM staging.seed_suppliers
LIMIT 100;
