import platform
import re
import shutil
from pathlib import Path
from tempfile import gettempdir
from typing import Final

# OS, ensures it is Win, Mac, or Linux
OS_NAME = platform.system()
if OS_NAME not in ['Linux', 'Windows', 'Darwin']:
    raise RuntimeError(f'Unknown OS: {OS_NAME}')

# Console format
IND: Final[str] = '> '

# Console width, prevents formatted lines from reaching the edge
_stdout_width, _ = shutil.get_terminal_size()
STDOUT_WIDTH: Final[int] = _stdout_width

# Temporary directory
TMP_DIR: Final[Path] = Path(gettempdir()) / 'PyProjects'

# Text editor based on OS options map
_os_apps: dict[str, list[str]] = {
    'Windows': [r'C:\Windows\notepad.exe'],
    'Linux': ['kwrite'],
    'Darwin': ['open', '-e'],
}

TXT_APP: Final[list[str]] = _os_apps[OS_NAME]

# General date format
DT_FMT: Final[str] = '%Y-%m-%d'

# To locate and remove ANSI characters
ANSI_ESCAPE: Final[re.Pattern] = re.compile(r'\033\[[0-9]?[0-9]m')
