import os
import shutil
import sys
from pathlib import Path
from tempfile import gettempdir
from typing import Final

# formato en consola
SNG: Final[str] = '> '

# ancho de consola, solo para que al dar formato no lleguen los renglones hasta
# el final de la consola
_stdout_width, _ = shutil.get_terminal_size()
STDOUT_WIDTH: Final[int] = _stdout_width

# directorio temporal
TMP_DIR: Final[Path] = Path(gettempdir()) / 'PyProjects'

# editor de texto según el os, definimos el mapa de opciones
_os_apps: dict[str, list[str]] = {
    "nt": [r"C:\Windows\notepad.exe"],
    "linux": ["kwrite"],
    "darwin": ["open", "-e"],
}
_os_name = os.name
_patform = sys.platform
if _os_name == 'nt':
    key = 'nt'
elif _patform == 'darwin':
    key = 'darwin'
elif _os_name == 'posix':
    key = 'linux'
else:
    raise RuntimeError(
        f'OS Desconocido: os.name={_os_name}, sys.platform={_patform}'
    )

TXT_APP: Final[list[str]] = _os_apps[key]

# formato general para fechas
DT_FMT: Final[str] = '%Y-%m-%d'
