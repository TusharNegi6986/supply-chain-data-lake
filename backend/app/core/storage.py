from pathlib import Path
import uuid


BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = BASE_DIR / "storage"

RAW_DIR = STORAGE_DIR / "raw"
PROCESSED_DIR = STORAGE_DIR / "processed"
QUARANTINE_DIR = STORAGE_DIR / "quarantine"


def ensure_storage_directories():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)


def create_dataset_id() -> str:
    return f"ds_{uuid.uuid4().hex[:12]}"


def get_raw_dataset_dir(dataset_id: str) -> Path:
    return RAW_DIR / dataset_id


def get_processed_dataset_dir(dataset_id: str) -> Path:
    return PROCESSED_DIR / dataset_id


def get_quarantine_dataset_dir(dataset_id: str) -> Path:
    return QUARANTINE_DIR / dataset_id