import os
from pathlib import Path
import shutil
from tempfile import gettempdir

# formato en consola
SNG = '> '

# ancho de consola, solo para que al dar formato no lleguen los renglones hasta
# el final de la consola
STDOUT_WIDTH, _ = shutil.get_terminal_size()

# directorio temporal
TMP_DIR: Path = Path(gettempdir()) / "PyProjects"

# editor de texto según el os, definimos el mapa de opciones
_os_apps: dict[str, str] = {
    'nt': r'C:\Windows\notepad.exe',
    'posix': 'kwrite'
}

# Validamos antes de asignar
if os.name not in _os_apps:
    raise RuntimeError(f'OS Desconocido: {os.name}!!!')

TXT_APP: str = _os_apps[os.name]

# formato general para fechas
DT_FMT = '%Y-%m-%d'
