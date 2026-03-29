import os
import shutil
from pathlib import Path
from tempfile import gettempdir
from typing import Final

# formato en consola
SNG: Final[str] = "> "

# ancho de consola, solo para que al dar formato no lleguen los renglones hasta
# el final de la consola
_stdout_width, _ = shutil.get_terminal_size()
STDOUT_WIDTH: Final[int] = _stdout_width

# directorio temporal
TMP_DIR: Final[Path] = Path(gettempdir()) / "PyProjects"

# editor de texto según el os, definimos el mapa de opciones
_os_apps: dict[str, str] = {"nt": r"C:\Windows\notepad.exe", "posix": "kwrite"}

# Validamos antes de asignar
if os.name not in _os_apps:
    raise RuntimeError(f"OS Desconocido: {os.name}!!!")

TXT_APP: Final[str] = _os_apps[os.name]

# formato general para fechas
DT_FMT: Final[str] = "%Y-%m-%d"
