import numpy as np
from src.etl.main import store_raw
from tests.mock.mock_hapi import sample_mageis_raw
from unittest.mock import Mock
from datetime import datetime, timezone
from pathlib import Path



def test_store_to_npz_preserves_shape_and_values(tmp_path):

    mock_data = sample_mageis_raw()
    mock_logger = Mock()

    store_raw(
        mock_data,
        {"dir_path": str(tmp_path)},
        datetime(2013, 1, 1, tzinfo=timezone.utc),
        mock_logger
    )

    expected_out_path = Path(tmp_path, "2013", "01", "01.npz")
    assert expected_out_path.exists()

    stored = np.load(expected_out_path)
    restored_data = stored["data"]

    np.testing.assert_array_equal(actual=restored_data, desired=mock_data, verbose=True, strict=True)
