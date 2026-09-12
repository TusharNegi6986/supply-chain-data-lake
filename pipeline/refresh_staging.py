from pathlib import Path

from db import get_connection

def refresh_staging():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # --------------------------------------------------
            # 1. Departments
            # --------------------------------------------------
            cursor.execute("""
                INSERT INTO staging.departments (
                    department_id,
                    department_name
                )
                SELECT DISTINCT
                    department_id,
                    department_name
                FROM staging.orders_processed
                WHERE department_id IS NOT NULL
                ON CONFLICT (department_id)
                DO UPDATE SET
                    department_name = EXCLUDED.department_name;
            """)

            # --------------------------------------------------
            # 2. Categories
            # --------------------------------------------------
            cursor.execute("""
                INSERT INTO staging.categories (
                    category_id,
                    category_name,
                    department_id
                )
                SELECT DISTINCT ON (category_id)
                    category_id,
                    category_name,
                    department_id
                FROM staging.orders_processed
                WHERE category_id IS NOT NULL
                ORDER BY category_id
                ON CONFLICT (category_id)
                DO UPDATE SET
                    category_name = EXCLUDED.category_name,
                    department_id = EXCLUDED.department_id;
            """)

            # --------------------------------------------------
            # 3. Customers
            # --------------------------------------------------
            cursor.execute("""
                INSERT INTO staging.customers (
                    customer_id,
                    first_name,
                    last_name,
                    email,
                    segment,
                    city,
                    state,
                    country,
                    street,
                    zipcode
                )
                SELECT DISTINCT ON (customer_id)
                    customer_id::TEXT,
                    customer_fname,
                    customer_lname,
                    customer_email,
                    customer_segment,
                    customer_city,
                    customer_state,
                    customer_country,
                    customer_street,
                    customer_zipcode
                FROM staging.orders_processed
                WHERE customer_id IS NOT NULL
                ORDER BY customer_id
                ON CONFLICT (customer_id)
                DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    email = EXCLUDED.email,
                    segment = EXCLUDED.segment,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state,
                    country = EXCLUDED.country,
                    street = EXCLUDED.street,
                    zipcode = EXCLUDED.zipcode;
            """)

            # --------------------------------------------------
            # 4. Products
            # --------------------------------------------------
            cursor.execute("""
                INSERT INTO staging.products (
                    product_id,
                    product_category_id,
                    category_id,
                    product_name,
                    product_description,
                    product_image,
                    product_price,
                    product_status
                )
                SELECT DISTINCT ON (product_card_id)
                    product_card_id,
                    product_category_id,
                    category_id,
                    product_name,
                    product_description,
                    product_image,
                    product_price,
                    product_status
                FROM staging.orders_processed
                WHERE product_card_id IS NOT NULL
                ORDER BY product_card_id
                ON CONFLICT (product_id)
                DO UPDATE SET
                    product_category_id = EXCLUDED.product_category_id,
                    category_id = EXCLUDED.category_id,
                    product_name = EXCLUDED.product_name,
                    product_description = EXCLUDED.product_description,
                    product_image = EXCLUDED.product_image,
                    product_price = EXCLUDED.product_price,
                    product_status = EXCLUDED.product_status;
            """)

            # --------------------------------------------------
            # 5. Orders
            # --------------------------------------------------
            cursor.execute("""
                INSERT INTO staging.orders (
                    order_id,
                    customer_id,
                    order_date,
                    order_status,
                    order_city,
                    order_state,
                    order_country,
                    order_region,
                    shipping_mode,
                    shipping_date,
                    days_for_shipping_real,
                    days_for_shipment_scheduled,
                    delivery_status,
                    late_delivery_risk
                )
                SELECT DISTINCT ON (order_id)
                    order_id,
                    order_customer_id::TEXT,
                    order_date,
                    order_status,
                    order_city,
                    order_state,
                    order_country,
                    order_region,
                    shipping_mode,
                    shipping_date,
                    days_for_shipping_real,
                    days_for_shipment_scheduled,
                    delivery_status,
                    late_delivery_risk
                FROM staging.orders_processed
                WHERE order_id IS NOT NULL
                ORDER BY order_id
                ON CONFLICT (order_id)
                DO UPDATE SET
                    customer_id = EXCLUDED.customer_id,
                    order_date = EXCLUDED.order_date,
                    order_status = EXCLUDED.order_status,
                    order_city = EXCLUDED.order_city,
                    order_state = EXCLUDED.order_state,
                    order_country = EXCLUDED.order_country,
                    order_region = EXCLUDED.order_region,
                    shipping_mode = EXCLUDED.shipping_mode,
                    shipping_date = EXCLUDED.shipping_date,
                    days_for_shipping_real = EXCLUDED.days_for_shipping_real,
                    days_for_shipment_scheduled = EXCLUDED.days_for_shipment_scheduled,
                    delivery_status = EXCLUDED.delivery_status,
                    late_delivery_risk = EXCLUDED.late_delivery_risk;
            """)

            # --------------------------------------------------
            # 6. Order Items
            # --------------------------------------------------
            cursor.execute("""
                INSERT INTO staging.order_items (
                    order_item_id,
                    order_id,
                    product_id,
                    product_category_id,
                    quantity,
                    product_price,
                    discount,
                    discount_rate,
                    sales,
                    order_item_total,
                    profit_per_order,
                    profit_ratio
                )
                SELECT
                    order_item_id,
                    order_id,
                    order_item_cardprod_id,
                    product_category_id,
                    order_item_quantity,
                    order_item_product_price,
                    order_item_discount,
                    order_item_discount_rate,
                    sales,
                    order_item_total,
                    order_profit_per_order,
                    order_item_profit_ratio
                FROM staging.orders_processed
                WHERE order_item_id IS NOT NULL
                ON CONFLICT (order_item_id)
                DO UPDATE SET
                    order_id = EXCLUDED.order_id,
                    product_id = EXCLUDED.product_id,
                    product_category_id = EXCLUDED.product_category_id,
                    quantity = EXCLUDED.quantity,
                    product_price = EXCLUDED.product_price,
                    discount = EXCLUDED.discount,
                    discount_rate = EXCLUDED.discount_rate,
                    sales = EXCLUDED.sales,
                    order_item_total = EXCLUDED.order_item_total,
                    profit_per_order = EXCLUDED.profit_per_order,
                    profit_ratio = EXCLUDED.profit_ratio;
            """)

        conn.commit()

        print("Staging refresh completed.")
        print("Source-derived staging tables updated successfully.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    refresh_staging()