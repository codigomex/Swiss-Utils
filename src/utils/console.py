import ctypes
import os
import textwrap
from datetime import datetime
from subprocess import run
from time import sleep
from typing import Literal

from .config import DT_FMT, SNG, STDOUT_WIDTH


def ask_valida(
    msje: str, *resps: str, sangria: str = SNG, nl_antes: int = 0, nl_despues: int = 0
) -> str:
    """
    Hace una pregunta y espera una respuesta en resps - la pregunta le da
    formato con parr, y para ello pedimos los mismos parámetros
    :param msje: pregunta
    :param resps: respuesas aceptadas
    :param sangria: intentado, por defaul el que usamos para op_yn
    :param nl_antes: nuevas lineas antes
    :param nl_despues: nuevas lineas después
    :return: bool indicando si/no
    """

    # Si hay mensaje, lo mostramos con formato
    if msje:
        pparr(msje, sangria, nl_antes, nl_despues)

    while True:
        # Usamos la sangría directamente en el prompt
        respuesta: str = input(f'{sangria}')

        if respuesta in resps:
            return respuesta

        # Si falla, avisamos cuáles son las opciones válidas
        opciones = '/'.join(resps)
        pparr(
            f'Respuesta inválida. Favor de elegir una de estas: [{opciones}]',
            indent=sangria,
        )


def clear() -> None:
    """
    Limpia la pantalla de comandos
    """
    command: Literal['cls', 'clear'] = 'cls' if os.name == 'nt' else 'clear'
    run(args=command, shell=True, check=False)


def window_title(title: str) -> None:
    """
    Cambia el título de la ventana para el cmd de windows
    :param title: título
    :return: nada
    """
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)  # type: ignore
    elif os.name == 'posix':
        print(f'\33]0;{title}\a', end='', flush=True)
    else:
        raise Exception(f'OS Desconocido: {os.name}!!!')


def pparr(
    msje: str,
    indent: str = SNG,
    nl_antes: int = 0,
    nl_despues: int = 0,
    width: int = STDOUT_WIDTH,
) -> None:
    """
    Wrapper para textwrap, para generar e imprimir a stdout un párrafo estandar
    con un indentado general.
    :param msje: texto a formatear
    :param indent: indentado
    :param nl_antes: nuevas lineas antes
    :param nl_despues: nuevas lineas después
    :param width: ancho del párrafo
    :return: nada
    """

    if not msje.strip():
        return

    indent_n: str = ' ' * len(indent)

    def format(tx: str, first: bool) -> str:
        ini = indent if first else indent_n
        rt = textwrap.fill(
            text=tx,
            initial_indent=ini,
            subsequent_indent=indent_n,
            width=width,
        )
        return rt

    lines: list[str] = msje.splitlines()
    
    wlines = [format(lines[0], True)]
    for l in lines[1:]:
        wlines.append(format(l, False))
    
    fmt = '\n'.join(wlines)

    print(f"{'\n' * nl_antes}{fmt}{'\n' * nl_despues}")


def op_yn(indent: str = SNG) -> bool:
    """
    Espera de un "input" una respuesta que tenga que ser el equivalente
    a un si/no.
    Se usa el indentado estandar y la función parr
    :return: bool indicando si/no
    """

    while True:
        resp: str = input(indent)
        if resp.lower() in ['s', 'si', 'yes', 'y', '1']:
            return True
        elif resp.lower() in ['n', 'no', 'n', 'noup', 'nel', 'false', '0']:
            return False
        else:
            pparr('Intruduzca una respuesta que signifique si/no!!!', indent)
            sleep(0.2)


def waiti(msg: str = '', sangria: str = SNG, nl_antes=0, nl_despues=0) -> None:
    """
    Wrapper de pparr.
    Presenta un input con una sangría y un mensaje vacío, sangría y mensaje se
    pueden cambiar desde donde se llame el def.
    Se usa principalmente para eso, presentar un input como una pausa que se elimina
    cuando el usuario presione enter.
    :param sangria: sangría
    :param msg: mensaje
    :return: nada
    """
    input(pparr(msje=msg, indent=sangria, nl_antes=nl_antes, nl_despues=nl_despues))


def tellme(sangria: str = SNG, msg: str = '') -> str:
    """
    Similar a waiti, pero regresa un str escrito por el usuario,
    no se valida que no sea un str vacío
    :param str sangria: sangria, defaults to SNG
    :param str msg: mensaje, defaults to ''
    :return str: respuesta del usuario
    """
    ret: str = input(f'{sangria}{msg}')
    return ret


def tobool(val: str) -> bool:
    """
    Recibe un valor y trata de interpretarlo como bool, desde que
    es para uso interno, mejor avisar con una excepción si el valor no
    se puede interpretar
    :param val: valor
    :return: el respectivo bool
    """
    if str(val).lower() in ['ok', 'si', 'true', 'verdadero', '1']:
        ret = True
    elif str(val).lower() in ['no', 'falso', 'false', '0']:
        ret = False
    else:
        raise Exception(f'No se reconoce el valor ({val}) como bool...')
    return ret


