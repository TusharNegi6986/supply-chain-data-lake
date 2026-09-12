import csv
from pathlib import Path

from db import get_connection


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_FILE = (
    PROJECT_ROOT
    / "datalake"
    / "processed"
    / "DataCoSupplyChainDataset_processed.csv"
)

TARGET_TABLE = "staging.orders_processed"


def load_processed_data():
    conn = get_connection()

    try:
        with open(
            PROCESSED_FILE,
            "r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.reader(file)
            columns = next(reader)

            column_list = ", ".join(
                f'"{column}"'
                for column in columns
            )

            with conn.cursor() as cursor:

                cursor.execute(
                    f"TRUNCATE TABLE {TARGET_TABLE};"
                )

                cursor.copy_expert(
                    f"""
                    COPY {TARGET_TABLE} ({column_list})
                    FROM STDIN
                    WITH (
                        FORMAT CSV,
                        HEADER FALSE,
                        DELIMITER ',',
                        QUOTE '"',
                        ESCAPE '"'
                    )
                    """,
                    file
                )

        conn.commit()

        print("Data loading completed.")
        print(f"Rows loaded into {TARGET_TABLE}")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    load_processed_data()