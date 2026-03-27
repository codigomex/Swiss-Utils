from pathlib import Path
import tkinter as tk
from tkinter import Tk, filedialog
from typing import Optional


def pic_dir(dir_init: Path) -> Optional[Path]:
    """
    Abre un diólogo en Tk para escoger un directorio, devuelve la ruta a éste o
    None en caso de cancelación.
    :param dir_init: str, ruta inicial
    :return: ruta al dir escogido
    """

    root = tk.Tk()
    root.withdraw()
    ret: str = filedialog.askdirectory(initialdir=dir_init, title="Seleccione")
    return Path(ret) if ret else None


def pic_file(dir_init: Path, ext: str = "txt") -> Optional[Path]:
    """
    Dioálogo para seleccionar un archivo con extensión "ext",
    iniciando en "dir_init"
    :param dir_init: directorio inicial
    :param ext: extensión del archivo, sin punto
    :return:
    """

    root: Tk = tk.Tk()
    root.withdraw()

    file_path: str = filedialog.askopenfilename(
        title="Seleccione Un Archivo:",
        initialdir=dir_init,
        filetypes=[(f"Archivos {ext.upper()}", f".{ext.lower()}")],
    )

    return Path(file_path) if file_path else None 
