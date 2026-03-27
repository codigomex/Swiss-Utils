from datetime import datetime
import random
import string
from typing import LiteralString


def random_string(string_len: int=6) -> str:
    """
    Genera un string de caracteres y números aleatorios
    :param string_len: longitud del string
    :return: string generado
    """
    letters_digits: LiteralString = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits)
                   for _ in range(string_len))


def str_now(fmt: str='%Y%m%d_%H%M%S') -> str:
    """
    Devuelve fecha y hora en str en un formato predeterminado.
    """
    return datetime.now().strftime(fmt)


def fmt_tm(secs_init: int) -> str:
    """
    Recibe un entero que representa un número de segundos, y se regresa
    un str en formato hh:mm:ss
    :param secs_init: int -> segundos
    :return: str -> hh:mm:ss
    """
    secs: int = secs_init % 60
    mins_tmp: int = secs_init // 60
    mins: int = mins_tmp % 60
    hrs: int = mins_tmp // 60

    return f"{hrs:02:d}:{mins:02d}:{secs:02d}"




