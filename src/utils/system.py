import os
import shutil
import sys
import traceback
from pathlib import Path
from subprocess import DEVNULL, Popen, check_call
from time import sleep
from typing import Never

from .config import OS_NAME, SNG, TMP_DIR, TXT_APP
from .console import ask_valida, pparr
from .format import random_string, str_now


def exec_file(file_path: Path) -> bool:
    """
    Ejecuta un programa con la aplicación asociadad y continua
    :param file_path: ruta al archivo
    :return: bool indicando exito
    """

    try:
        # Ya se validó que OS_NAME solo tenga uno de estos 3 valores
        if OS_NAME == 'Windows':
            os.startfile(str(file_path))
            return True
        elif OS_NAME == 'Darwin':
            with open(os.devnull, 'w') as f:
                check_call(['open', file_path], stdout=f, stderr=f)
            return True
        elif OS_NAME == 'Linux':
            with open(os.devnull, 'w') as f:
                check_call(['xdg-open', file_path], stdout=f, stderr=f)
            return True

    except Exception as _:
        return False

    return False


def exit(msje: str = '', out_code: int = 0, wait: bool = False) -> Never:
    """
    Sale del programa
    :param msje: mensaje anunciando porqué se sale
    :param out_code: si se quiere dar un código numéricoc a sys.exit()
    :return: nada
    """

    if msje:
        pparr(msje, nl_antes=2)
    if wait:
        pparr('Presione Enter para Salir...')
        input(SNG)
    sys.exit(out_code)


def show_tmp(st: str, espera: bool = False, ext: str = 'txt') -> None:
    """
    Recibe un str y lo guarda en un archivo de texto temporal en
    el folder temporal definido globalmente, para ello genera un
    nombre de archivo aleatorio.
    :param st: str a mostrar
    :param espera: bool, si se detiene el programa hasta que se cierre el proc.
    :return: nada
    """

    # valida que exista el dir temporal
    if not TMP_DIR.exists():
        raise Exception('TMP_DIR no existe')
    # nombre de archivo
    fname: Path = tmp_fname(ext=ext)
    # escribe a archivo
    with open(fname, 'w', encoding='utf8') as f:
        f.write(st)
    # lo muestra y sale
    av: Popen[bytes] = Popen[bytes]([*TXT_APP, fname], stdout=DEVNULL, stderr=DEVNULL)
    if espera:
        av.wait()


def tmp_fname(ext: str) -> Path:
    """
    Genera un nombre de archivo en el dir temporal, notar que
    no genera el archivo
    :param ext: extensión sin el punto
    :return: ruta al archivo
    """

    # Limpiamos la extensión por si acaso traía punto
    ext = ext.lstrip('.')

    while True:
        # nombre de archivo
        name: str = f'{str_now()}_{random_string(3)}.{ext}'
        fname: Path = TMP_DIR / name

        # revisamos si existe
        if not fname.exists():
            return fname
        # si existe esperamos 1 segundo y volvemos a intentar,
        # desde que el nombre de archivo depende del tiempo y trae
        # un str random es de esperarse que el nuevo nombre no
        # exista
        else:
            sleep(1)


def init_tmp(borrar: bool = False) -> None:
    """
    Si no existe el directorio temporal, lo genera
    :return: nada
    """

    # si existe y no se pidió borrar no se hace nada
    if TMP_DIR.exists():
        if borrar:
            shutil.rmtree(TMP_DIR)
            os.mkdir(TMP_DIR)
    else:
        os.mkdir(TMP_DIR)


def file_check(filepath: Path) -> None:
    """
    Revisa si existe un archivo, caso no esté, da opción de esperar o salir.
    :param filepath: ruta Path al archivo
    :return: nada
    """

    while True:
        if filepath.exists():
            break
        else:
            pparr(
                f'{SNG}No se localiza el archivo:\n  {filepath}\n{SNG}¿Desea '
                f'(a)Asegurarse que Exista o (s)Salir? '
                f'(solo recuerde que es posible que haya información que se pierda)'
            )
            op_fc: str = ask_valida('', *list[str]('aAsS'))
            if op_fc.lower() == 'a':
                input('> Oprima Enter para Continuar...')
            else:
                print('> Saliendo...')
                sleep(0.5)
                exit()


def get_user_input(q: str = '') -> list[str]:
    """
    Pregunta la pregunta "q" y abre un archivo de texto para dejar que el usuario
    escriba la respuesta a la pregunta, se regresa la respuesta como una lista de strs
    :param q: pregunta
    :return: lista de respuestas
    """

    if q:
        print(q)

    fn: Path = tmp_fname('txt')
    with open(fn, 'w', encoding='utf8') as _:
        pass
    proc = Popen([*TXT_APP, fn])
    proc.wait()

    with open(fn, mode='rt', encoding='utf8') as f:
        data: str = f.read()

    return data.splitlines()


def where_err() -> str | None:
    """Returns 'LnNumber: Code' from the actual exception or None"""
    _, _, tb = sys.exc_info()

    if tb:
        resumen = traceback.extract_tb(tb)
        _, linea, _, texto = resumen[-1]
        return f'{linea}: {texto}'
    return None
