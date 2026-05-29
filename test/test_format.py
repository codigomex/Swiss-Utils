import re

from py_utils.format import fmt_tm, no_ansi, random_string, str_now


def test_random_string_length() -> None:
    res = random_string(10)
    assert len(res) == 10
    assert res.isalnum()


def test_str_now() -> None:
    # Basic check to ensure it returns digits and underscores
    res = str_now()
    assert re.match(r'^\d{8}_\d{6}$', res)


def test_fmt_tm() -> None:
    assert fmt_tm(0) == '00:00:00'
    assert fmt_tm(65) == '00:01:05'
    assert fmt_tm(3665) == '01:01:05'


def test_no_ansi() -> None:
    text_with_ansi = '\033[92mSuccess\033[0m'
    clean_text = no_ansi(text_with_ansi)
    assert clean_text == 'Success'
