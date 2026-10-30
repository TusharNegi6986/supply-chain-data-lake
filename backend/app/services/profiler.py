from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
}


def load_dataset(file_path: Path) -> pd.DataFrame:
    extension = file_path.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(file_path)

    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)

    raise ValueError(
        f"Unsupported file format: {extension}. "
        f"Supported formats: CSV, XLSX, XLS."
    )


def detect_column_type(series: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    non_null = series.dropna()

    if len(non_null) > 0:
        sample = non_null.astype(str)

        parsed_dates = pd.to_datetime(
            sample,
            errors="coerce"
        )

        if parsed_dates.notna().mean() >= 0.9:
            return "datetime"

    unique_count = series.nunique(dropna=True)

    if unique_count <= min(50, max(10, len(series) * 0.05)):
        return "categorical"

    return "text"


def profile_column(series: pd.Series) -> dict:
    total_rows = len(series)
    null_count = int(series.isna().sum())

    profile = {
        "name": str(series.name),
        "dtype": str(series.dtype),
        "semantic_type": detect_column_type(series),
        "total_values": total_rows,
        "null_count": null_count,
        "null_percentage": round(
            (null_count / total_rows * 100)
            if total_rows
            else 0,
            2
        ),
        "unique_count": int(series.nunique(dropna=True)),
    }

    if pd.api.types.is_numeric_dtype(series):
        numeric_series = pd.to_numeric(
            series,
            errors="coerce"
        ).dropna()

        if not numeric_series.empty:
            profile.update(
                {
                    "min": float(numeric_series.min()),
                    "max": float(numeric_series.max()),
                    "mean": round(
                        float(numeric_series.mean()),
                        4
                    ),
                    "median": float(numeric_series.median()),
                }
            )

    else:
        non_null = series.dropna()

        if not non_null.empty:
            value_counts = (
                non_null
                .astype(str)
                .value_counts()
                .head(5)
            )

            profile["top_values"] = [
                {
                    "value": str(value),
                    "count": int(count),
                }
                for value, count in value_counts.items()
            ]

    return profile


def profile_dataset(df: pd.DataFrame) -> dict:
    rows = len(df)
    columns = len(df.columns)

    duplicate_rows = int(df.duplicated().sum())

    column_profiles = [
        profile_column(df[column])
        for column in df.columns
    ]

    total_cells = rows * columns
    total_nulls = int(df.isna().sum().sum())

    completeness = (
        ((total_cells - total_nulls) / total_cells) * 100
        if total_cells
        else 100
    )

    return {
        "rows": rows,
        "columns": columns,
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": round(
            (duplicate_rows / rows * 100)
            if rows
            else 0,
            2
        ),
        "total_missing_values": total_nulls,
        "completeness_percentage": round(
            completeness,
            2
        ),
        "column_profiles": column_profiles,
    }