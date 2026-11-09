from datetime import UTC, datetime

from src.etl.main import time_chunks


def test_final_tuple_doesnt_go_beyond_stop_date():
    sample_start = datetime(2026, 10, 24, 0, 0, 0, tzinfo=UTC)
    sample_stop = datetime(2026, 10, 26, 0, 0, 0, tzinfo=UTC)

    for dt_tuple in time_chunks(
        datetime.isoformat(sample_start), datetime.isoformat(sample_stop)
    ):
        assert dt_tuple[0] < sample_stop
        assert dt_tuple[1] <= sample_stop
