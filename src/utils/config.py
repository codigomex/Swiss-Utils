import platform
import re
import shutil
from pathlib import Path
from tempfile import gettempdir
from typing import Final

# sistema operativo, se asegura que sea Win, Mac, Linux
OS_NAME = platform.system()
if OS_NAME not in ['Linux', 'Windows', 'Darwin']:
    raise RuntimeError(f'OS Desconocido: {OS_NAME}')

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
    'Windows': [r'C:\Windows\notepad.exe'],
    'Linux': ['kwrite'],
    'Darwin': ['open', '-e'],
}

TXT_APP: Final[list[str]] = _os_apps[OS_NAME]

# formato general para fechas
DT_FMT: Final[str] = '%Y-%m-%d'

# para localizar y eliminar caracteres ANSI
ANSI_ESCAPE: Final[re.Pattern] = re.compile(r'\033\[[0-9]?[0-9]m')
