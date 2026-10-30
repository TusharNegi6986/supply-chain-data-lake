
import sys
from pathlib import Path
from unittest.mock import patch

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_rejects_unsupported_extension():
    response = client.post(
        "/api/datasets/upload",
        files={
            "file": (
                "malware.exe",
                b"not a real executable",
                "application/octet-stream",
            )
        },
    )

    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]


@patch("app.api.datasets.map_dataset_semantics")
@patch("app.api.datasets.profile_dataset")
@patch("app.api.datasets.load_dataset")
@patch("app.api.datasets.calculate_file_hash")
@patch("app.api.datasets.ensure_storage_directories")
@patch("app.api.datasets.get_processed_dataset_dir")
@patch("app.api.datasets.get_raw_dataset_dir")
@patch("app.api.datasets.create_dataset_id", return_value="ds_test123")
def test_upload_valid_csv(
    mock_id,
    mock_raw_dir,
    mock_processed_dir,
    mock_ensure_dirs,
    mock_hash,
    mock_load,
    mock_profile,
    mock_map,
    tmp_path,
):
    import pandas as pd

    raw_dir = tmp_path / "raw" / "ds_test123"
    processed_dir = tmp_path / "processed" / "ds_test123"

    mock_raw_dir.return_value = raw_dir
    mock_processed_dir.return_value = processed_dir
    mock_hash.return_value = "test-sha256"

    dataframe = pd.DataFrame({"order_id": [1, 2]})
    mock_load.return_value = dataframe
    mock_profile.return_value = {"rows": 2}
    mock_map.return_value = {"order_id": "Order ID"}

    with patch.object(
        dataframe,
        "to_parquet",
    ) as mock_to_parquet:
        response = client.post(
            "/api/datasets/upload",
            files={
                "file": (
                    "orders.csv",
                    b"order_id\n1\n2\n",
                    "text/csv",
                )
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["dataset_id"] == "ds_test123"
    assert body["filename"] == "orders.csv"
    assert body["profile"] == {"rows": 2}
    assert body["semantic_mapping"] == {"order_id": "Order ID"}
    mock_to_parquet.assert_called_once()
    mock_load.assert_called_once()
