import re

import pandas as pd


SEMANTIC_RULES = {
    "identifier": [
        "id",
        "code",
        "number",
        "no",
        "key",
    ],
    "customer": [
        "customer",
        "client",
        "buyer",
        "user",
    ],
    "product": [
        "product",
        "item",
        "sku",
        "stock",
    ],
    "date": [
        "date",
        "time",
        "timestamp",
    ],
    "revenue": [
        "sales",
        "revenue",
        "amount",
        "income",
        "turnover",
    ],
    "quantity": [
        "quantity",
        "qty",
        "units",
        "volume",
    ],
    "price": [
        "price",
        "unit_price",
        "selling_price",
        "cost",
    ],
    "country": [
        "country",
        "nation",
    ],
    "state": [
        "state",
        "province",
        "region",
    ],
    "city": [
        "city",
        "town",
    ],
    "category": [
        "category",
        "type",
        "class",
        "segment",
    ],
}


def normalize_column_name(column_name: str) -> str:
    name = str(column_name).strip().lower()

    name = re.sub(
        r"[^a-z0-9]+",
        "_",
        name,
    )

    return name.strip("_")


def detect_semantic_type(
    column_name: str,
    series: pd.Series,
) -> str:

    normalized_name = normalize_column_name(column_name)

    # Date detection
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    # Check whether the column name strongly indicates a date
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["date"]
    ):
        return "date"

    # Identifier detection
    if (
        normalized_name.endswith("_id")
        or normalized_name == "id"
        or normalized_name.endswith("_code")
        or normalized_name.endswith("_key")
    ):
        if "customer" in normalized_name:
            return "customer_identifier"

        if "product" in normalized_name:
            return "product_identifier"

        if "order" in normalized_name:
            return "order_identifier"

        return "identifier"

    # Customer detection
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["customer"]
    ):
        return "customer"

    # Product detection
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["product"]
    ):
        return "product"

    # Revenue detection
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["revenue"]
    ):
        if pd.api.types.is_numeric_dtype(series):
            return "revenue"

    # Quantity detection
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["quantity"]
    ):
        if pd.api.types.is_numeric_dtype(series):
            return "quantity"

    # Price detection
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["price"]
    ):
        if pd.api.types.is_numeric_dtype(series):
            return "price"

    # Geographic fields
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["country"]
    ):
        return "country"

    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["state"]
    ):
        return "state"

    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["city"]
    ):
        return "city"

    # Category-like columns
    if any(
        keyword in normalized_name
        for keyword in SEMANTIC_RULES["category"]
    ):
        return "category"

    # Generic fallback based on detected data type
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    if series.nunique(dropna=True) <= min(
        50,
        max(10, len(series) * 0.05),
    ):
        return "categorical"

    return "text"


def map_dataset_semantics(
    dataframe: pd.DataFrame,
) -> list[dict]:

    mappings = []

    for column in dataframe.columns:
        series = dataframe[column]

        mappings.append(
            {
                "column_name": str(column),
                "normalized_name": normalize_column_name(
                    column
                ),
                "semantic_type": detect_semantic_type(
                    column,
                    series,
                ),
                "data_type": str(series.dtype),
                "unique_count": int(
                    series.nunique(dropna=True)
                ),
                "confidence": "high",
            }
        )

    return mappings