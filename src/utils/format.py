import random
import string
from datetime import datetime
from typing import LiteralString

from .config import ANSI_ESCAPE


def random_string(string_len: int = 6) -> str:
    """
    Genera un string de caracteres y números aleatorios
    :param string_len: longitud del string
    :return: string generado
    """
    letters_digits: LiteralString = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for _ in range(string_len))


def str_now(fmt: str = '%Y%m%d_%H%M%S') -> str:
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

    return f'{hrs:02d}:{mins:02d}:{secs:02d}'


def no_ansi(st):
    """
    Usamos caracteres ANSI para los colores de la consola,
    pero si el mismo string se va a usar para mostrarse en archivo de texto hay que
    quitarlos (los caracteres ANSI se agregan con la clase CL)
    :param st: string a limpiar
    :return: string limpio
    """
    return ANSI_ESCAPE.sub('', st)


class Cl:
    """
    Clase para dar estilo con colores a strings, tomada de
    https://
    stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    Y ya de mi parte redefiní miembros, y tomé otros colores de:
    https://
    stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences/36045849
    Si notar que escoguí colores que se vieran bien en konsole, independientemente de si
    los colores están definidos como normales o brillantes.
    """

    # colores
    red = '\033[31m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    # colores con bold integrado
    bred = '\033[1m\033[31m'
    bgreen = '\033[1m\033[92m'
    byellow = '\033[1m\033[93m'
    bblue = '\033[1m\033[94m'
    # estilos
    bold = '\033[1m'
    underline = '\033[4m'
    # finalizar color o estilo
    endc = '\033[0m'

# Para ser importado
cl = Cl()
