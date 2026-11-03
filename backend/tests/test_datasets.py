
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


@patch("app.api.datasets.fetch_one", return_value=None)
@patch("app.api.datasets.load_dataset")
@patch("app.api.datasets.profile_dataset")
@patch("app.api.datasets.map_dataset_semantics")
@patch("app.api.datasets.calculate_file_hash", return_value="test-sha256")
@patch("app.api.datasets.RAW_DIR")
@patch("app.api.datasets.PROCESSED_DIR")
def test_dataset_details_uses_filesystem_fallback(
    mock_processed_root,
    mock_raw_root,
    mock_hash,
    mock_map,
    mock_profile,
    mock_load,
    mock_fetch_one,
    tmp_path,
):
    import pandas as pd

    dataset_id = "ds_fallback123"
    raw_dir = tmp_path / "raw" / dataset_id
    processed_dir = tmp_path / "processed" / dataset_id

    raw_dir.mkdir(parents=True)
    processed_dir.mkdir(parents=True)

    raw_file = raw_dir / "orders.csv"
    raw_file.write_text("order_id\n1\n2\n", encoding="utf-8")
    (processed_dir / "data.parquet").write_bytes(b"test parquet placeholder")

    mock_raw_root.__truediv__.return_value = raw_dir
    mock_processed_root.__truediv__.return_value = processed_dir

    dataframe = pd.DataFrame({"order_id": [1, 2]})
    mock_load.return_value = dataframe
    mock_profile.return_value = {
        "rows": 2,
        "columns": 1,
        "duplicate_rows": 0,
        "total_missing_values": 0,
        "completeness_percentage": 100,
    }
    mock_map.return_value = [{"column_name": "order_id"}]

    response = client.get(f"/api/datasets/{dataset_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["dataset"]["dataset_id"] == dataset_id
    assert body["dataset"]["filename"] == "orders.csv"
    assert body["dataset"]["row_count"] == 2
    assert body["dataset"]["sha256"] == "test-sha256"
    mock_fetch_one.assert_called_once()

def test_semantic_mapping_supports_unrelated_datasets():
    import pandas as pd
    from backend.app.services.semantic_mapper import map_dataset_semantics

    df = pd.DataFrame({
        "employee_name": ["Asha", "Ravi"],
        "salary": [40000, 50000],
        "email_address": ["asha@example.com", "ravi@example.com"],
        "performance_rating": [4.5, 3.8],
    })

    result = map_dataset_semantics(df)
    mapped = {item["column_name"]: item for item in result}

    assert len(result) == 4
    assert mapped["salary"]["semantic_type"] == "salary"
    assert mapped["employee_name"]["semantic_type"] == "employee"



@patch("app.api.datasets.RAW_DIR")
@patch("app.api.datasets.PROCESSED_DIR")
def test_list_datasets_returns_empty_list(
    mock_processed_root,
    mock_raw_root,
    tmp_path,
):
    mock_raw_root.__truediv__.return_value = tmp_path / "raw"
    mock_processed_root.__truediv__.return_value = tmp_path / "processed"

    (tmp_path / "raw").mkdir()
    (tmp_path / "processed").mkdir()

    response = client.get("/api/datasets")

    assert response.status_code == 200


def test_dataset_details_returns_404_for_missing_dataset():
    response = client.get("/api/datasets/ds_does_not_exist")

    assert response.status_code == 404


@patch("app.api.datasets.MAX_FILE_SIZE", 10)
def test_upload_rejects_file_over_size_limit(tmp_path):
    response = client.post(
        "/api/datasets/upload",
        files={
            "file": (
                "large.csv",
                b"01234567890",
                "text/csv",
            )
        },
    )

    assert response.status_code == 413
    assert response.json()["detail"] == (
        "File exceeds the 100 MB upload limit."
    )

@patch("app.api.datasets.ensure_storage_directories")
@patch("app.api.datasets.get_processed_dataset_dir")
@patch("app.api.datasets.get_raw_dataset_dir")
@patch("app.api.datasets.create_dataset_id", return_value="ds_empty123")
def test_upload_rejects_empty_file(
    mock_id,
    mock_raw_dir,
    mock_processed_dir,
    mock_ensure_dirs,
    tmp_path,
):
    raw_dir = tmp_path / "raw" / "ds_empty123"
    processed_dir = tmp_path / "processed" / "ds_empty123"

    mock_raw_dir.return_value = raw_dir
    mock_processed_dir.return_value = processed_dir

    response = client.post(
        "/api/datasets/upload",
        files={
            "file": ("empty.csv", b"", "text/csv"),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The uploaded file is empty."
    assert not (raw_dir / "empty.csv").exists()
