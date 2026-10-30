from pathlib import Path
import hashlib

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..core.storage import (
    create_dataset_id,
    ensure_storage_directories,
    get_processed_dataset_dir,
    get_raw_dataset_dir,
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
    file: UploadFile = File(...)
):
    ensure_storage_directories()

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

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
    processed_dir = get_processed_dataset_dir(
        dataset_id
    )

    raw_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_filename = Path(
        file.filename
    ).name

    raw_path = raw_dir / safe_filename

    total_size = 0

    try:
        with raw_path.open("wb") as output:

            while chunk := await file.read(
                1024 * 1024
            ):
                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    output.close()

                    raw_path.unlink(
                        missing_ok=True
                    )

                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "File exceeds the "
                            "100 MB upload limit."
                        ),
                    )

                output.write(chunk)

        file_hash = calculate_file_hash(
            raw_path
        )

        dataframe = load_dataset(
            raw_path
        )

        profile = profile_dataset(
            dataframe
        )

        semantic_mapping = map_dataset_semantics(
            dataframe
        )

        parquet_path = (
            processed_dir / "data.parquet"
        )

        dataframe.to_parquet(
            parquet_path,
            index=False,
            engine="pyarrow",
        )

        return {
            "status": "success",
            "dataset_id": dataset_id,
            "filename": safe_filename,
            "file_type": extension.replace(
                ".",
                "",
            ),
            "file_size_bytes": total_size,
            "sha256": file_hash,
            "raw_path": str(
                raw_path.relative_to(
                    raw_dir.parent.parent
                )
            ),
            "parquet_path": str(
                parquet_path.relative_to(
                    processed_dir.parent.parent
                )
            ),
            "profile": profile,
            "semantic_mapping": semantic_mapping,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raw_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Dataset processing failed: "
                f"{str(exc)}"
            ),
        ) from exc