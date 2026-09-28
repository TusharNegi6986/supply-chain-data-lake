COLUMN_TO_MODEL = {
    "id": "order_id",
    "rowid": "order_id",
    "customer": "customer_name",
    "customer_name": "customer_name",
    "order_date": "order_date",
    "amount": "amount",
    # add more as needed
}

def map_columns_to_model(d: dict) -> dict:
    mapped = {}
    for k, v in d.items():
        nk = COLUMN_TO_MODEL.get(k, k)   # default: keep same
        mapped[nk] = v
    return mapped