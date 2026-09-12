import sys
from pathlib import Path

from db import get_connection


def refresh_fact_table():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                TRUNCATE TABLE analytics.fact_order_items;

                INSERT INTO analytics.fact_order_items (
                    order_item_id,
                    order_id,
                    customer_id,
                    product_id,
                    product_category_id,
                    category_id,
                    order_date,
                    shipping_date,
                    quantity,
                    product_price,
                    discount,
                    discount_rate,
                    sales,
                    order_item_total,
                    profit_per_order,
                    profit_ratio,
                    days_for_shipping_real,
                    days_for_shipment_scheduled,
                    delivery_status,
                    late_delivery_risk,
                    shipping_mode,
                    order_city,
                    order_state,
                    order_country,
                    order_region
                )
                SELECT
                    oi.order_item_id,
                    oi.order_id,
                    o.customer_id,
                    oi.product_id,
                    oi.product_category_id,
                    p.category_id,
                    o.order_date,
                    o.shipping_date,
                    oi.quantity,
                    oi.product_price,
                    oi.discount,
                    oi.discount_rate,
                    oi.sales,
                    oi.order_item_total,
                    oi.profit_per_order,
                    oi.profit_ratio,
                    o.days_for_shipping_real,
                    o.days_for_shipment_scheduled,
                    o.delivery_status,
                    o.late_delivery_risk,
                    o.shipping_mode,
                    o.order_city,
                    o.order_state,
                    o.order_country,
                    o.order_region
                FROM staging.order_items oi
                JOIN staging.orders o
                    ON oi.order_id = o.order_id
                JOIN staging.products p
                    ON oi.product_id = p.product_id;
            """)

            cursor.execute("""
                SELECT COUNT(*)
                FROM analytics.fact_order_items;
            """)

            fact_rows = cursor.fetchone()[0]

        conn.commit()

        print("Fact table refresh completed.")
        print(f"Rows in analytics.fact_order_items: {fact_rows}")

        if fact_rows != 180519:
            print("WARNING: Expected 180519 rows.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    refresh_fact_table()