__all__ = [
    'pic_dir',
    'pic_file',
]


import tkinter as tk
from pathlib import Path
from tkinter import Tk, filedialog
from typing import Optional


def pic_dir(dir_init: Path) -> Optional[Path]:
    """
    Opens a Tk dialog to choose a directory. Returns the path or None
    in case of cancellation.
    :param dir_init: Path, initial directory
    :return: path to the chosen directory or None
    """
    root = tk.Tk()
    root.withdraw()
    ret: str = filedialog.askdirectory(initialdir=dir_init, title='Select')
    root.destroy()
    return Path(ret) if ret else None


def pic_file(dir_init: Path, ext: str = 'txt') -> Optional[Path]:
    """
    Dialog to select a file with the given extension 'ext',
    starting in 'dir_init'.
    :param dir_init: initial directory
    :param ext: file extension, without dot
    :return: path to the chosen file or None
    """
    root: Tk = tk.Tk()
    root.withdraw()

    file_path: str = filedialog.askopenfilename(
        title='Select a File:',
        initialdir=dir_init,
        filetypes=[(f'{ext.upper()} Files', f'*.{ext.lower()}')],
    )
    root.destroy()
    return Path(file_path) if file_path else None
