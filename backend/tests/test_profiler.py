
import pandas as pd

from app.services.profiler import profile_dataset



def test_profile_dataset_calculates_data_quality_metrics():
    df = pd.DataFrame({
        "order_id": [1, 2, 2, 4],
        "status": ["Delivered", "Late", "Late", None],
    })

    result = profile_dataset(df)

    assert result["rows"] == 4
    assert result["columns"] == 2
    assert result["duplicate_rows"] == 1
    assert result["total_missing_values"] == 1
    assert result["completeness_percentage"] == 87.5
    assert result["duplicate_percentage"] == 25.0


def test_profile_dataset_handles_empty_dataframe():
    df = pd.DataFrame()

    result = profile_dataset(df)

    assert result["rows"] == 0
    assert result["columns"] == 0
    assert result["duplicate_rows"] == 0
    assert result["total_missing_values"] == 0
    assert result["completeness_percentage"] == 100
    assert result["duplicate_percentage"] == 0
