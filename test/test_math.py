from decimal import Decimal

import pytest

from py_utils.math import div_prec, precise_round, qseconds


def test_precise_round() -> None:
    res = precise_round(1.2345, 2)
    assert res == Decimal("1.23")
    
    res_up = precise_round(1.235, 2)
    assert res_up == Decimal("1.24")


def test_qseconds_valid() -> None:
    assert qseconds("45") == 45
    assert qseconds("01:30") == 90
    assert qseconds("01:01:01") == 3661


def test_qseconds_invalid() -> None:
    with pytest.raises(ValueError):
        qseconds("01:01:01:01")
    
    with pytest.raises(ValueError):
        qseconds("90:00")


def test_div_prec() -> None:
    # Verifies localcontext applies correctly for precision limits
    res = div_prec(10, 3, precision=2)
    assert res == Decimal("3.33")
    
    res_exact = div_prec("1", "2", precision=4)
    assert res_exact == Decimal("0.5000")