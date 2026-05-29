__all__ = [
    'random_string',
    'str_now',
    'fmt_tm',
    'no_ansi',
    'cl',
]


import random
import string
from datetime import datetime
from typing import LiteralString

from .config import ANSI_ESCAPE


def random_string(string_len: int = 6) -> str:
    """
    Generates a string of random characters and numbers.
    :param string_len: string length
    :return: generated string
    """
    letters_digits: LiteralString = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for _ in range(string_len))


def str_now(fmt: str = '%Y%m%d_%H%M%S') -> str:
    """
    Returns the current date and time as a string in a default format.
    """
    return datetime.now().strftime(fmt)


def fmt_tm(secs_init: int) -> str:
    """
    Receives an integer representing seconds and returns a string
    formatted as hh:mm:ss.
    :param secs_init: int -> total seconds
    :return: str -> hh:mm:ss
    """
    secs: int = secs_init % 60
    mins_tmp: int = secs_init // 60
    mins: int = mins_tmp % 60
    hrs: int = mins_tmp // 60

    return f'{hrs:02d}:{mins:02d}:{secs:02d}'


def no_ansi(st):
    """
    Removes ANSI characters from a string. Useful when the same string
    intended for colored console output is going to be saved to a text file.
    :param st: string to clean
    :return: clean string
    """
    return ANSI_ESCAPE.sub('', st)


class Cl:
    """
    Class to style strings with colors in the terminal.
    Selected colors look good on konsole, regardless of bold settings.
    """

    # Colors
    red = '\033[31m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'

    # Colors with integrated bold
    bred = '\033[1m\033[31m'
    bgreen = '\033[1m\033[92m'
    byellow = '\033[1m\033[93m'
    bblue = '\033[1m\033[94m'

    # Styles
    bold = '\033[1m'
    underline = '\033[4m'

    # End color or style
    endc = '\033[0m'


# Ready to be imported
cl = Cl()
