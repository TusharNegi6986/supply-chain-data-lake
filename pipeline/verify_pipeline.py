from db import get_connection


EXPECTED = {
    "orders_processed": 180519,
    "customers": 20652,
    "orders": 65752,
    "order_items": 180519,
    "products": 118,
    "categories": 51,
    "departments": 11,
    "fact_order_items": 180519,
}


def verify_pipeline():
    conn = get_connection()
    failures = []

    try:
        with conn.cursor() as cursor:

            checks = {
                "orders_processed": "SELECT COUNT(*) FROM staging.orders_processed",
                "customers": "SELECT COUNT(*) FROM staging.customers",
                "orders": "SELECT COUNT(*) FROM staging.orders",
                "order_items": "SELECT COUNT(*) FROM staging.order_items",
                "products": "SELECT COUNT(*) FROM staging.products",
                "categories": "SELECT COUNT(*) FROM staging.categories",
                "departments": "SELECT COUNT(*) FROM staging.departments",
                "fact_order_items": "SELECT COUNT(*) FROM analytics.fact_order_items",
            }

            print("\nPIPELINE DATA QUALITY CHECK")
            print("=" * 60)

            for name, query in checks.items():
                cursor.execute(query)
                actual = cursor.fetchone()[0]
                expected = EXPECTED[name]

                if actual == expected:
                    print(f"{name:20} PASSED  ({actual})")
                else:
                    print(
                        f"{name:20} FAILED  "
                        f"(expected {expected}, got {actual})"
                    )
                    failures.append(name)

        if failures:
            print("\nDATA QUALITY CHECK FAILED")
            print("Failed checks:", ", ".join(failures))
            raise SystemExit(1)

        print("\nDATA QUALITY CHECK PASSED")

    finally:
        conn.close()


if __name__ == "__main__":
    verify_pipeline()