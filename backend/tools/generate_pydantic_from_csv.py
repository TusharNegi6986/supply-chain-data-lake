# backend/tools/generate_pydantic_from_csv.py
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime

TYPE_MAP = {
    "int64": "int",
    "float64": "float",
    "bool": "bool",
    "datetime64[ns]": "datetime.datetime",
    "object": "str"
}

def infer_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "int"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime.datetime"
    return "str"

def sanitize_name(name: str) -> str:
    # simple sanitization: replace spaces and illegal chars with _
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name).lower()

def generate_model(csv_path: Path, class_name: str = "OrderRecord", rows_to_read: int = 200):
    df = pd.read_csv(csv_path, nrows=rows_to_read)
    # optional: convert columns with parseable dates
    for col in df.columns:
        try:
            parsed = pd.to_datetime(df[col], errors="coerce")
            # if more than 50% non-na after parse, treat as datetime
            if parsed.notna().sum() > len(parsed) * 0.5:
                df[col] = parsed
        except Exception:
            pass

    lines = []
    imports = {"from pydantic import BaseModel"}
    needs_datetime = False
    lines.append(f"class {class_name}(BaseModel):")

    for col in df.columns:
        pyname = sanitize_name(col)
        # ensure field name is a valid python identifier
        if pyname[0].isdigit():
            pyname = "_" + pyname
        dtype = infer_type(df[col])
        if dtype == "datetime.datetime":
            needs_datetime = True
        lines.append(f"    {pyname}: {dtype} | None = None")

    header = ["# Auto-generated Pydantic models from CSV", "from typing import Optional"]
    if needs_datetime:
        header.append("import datetime")
    header.extend(sorted(list(imports)))
    header_text = "\n".join(header) + "\n\n\n"
    content = header_text + "\n".join(lines) + "\n"
    return content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", "-c", required=True, help="Path to CSV file")
    parser.add_argument("--out", "-o", required=True, help="Output .py file for models")
    parser.add_argument("--class-name", default="OrderRecord", help="Pydantic class name")
    args = parser.parse_args()
    csv_path = Path(args.csv).expanduser()
    out_path = Path(args.out).expanduser()
    content = generate_model(csv_path, args.class_name)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf8")
    print(f"Wrote model to {out_path}")

if __name__ == "__main__":
    main()