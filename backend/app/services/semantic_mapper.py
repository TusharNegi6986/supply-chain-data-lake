
import re

import pandas as pd


SEMANTIC_RULES = {
    "identifier": ["id", "code", "number", "no", "key"],
    "customer": ["customer", "client", "buyer", "user"],
    "product": ["product", "item", "sku", "stock"],
    "date": ["date", "time", "timestamp"],
    "revenue": ["sales", "revenue", "amount", "income", "turnover"],
    "quantity": ["quantity", "qty", "units", "volume"],
    "price": ["price", "unit_price", "selling_price"],
    "cost": ["cost", "expense", "expenditure"],
    "country": ["country", "nation"],
    "state": ["state", "province", "region"],
    "city": ["city", "town"],
    "category": ["category", "type", "class", "segment"],
    "employee": ["employee", "staff", "worker"],
    "salary": ["salary", "wage", "pay"],
    "email": ["email", "email_address"],
    "rating": ["rating", "score", "review"],
}


def normalize_column_name(column_name: str) -> str:
    name = str(column_name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def _name_tokens(column_name: str) -> set[str]:
    return set(normalize_column_name(column_name).split("_"))


def detect_semantic_type(
    column_name: str,
    series: pd.Series,
) -> str:
    name = normalize_column_name(column_name)
    tokens = _name_tokens(column_name)

    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    if tokens.intersection({"date", "time", "timestamp"}):
        return "date"

    if (
        name == "id"
        or name.endswith(("_id", "_code", "_key"))
    ):
        if "customer" in tokens:
            return "customer_identifier"
        if "product" in tokens:
            return "product_identifier"
        if "order" in tokens:
            return "order_identifier"
        return "identifier"

    # More specific semantic matches take precedence.
    for semantic_type in (
        "email", "employee", "salary", "rating",
        "customer", "product", "country", "state",
        "city", "revenue", "quantity", "price", "cost",
        "category",
    ):
        keywords = SEMANTIC_RULES[semantic_type]

        if any(
            keyword in tokens
            for keyword in keywords
        ):
            if semantic_type in {
                "revenue", "quantity", "price", "cost", "salary", "rating"
            } and not pd.api.types.is_numeric_dtype(series):
                continue

            return semantic_type

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    non_null = series.dropna()
    if not non_null.empty:
        parsed_dates = pd.to_datetime(
            non_null.astype(str),
            errors="coerce",
            format="mixed",
        )
        if parsed_dates.notna().mean() >= 0.9:
            return "date"

    unique_count = series.nunique(dropna=True)
    if unique_count <= min(50, max(10, len(series) * 0.05)):
        return "categorical"

    return "text"


def _confidence_for(
    column_name: str,
    series: pd.Series,
    semantic_type: str,
) -> str:
    name = normalize_column_name(column_name)
    tokens = _name_tokens(column_name)

    if semantic_type == "date" and (
        pd.api.types.is_datetime64_any_dtype(series)
        or tokens.intersection({"date", "time", "timestamp"})
    ):
        return "high"

    if semantic_type in {
        "identifier", "customer_identifier",
        "product_identifier", "order_identifier",
    } and (
        name == "id" or name.endswith(("_id", "_code", "_key"))
    ):
        return "high"

    for rule_type, keywords in SEMANTIC_RULES.items():
        if semantic_type == rule_type and tokens.intersection(
            set(keywords)
        ):
            return "medium"

    return "low"


def map_dataset_semantics(
    dataframe: pd.DataFrame,
) -> list[dict]:
    mappings = []

    for column in dataframe.columns:
        series = dataframe[column]
        semantic_type = detect_semantic_type(column, series)

        mappings.append({
            "column_name": str(column),
            "normalized_name": normalize_column_name(column),
            "semantic_type": semantic_type,
            "data_type": str(series.dtype),
            "unique_count": int(series.nunique(dropna=True)),
            "confidence": _confidence_for(
                column, series, semantic_type
            ),
        })

    return mappings
