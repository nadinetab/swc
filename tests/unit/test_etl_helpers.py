from src.etl.main import time_chunks
from datetime import datetime, timezone


def test_final_tuple_doesnt_go_beyond_stop_date():
    sample_start = datetime(2026, 10, 24, 0, 0, 0, tzinfo=timezone.utc)
    sample_stop = datetime(2026, 10, 26, 0, 0, 0, tzinfo=timezone.utc)

    for dt_tuple in time_chunks(datetime.isoformat(sample_start), datetime.isoformat(sample_stop)):
        assert dt_tuple[0] < sample_stop
        assert dt_tuple[1] <= sample_stop
