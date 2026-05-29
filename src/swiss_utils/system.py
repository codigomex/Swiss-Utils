__all__ = [
    'exec_file',
    'init_tmp',
    'exit',
    'show_tmp',
    'tmp_fname',
    'file_check',
    'get_user_input',
    'where_err',
]


import os
import shutil
import sys
import traceback
from pathlib import Path
from subprocess import DEVNULL, Popen, check_call
from time import sleep
from typing import Never

from .config import IND, OS_NAME, TMP_DIR, TXT_APP
from .console import ask_verif, pparr
from .format import random_string, str_now


def exec_file(file_path: Path) -> bool:
    """
    Executes a program with its associated application and continues.
    :param file_path: path to the file
    :return: bool indicating success
    """
    try:
        # OS_NAME was already validated to be one of these 3 values
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


def exit(message: str = '', wait: str = '', out_code: int = 0) -> Never:
    """
    Exits the program.
    :param message: message announcing the reason for exiting
    :param wait: message asking to wait for user to press enter
    :param out_code: numeric code passed to sys.exit()
    :return: Never
    """
    if message:
        pparr(message, nl_bfore=2)
    if wait:
        pparr(wait)
        input(IND)
    sys.exit(out_code)


def show_tmp(st: str, wait: bool = False, ext: str = 'txt') -> None:
    """
    Receives a string and saves it to a temporary text file in
    the global temporary folder using a random file name.
    :param st: str to display
    :param wait: bool, pauses the program until the process is closed
    :param ext: file extension string
    :return: None
    """
    # Validate that the temp directory exists
    if not TMP_DIR.exists():
        raise Exception('TMP_DIR does not exist')

    # File name
    fname: Path = tmp_fname(ext=ext)

    # Write to file
    with open(fname, 'w', encoding='utf8') as f:
        f.write(st)

    # Show it and exit
    av: Popen[bytes] = Popen[bytes]([*TXT_APP, fname], stdout=DEVNULL, stderr=DEVNULL)
    if wait:
        av.wait()


def tmp_fname(ext: str) -> Path:
    """
    Generates a file name in the temporary directory. Does not
    create the file itself.
    :param ext: extension without the dot
    :return: path to the file
    """
    # Clean the extension just in case it had a dot
    ext = ext.lstrip('.')

    while True:
        # File name
        name: str = f'{str_now()}_{random_string(3)}.{ext}'
        fname: Path = TMP_DIR / name

        # Check if it exists
        if not fname.exists():
            return fname

        # If it exists, wait 1 second and try again
        else:
            sleep(1)


def init_tmp(delete: bool = False) -> None:
    """
    Creates the temporary directory if it does not exist.
    :param delete: if True, deletes the directory first if it exists
    :return: None
    """
    # If it exists and deletion wasn't requested, do nothing
    if TMP_DIR.exists():
        if delete:
            shutil.rmtree(TMP_DIR)
            TMP_DIR.mkdir(parents=True, exist_ok=True)
    else:
        TMP_DIR.mkdir(parents=True, exist_ok=True)


def file_check(filepath: Path) -> None:
    """
    Checks if a file exists. If not, gives the option to wait or exit.
    :param filepath: Path to the file
    :return: None
    """
    while True:
        if filepath.exists():
            break
        else:
            pparr(
                f'{IND}File not found:\n  {filepath}\n{IND}Do you want to '
                f'(a)Assure it exists or (s)Stop? '
                f'(remember that some data might be lost)'
            )
            op_fc: str = ask_verif('', *list[str]('aAsS'))
            if op_fc.lower() == 'a':
                input('> Press Enter to Continue...')
            else:
                print('> Exiting...')
                sleep(0.5)
                exit()


def get_user_input(q: str = '') -> list[str]:
    """
    Asks a question and opens a text file to let the user write
    the answer. Returns the response as a list of strings.
    :param q: question prompt
    :return: list of response strings
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
    """
    Returns 'LnNumber: Code' from the actual exception or None.
    :return: formatted error string or None
    """
    _, _, tb = sys.exc_info()

    if tb:
        resumen = traceback.extract_tb(tb)
        _, linea, _, texto = resumen[-1]
        return f'{linea}: {texto}'
    return None
