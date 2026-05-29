__all__ = [
    'comp_dicts',
    'show_data',
    'octa_uuid',
]


import secrets
from pprint import pformat
from typing import Any

from .system import show_tmp


def octa_uuid(fmt: bool = True, compare: list[str] | None = None) -> str:
    """
    Generates an 8-character hexadecimal identifier.
    Example: 'A1B2-C3D4' or 'A1B2C3D4'
    """
    while True:
        token = secrets.token_hex(4).upper()
        ret = f'{token[:4]}-{token[4:]}' if fmt else token
        if compare:
            if ret not in compare:
                return ret
        else:
            return ret


def comp_dicts(new: dict[Any, Any], old: dict[Any, Any]) -> tuple[bool, list[str]]:
    """
    Compares 2 dictionaries, checks for new fields, and presents differences.
    :param new: "new" dictionary
    :param old: "old" dictionary
    :return: bool indicating equality + possible list of differences
    """
    if new == old:
        return True, []

    diffs: list[str] = []
    k_new, k_old = set[Any](new), set[Any](old)

    # New and deleted fields
    for k in k_new - k_old:
        diffs.append(f'New Field: [{k}] = {new[k]}')

    for k in k_old - k_new:
        diffs.append(f'Deleted Field: [{k}] = {old[k]}')

    # Values that changed (intersection of keys)
    for k in k_new & k_old:
        if new[k] != old[k]:
            diffs.append(f'Field [{k}] changed from {old[k]} to {new[k]}')

    return False, diffs


def show_data(data: dict[str, object]) -> None:
    """
    Shows a pformat object that is a dict containing a key
    and an object/class as its value.
    :param data: object to display
    :return: None
    """
    ret: list[str] = []
    for k, v in data.items():
        # We use v.__dict__ directly as preferred
        ret.append(f'KEY {k}\n{pformat(v.__dict__, width=70)}\n')

    show_tmp('\n'.join(ret))
