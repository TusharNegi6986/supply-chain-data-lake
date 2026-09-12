import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PIPELINE_DIR = PROJECT_ROOT / "pipeline"
REPORT_DIR = PIPELINE_DIR / "reports"
LOG_FILE = REPORT_DIR / "pipeline_log.txt"


STEPS = [
    ("Data validation", PIPELINE_DIR / "ingest.py"),
    ("Data processing", PIPELINE_DIR / "process.py"),
    ("Database loading", PIPELINE_DIR / "load.py"),
    ("Staging refresh", PIPELINE_DIR / "refresh_staging.py"),
    ("Fact table refresh", PIPELINE_DIR / "refresh_fact.py"),
    ("Data quality verification", PIPELINE_DIR / "verify_pipeline.py"),
]


def write_log(message):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(message + "\n")


def run_step(name, script):
    print("\n" + "=" * 60)
    print(f"STARTING: {name}")
    print("=" * 60)

    start_time = time.time()

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_ROOT
    )

    duration = time.time() - start_time

    if result.returncode != 0:
        message = (
            f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
            f"{name} | FAILED | {duration:.2f}s"
        )

        write_log(message)

        print(f"\nFAILED: {name}")
        sys.exit(result.returncode)

    message = (
        f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
        f"{name} | PASSED | {duration:.2f}s"
    )

    write_log(message)

    print(f"\nPASSED: {name}")
    print(f"Duration: {duration:.2f} seconds")


def main():
    start_time = time.time()

    print("=" * 60)
    print("SUPPLY CHAIN DATA PIPELINE")
    print("=" * 60)

    write_log("")
    write_log("=" * 60)
    write_log(
        f"PIPELINE RUN STARTED | "
        f"{datetime.now():%Y-%m-%d %H:%M:%S}"
    )
    write_log("=" * 60)

    for name, script in STEPS:
        run_step(name, script)

    total_duration = time.time() - start_time

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Total duration: {total_duration:.2f} seconds")

    write_log(
        f"PIPELINE COMPLETED SUCCESSFULLY | "
        f"{total_duration:.2f}s"
    )
    write_log("=" * 60)


if __name__ == "__main__":
    main()