def ask_date(
    msje: str,
    fmt: str = DT_FMT,
    futuro: bool = False,
    indent: str = SNG,
    nl_antes: int = 0,
    nl_despues: int = 0,
) -> datetime:
    """
    Hace una pregunta y espera una fecha que, dependiendo de "futuro"
    puede o no ser mayor que la acutal - la pregunta le da
    formato con pparr, y para ello pedimos los mismos parámetros
    :param msje: pregunta
    :param fmt: formato esperado de la fecha
    :param futuro: bool indicando si la fecha puede ser mayor que la actual
    :param indent: intentado, por defaul el que usamos para op_yn
    :param nl_antes: nuevas lineas antes
    :param nl_despues: nuevas lineas después
    :return: bool indicando si/no
    """

    pparr(msje, indent, nl_antes, nl_despues)
    while True:
        respuesta: str = input(f'{indent}')
        try:
            ret: datetime = datetime.strptime(respuesta, fmt)
            if not futuro and ret > datetime.now():
                pparr(
                    'La fecha no puede ser mayor que la actual!, intente de nuevo',
                    indent=indent,
                )
            else:
                break
        except ValueError:
            pparr(f'Respuesta no reconocida, use el formato {fmt}', indent=indent)

    return ret


def ask_tipo(
    msje: str, tipo: type, indent: str = SNG, nl_antes: int = 0, nl_despues: int = 0
):
    """
    Hace una pregunta y espera una respuesta tipo "tipo" - la pregunta le da
    formato con parr, y para ello pedimos los mismos parámetros
    :param msje: pregunta
    :param tipo: tipo esperado de la respuesta
    :param indent: intentado, por defaul el que usamos para op_yn
    :param nl_antes: nuevas lineas antes
    :param nl_despues: nuevas lineas después
    :return: bool indicando si/no
    """

    pparr(msje, indent, nl_antes, nl_despues)

    while True:
        respuesta: str = input(f'{indent}')
        try:
            # Intentamos convertir directamente usando la clase pasada
            return tipo(respuesta)
        except ValueError:
            pparr(
                f'Error: Se esperaba un [{tipo.__name__}]. Intenta de nuevo.',
                indent=indent,
            )


def ask_varios(
    msje: str = '',
    *opciones: str,
    sep: str = ',',
    indent: str = SNG,
    nl_antes: int = 0,
    nl_despues: int = 0,
) -> list[str]:
    """
    Hace una pregunta y espera una o más respuesta en opciones - la pregunta le da
    formato con pparr, y para ello pedimos los mismos parámetros.
    El def es una modificación de ask_valida de este mismo módulo.
    :param msje: pregunta
    :param opciones: opciones o respuestas aceptadas
    :param sep: separador de respuestas
    :param indent: intentado, por defaul el que usamos para op_yn
    :param nl_antes: nuevas lineas antes
    :param nl_despues: nuevas lineas después
    :return: bool indicando si/no
    """

    if msje:
        pparr(msje, indent, nl_antes, nl_despues)

    while True:
        respuestas_usuario = input(f'{indent}').split(sep)
        # Limpiamos espacios accidentales en cada respuesta
        seleccion = [r.strip() for r in respuestas_usuario if r.strip()]

        # Verificamos si todas las selecciones son válidas
        if all(item in opciones for item in seleccion) and seleccion:
            return seleccion

        # Mensaje de error si algo falló
        pparr(
            f'Error. Ingrese solo opciones válidas separadas por "{sep}":',
            indent=indent,
        )
        print(f'{indent}{f" {sep} ".join(opciones)}')
        pparr('Evite espacios adicionales entre el separador.', indent=indent)


def ask_unico(*ops: str, q: str = '¿Cuál es su Selección?', nlines_ops: bool = False):
    """
    Presenta una lista de opciones (*ops) y devuelve la opción escogida
    :param q: pregunta
    :param ops: lista de opciones
    :param nlines_ops: si true, agrega un newline entre opción y opción
    :return: opción escogida
    """

    # Calculamos el ancho del número para que todos queden alineados
    ancho: int = len(str(len(ops)))

    print(f'\n{SNG}{q}\n')

    for i, op in enumerate(ops, 1):
        # f-string con padding dinámico: :>{ancho}
        print(f'  ({i:>{ancho}}) {op}')
        if nlines_ops:
            print()

    # Validamos que la entrada esté entre 1 y el total de opciones
    # Nota: Asumo que ask_valida acepta strings de los números válidos
    opciones_validas = [str(i) for i in range(1, len(ops) + 1)]
    num = ask_valida('', *opciones_validas)

    return ops[int(num) - 1]


def ask_date_fmt_iso8601(
    q: str = 'Ingrese una fecha en formato YYYYY-MM-DD:', fmt: str = '%Y-%m-%d'
):
    """
    Pide se ingrese una fecha en formato iso 8601, o en el que se indique en fmt
    :param q: pregunta
    :param fmt: formato de la fecha
    :return: st de la fecha
    """

    print(f'{SNG}{q}')
    while True:
        dt: str = input(f'{SNG}')
        try:
            _ = datetime.strptime(dt, fmt)
            break
        except ValueError:
            print(f'{SNG}Ingrese el formato soliciado...')

    return dt
