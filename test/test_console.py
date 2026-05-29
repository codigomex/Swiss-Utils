from unittest.mock import patch

import pytest

from swiss_utils.console import ask_verif, tobool


def test_tobool_valid() -> None:
    assert tobool('1') is True
    assert tobool('yes') is True
    assert tobool('0') is False
    assert tobool('no') is False


def test_tobool_invalid() -> None:
    with pytest.raises(Exception, match='is not recognized as a bool'):
        tobool('maybe')


@patch('builtins.input', side_effect=['invalid', 'y'])
def test_ask_verif(mock_input) -> None:
    # Simulates user entering bad input, then good input
    res = ask_verif('Confirm?', 'y', 'n')
    assert res == 'y'
    assert mock_input.call_count == 2
