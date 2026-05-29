from pathlib import Path
from unittest.mock import Mock, patch

from swiss_utils.system import tmp_fname


@patch('swiss_utils.system.TMP_DIR', Path('/fake/dir'))
@patch('swiss_utils.system.Path.exists', side_effect=[True, False])
def test_tmp_fname_collision(mock_exists) -> None:
    # Simulates first generated name exists, second does not
    # Also patches sleep to avoid delaying test execution
    with patch('swiss_utils.system.sleep', return_value=None):
        fname = tmp_fname('txt')

    assert fname.suffix == '.txt'
    assert fname.parent == Path('/fake/dir')
    assert mock_exists.call_count == 2
