import csv
import json
import re
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_ROOT
    / "datalake"
    / "raw"
    / "DataCoSupplyChainDataset.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "datalake" / "processed"

PROCESSED_FILE = (
    PROCESSED_DIR
    / "DataCoSupplyChainDataset_processed.csv"
)

REPORT_DIR = PROJECT_ROOT / "pipeline" / "reports"

REPORT_FILE = REPORT_DIR / "processing_report.json"


COLUMN_RENAMES = {
    "order_date_dateorders": "order_date",
    "shipping_date_dateorders": "shipping_date",
}


INTEGER_COLUMNS = {
    "days_for_shipping_real",
    "days_for_shipment_scheduled",
    "late_delivery_risk",
    "category_id",
    "customer_id",
    "department_id",
    "order_customer_id",
    "order_id",
    "order_item_cardprod_id",
    "order_item_id",
    "order_item_quantity",
    "product_card_id",
    "product_category_id",
    "product_status",
}


DATE_COLUMNS = {
    "order_date",
    "shipping_date",
}


def clean_column_name(column):
    """Convert a raw column name to snake_case."""

    column = column.strip().lower()

    column = re.sub(
        r"[^a-z0-9]+",
        "_",
        column
    )

    return column.strip("_")


def convert_date(value):
    """Convert DataCo date format to ISO datetime format."""

    value = value.strip()

    if not value:
        return ""

    try:
        date_value = datetime.strptime(
            value,
            "%m/%d/%Y %H:%M"
        )

        return date_value.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:
        return value


def convert_value(column, value):
    """Standardize a single field."""

    value = value.strip()

    if column in DATE_COLUMNS:
        return convert_date(value)

    if column in INTEGER_COLUMNS and value:
        try:
            return str(int(float(value)))
        except ValueError:
            return value

    return value


def process_csv():
    """Create standardized processed CSV and quality report."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    missing_values = {}
    row_count = 0

    with open(
        RAW_FILE,
        "r",
        encoding="latin1",
        newline=""
    ) as input_file:

        reader = csv.reader(input_file)

        raw_headers = next(reader)

        cleaned_headers = [
            clean_column_name(column)
            for column in raw_headers
        ]

        final_headers = [
            COLUMN_RENAMES.get(
                column,
                column
            )
            for column in cleaned_headers
        ]

        missing_values = {
            column: 0
            for column in final_headers
        }

        with open(
            PROCESSED_FILE,
            "w",
            encoding="utf-8",
            newline=""
        ) as output_file:

            writer = csv.writer(output_file)

            writer.writerow(final_headers)

            for row in reader:

                processed_row = []

                for index, value in enumerate(row):

                    column = final_headers[index]

                    processed_value = convert_value(
                        column,
                        value
                    )

                    if not processed_value:
                        missing_values[column] += 1

                    processed_row.append(
                        processed_value
                    )

                writer.writerow(processed_row)

                row_count += 1

    missing_columns = {
        column: count
        for column, count in missing_values.items()
        if count > 0
    }

    report = {
        "file": PROCESSED_FILE.name,
        "processing_status": "PASSED",
        "rows_processed": row_count,
        "columns_processed": len(final_headers),
        "missing_values": missing_columns,
    }

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as report_file:

        json.dump(
            report,
            report_file,
            indent=4
        )

    print("Processing completed.")
    print(f"Rows processed : {row_count}")
    print(f"Columns        : {len(final_headers)}")
    print(f"Output file    : {PROCESSED_FILE}")

    print("\nMissing values:")

    if missing_columns:
        for column, count in missing_columns.items():
            print(f"{column}: {count}")
    else:
        print("None")

    print("\nProcessing report:")
    print(REPORT_FILE)


if __name__ == "__main__":
    process_csv()