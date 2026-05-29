from py_utils.data import comp_dicts, octa_uuid


def test_octa_uuid_format() -> None:
    # Generates standard 8-char hex with hyphen
    uid = octa_uuid()
    assert len(uid) == 9
    assert "-" in uid


def test_octa_uuid_no_fmt() -> None:
    # Generates pure 8-char hex string
    uid = octa_uuid(fmt=False)
    assert len(uid) == 8
    assert "-" not in uid


def test_comp_dicts_equal() -> None:
    d1 = {"a": 1, "b": 2}
    d2 = {"a": 1, "b": 2}
    is_eq, diffs = comp_dicts(d1, d2)
    
    assert is_eq is True
    assert len(diffs) == 0


def test_comp_dicts_diff() -> None:
    new_d = {"a": 1, "b": 3, "c": 4}
    old_d = {"a": 1, "b": 2, "d": 5}
    is_eq, diffs = comp_dicts(new_d, old_d)
    
    assert is_eq is False
    assert any("New Field: [c]" in d for d in diffs)
    assert any("Deleted Field: [d]" in d for d in diffs)
    assert any("changed from 2 to 3" in d for d in diffs)