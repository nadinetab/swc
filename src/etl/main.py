import json
import logging
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

import numpy as np
import yaml
from hapiclient import hapi


def setup_logger() -> logging.Logger:
    now = datetime.now(UTC).timestamp()
    logs_file_path = Path(Path.cwd(), "logs", f"{int(now)}.app.log")
    logs_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=logs_file_path,
        encoding="utf-8",
        format="{asctime} : {levelname} : {message}",
        style="{",
        level=logging.INFO,
    )

    return logging.getLogger(__name__)


def store_raw(
    data: np.ndarray, config: dict, start_dt: datetime, logger: logging.Logger
) -> None:
    """Store incoming Numpy array as binary .npz file, binned by spacecraft/instrument/year/month/day."""

    file_path = Path(
        config["dir_path"],
        start_dt.strftime("%Y"),
        start_dt.strftime("%m"),
        f"{start_dt.strftime('%d')}.npz",
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        np.savez_compressed(file=file_path, data=data)
    except Exception:
        logger.exception(f"Error writing data to file: {file_path}")
        raise

    logger.info(f"Wrote data to file: {file_path}")


def store_meta(
    data: dict, config: dict, start_dt: datetime, logger: logging.Logger
) -> None:
    """Store corresponding metadata as json files, binned by spacecraft/instrument/year/month/day."""

    file_path = Path(
        config["metadata_path"],
        start_dt.strftime("%Y"),
        start_dt.strftime("%m"),
        f"{start_dt.strftime('%d')}.json",
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as metafile:
        try:
            json.dump(data, metafile)
        except Exception:
            logger.exception(f"Error writing metadata to file {file_path}")
            raise

    logger.info(f"Wrote metadata to file: {file_path}")


def time_chunks(start: str, stop: str) -> Iterator[tuple[datetime, datetime]]:
    """Parse a given time window (incoming ISO-8601 string format) into 1d chunks."""

    start_dt = datetime.fromisoformat(start)
    stop_dt = datetime.fromisoformat(stop)

    # TODO - unit test
    cur_dt = start_dt
    while cur_dt < stop_dt:
        plus_one = cur_dt + timedelta(days=1)
        yield cur_dt, plus_one
        cur_dt = plus_one


def extract_and_load(config: dict, logger: logging.Logger) -> None:

    for p in config["data_products"]:
        extraction_config = p["extraction"]

        logger.info(
            f"Starting extraction for `{p['id']}` between {extraction_config['start']} and {extraction_config['stop']}"
        )

        # Batch in 1d chunks
        for start, stop in time_chunks(
            extraction_config["start"], extraction_config["stop"]
        ):
            # TODO - error handling
            data, meta = hapi(
                extraction_config["server"],
                p["id"],
                extraction_config["parameters"],
                datetime.isoformat(start),
                datetime.isoformat(stop),
            )

            store_raw(data, p["storage"], start, logger)
            store_meta(meta, p["storage"], start, logger)


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    logger = setup_logger()

    extract_and_load(config, logger)
