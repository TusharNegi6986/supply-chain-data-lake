import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "datalake" / "raw"
REPORT_DIR = PROJECT_ROOT / "pipeline" / "reports"


EXPECTED_COLUMNS = [
    "Type",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Benefit per order",
    "Sales per customer",
    "Delivery Status",
    "Late_delivery_risk",
    "Category Id",
    "Category Name",
    "Customer City",
    "Customer Country",
    "Customer Email",
    "Customer Fname",
    "Customer Id",
    "Customer Lname",
    "Customer Password",
    "Customer Segment",
    "Customer State",
    "Customer Street",
    "Customer Zipcode",
    "Department Id",
    "Department Name",
    "Latitude",
    "Longitude",
    "Market",
    "Order City",
    "Order Country",
    "Order Customer Id",
    "order date (DateOrders)",
    "Order Id",
    "Order Item Cardprod Id",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Id",
    "Order Item Product Price",
    "Order Item Profit Ratio",
    "Order Item Quantity",
    "Sales",
    "Order Item Total",
    "Order Profit Per Order",
    "Order Region",
    "Order State",
    "Order Status",
    "Order Zipcode",
    "Product Card Id",
    "Product Category Id",
    "Product Description",
    "Product Image",
    "Product Name",
    "Product Price",
    "Product Status",
    "shipping date (DateOrders)",
    "Shipping Mode",
]


def validate_schema(file_path):
    """Validate the CSV schema."""

    with open(file_path, "r", encoding="latin1", newline="") as file:
        reader = csv.reader(file)
        actual_columns = next(reader)

    result = {
        "expected_columns": len(EXPECTED_COLUMNS),
        "actual_columns": len(actual_columns),
        "passed": actual_columns == EXPECTED_COLUMNS,
    }

    if actual_columns != EXPECTED_COLUMNS:
        result["missing_columns"] = [
            column for column in EXPECTED_COLUMNS
            if column not in actual_columns
        ]

        result["unexpected_columns"] = [
            column for column in actual_columns
            if column not in EXPECTED_COLUMNS
        ]

    return result


def validate_rows(file_path):
    """Validate critical row-level fields."""

    total_rows = 0
    duplicate_order_items = 0

    seen_order_items = set()

    missing_order_ids = 0
    missing_customer_ids = 0
    missing_product_ids = 0
    missing_order_item_ids = 0

    with open(file_path, "r", encoding="latin1", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1

            order_id = row["Order Id"].strip()
            customer_id = row["Customer Id"].strip()
            product_id = row["Product Card Id"].strip()
            order_item_id = row["Order Item Id"].strip()

            if not order_id:
                missing_order_ids += 1

            if not customer_id:
                missing_customer_ids += 1

            if not product_id:
                missing_product_ids += 1

            if not order_item_id:
                missing_order_item_ids += 1

            if order_item_id:
                if order_item_id in seen_order_items:
                    duplicate_order_items += 1
                else:
                    seen_order_items.add(order_item_id)

    return {
        "total_rows": total_rows,
        "duplicate_order_item_ids": duplicate_order_items,
        "missing_order_ids": missing_order_ids,
        "missing_customer_ids": missing_customer_ids,
        "missing_product_ids": missing_product_ids,
        "missing_order_item_ids": missing_order_item_ids,
    }


def validate_business_rules(file_path):
    """Validate business rules and value ranges."""

    invalid_late_risk = 0
    invalid_quantity = 0
    invalid_product_price = 0
    invalid_shipping_days = 0
    missing_order_dates = 0
    missing_shipping_dates = 0

    shipping_modes = set()

    with open(file_path, "r", encoding="latin1", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            late_risk = row["Late_delivery_risk"].strip()
            quantity = row["Order Item Quantity"].strip()
            product_price = row["Order Item Product Price"].strip()
            shipping_days = row["Days for shipping (real)"].strip()
            order_date = row["order date (DateOrders)"].strip()
            shipping_date = row["shipping date (DateOrders)"].strip()
            shipping_mode = row["Shipping Mode"].strip()

            if late_risk not in {"0", "1"}:
                invalid_late_risk += 1

            if quantity:
                try:
                    if int(quantity) <= 0:
                        invalid_quantity += 1
                except ValueError:
                    invalid_quantity += 1

            if product_price:
                try:
                    if float(product_price) < 0:
                        invalid_product_price += 1
                except ValueError:
                    invalid_product_price += 1

            if shipping_days:
                try:
                    if int(shipping_days) < 0:
                        invalid_shipping_days += 1
                except ValueError:
                    invalid_shipping_days += 1

            if not order_date:
                missing_order_dates += 1

            if not shipping_date:
                missing_shipping_dates += 1

            if shipping_mode:
                shipping_modes.add(shipping_mode)

    return {
        "invalid_late_delivery_risk": invalid_late_risk,
        "invalid_quantities": invalid_quantity,
        "invalid_product_prices": invalid_product_price,
        "invalid_shipping_days": invalid_shipping_days,
        "missing_order_dates": missing_order_dates,
        "missing_shipping_dates": missing_shipping_dates,
        "shipping_modes": sorted(shipping_modes),
    }


def main():
    main_file = RAW_DIR / "DataCoSupplyChainDataset.csv"

    schema_result = validate_schema(main_file)

    if not schema_result["passed"]:
        print("Schema validation: FAILED")
        return

    print("Schema validation: PASSED")

    row_result = validate_rows(main_file)
    business_result = validate_business_rules(main_file)

    report = {
        "file": main_file.name,
        "schema_validation": schema_result,
        "row_validation": row_result,
        "business_rule_validation": business_result,
    }

    report["overall_status"] = "PASSED"

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_file = REPORT_DIR / "validation_report.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\nValidation report generated:")
    print(report_file)


if __name__ == "__main__":
    main()