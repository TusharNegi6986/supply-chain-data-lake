
from pathlib import Path
import hashlib
import json
from ..db import execute_query, fetch_one
from fastapi import APIRouter, File, HTTPException, UploadFile

from ..core.storage import (
    create_dataset_id,
    ensure_storage_directories,
    get_processed_dataset_dir,
    get_raw_dataset_dir,
    RAW_DIR,
    PROCESSED_DIR,
)

from ..services.profiler import (
    SUPPORTED_EXTENSIONS,
    load_dataset,
    profile_dataset,
)

from ..services.semantic_mapper import (
    map_dataset_semantics,
)


router = APIRouter(
    prefix="/api/datasets",
    tags=["Datasets"],
)

MAX_FILE_SIZE = 100 * 1024 * 1024


def calculate_file_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            sha256.update(chunk)

    return sha256.hexdigest()


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
):
    ensure_storage_directories()

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format. "
                "Please upload CSV, XLSX, or XLS."
            ),
        )

    dataset_id = create_dataset_id()

    raw_dir = get_raw_dataset_dir(dataset_id)
    processed_dir = get_processed_dataset_dir(dataset_id)

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename).name
    raw_path = raw_dir / safe_filename
    total_size = 0

    try:
        with raw_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    output.close()
                    raw_path.unlink(missing_ok=True)

                    raise HTTPException(
                        status_code=413,
                        detail="File exceeds the 100 MB upload limit.",
                    )

                output.write(chunk)

        if total_size == 0:
            raw_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty.",
            )

        file_hash = calculate_file_hash(raw_path)
        dataframe = load_dataset(raw_path)
        profile = profile_dataset(dataframe)
        semantic_mapping = map_dataset_semantics(dataframe)

        parquet_path = processed_dir / "data.parquet"

        dataframe.to_parquet(
            parquet_path,
            index=False,
            engine="pyarrow",
        )

        profile_data = profile if isinstance(profile, dict) else profile.to_dict()
        semantic_data = semantic_mapping

        execute_query(
            """
            INSERT INTO metadata.uploaded_datasets (
                dataset_id,
                filename,
                file_type,
                file_size_bytes,
                sha256,
                row_count,
                column_count,
                duplicate_rows,
                missing_values,
                completeness_percentage,
                semantic_mapping,
                raw_path,
                parquet_path,
                processing_status
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s::jsonb, %s, %s, %s
            )
            ON CONFLICT (dataset_id) DO NOTHING
            """,
            (
                dataset_id,
                safe_filename,
                extension.lstrip("."),
                total_size,
                file_hash,
                profile_data.get("rows"),
                profile_data.get("columns"),
                profile_data.get("duplicate_rows"),
                profile_data.get("total_missing_values"),
                profile_data.get("completeness_percentage"),
                json.dumps(semantic_data),
                str(raw_path),
                str(parquet_path),
                "completed",
            ),
        )

        return {
            "status": "success",
            "dataset_id": dataset_id,
            "filename": safe_filename,
            "file_type": extension.replace(".", ""),
            "file_size_bytes": total_size,
            "sha256": file_hash,
            "raw_path": str(
                raw_path.relative_to(raw_dir.parent.parent)
            ),
            "parquet_path": str(
                parquet_path.relative_to(processed_dir.parent.parent)
            ),
            "profile": profile,
            "semantic_mapping": semantic_mapping,
        }

    except HTTPException:
        raw_path.unlink(missing_ok=True)
        parquet_path = processed_dir / "data.parquet"
        parquet_path.unlink(missing_ok=True)
        raise

    except Exception as exc:
        raw_path.unlink(missing_ok=True)
        parquet_path = processed_dir / "data.parquet"
        parquet_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Dataset processing failed: {str(exc)}",
        ) from exc

    finally:
        await file.close()


@router.get("")
def list_datasets():
    """List datasets whose raw files and processed output exist."""
    ensure_storage_directories()

    datasets = []

    for raw_dir in RAW_DIR.iterdir():
        if not raw_dir.is_dir() or not raw_dir.name.startswith("ds_"):
            continue

        processed_dir = PROCESSED_DIR / raw_dir.name
        raw_files = [
            path for path in raw_dir.iterdir() if path.is_file()
        ]

        if not raw_files:
            continue

        for raw_file in raw_files:
            parquet_file = processed_dir / "data.parquet"

            datasets.append({
                "dataset_id": raw_dir.name,
                "filename": raw_file.name,
                "file_type": raw_file.suffix.lower().lstrip("."),
                "file_size_bytes": raw_file.stat().st_size,
                "processed": parquet_file.is_file(),
            })

    datasets.sort(key=lambda item: item["dataset_id"], reverse=True)

    return {
        "total": len(datasets),
        "datasets": datasets,
    }


@router.get("/{dataset_id}")
def get_dataset_details(dataset_id: str):
    dataset = fetch_one(
        """
        SELECT
            dataset_id,
            filename,
            file_type,
            file_size_bytes,
            sha256,
            row_count,
            column_count,
            duplicate_rows,
            missing_values,
            completeness_percentage,
            semantic_mapping,
            raw_path,
            parquet_path,
            processing_status,
            uploaded_at
        FROM metadata.uploaded_datasets
        WHERE dataset_id = %s
        """,
        (dataset_id,),
    )

    # Use stored metadata whenever it exists.
    if dataset is not None:
        return {
            "status": "success",
            "dataset": dataset,
        }

    # Fall back to the existing files when metadata is missing.
    raw_dir = RAW_DIR / dataset_id
    processed_dir = PROCESSED_DIR / dataset_id

    if (
        not dataset_id.startswith("ds_")
        or not raw_dir.is_dir()
        or not processed_dir.is_dir()
    ):
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    raw_files = [
        path for path in raw_dir.iterdir() if path.is_file()
    ]
    parquet_path = processed_dir / "data.parquet"

    if not raw_files or not parquet_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Dataset files not found",
        )

    raw_path = raw_files[0]

    try:
        dataframe = load_dataset(raw_path)
        profile = profile_dataset(dataframe)
        semantic_mapping = map_dataset_semantics(dataframe)

        return {
            "status": "success",
            "dataset": {
                "dataset_id": dataset_id,
                "filename": raw_path.name,
                "file_type": raw_path.suffix.lower().lstrip("."),
                "file_size_bytes": raw_path.stat().st_size,
                "sha256": calculate_file_hash(raw_path),
                "row_count": profile.get("rows"),
                "column_count": profile.get("columns"),
                "duplicate_rows": profile.get("duplicate_rows"),
                "missing_values": profile.get("total_missing_values"),
                "completeness_percentage": profile.get(
                    "completeness_percentage"
                ),
                "semantic_mapping": semantic_mapping,
                "raw_path": str(raw_path),
                "parquet_path": str(parquet_path),
                "processing_status": "completed",
                "uploaded_at": None,
            },
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not load dataset details: {str(exc)}",
        ) from exc
