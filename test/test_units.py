from decimal import Decimal

from py_utils.units import (
    in_to_pt,
    mm_to_pt,
    pt_to_in,
    pt_to_mm,
    px_to_mm,
    px_to_pt,
)


def test_px_to_mm() -> None:
    # 300 px at 300 dpi = 1 inch = 25.4 mm
    res = px_to_mm(300, 300)
    assert res == Decimal("25.4")


def test_px_to_pt() -> None:
    # 300 px at 300 dpi = 1 inch = 72 pt
    res = px_to_pt(300, 300)
    assert res == Decimal("72")


def test_mm_to_pt() -> None:
    res = mm_to_pt(25)  # roughly 1 inch
    expected = Decimal("25") * Decimal("72") / Decimal("25.4")
    assert res == expected


def test_in_to_pt() -> None:
    assert in_to_pt(1) == Decimal("72")
    assert in_to_pt(2.5) == Decimal("180")


def test_pt_to_in() -> None:
    assert pt_to_in(Decimal("72")) == Decimal("1")


def test_pt_to_mm() -> None:
    # 72 pts = 1 inch = 25.4 mm
    res = pt_to_mm(Decimal("72"))
    assert res == Decimal("25.4")