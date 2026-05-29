# Swiss-Utils – Essential Python Utilities

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue)](LICENSE)

A collection of **battle‑tested** utility modules for everyday Python tasks: console interaction, file dialogs, precise arithmetic, data handling, string formatting, system operations, and more.

> Designed to be **lightweight**, **self‑contained**, and easy to integrate into any project.

---

## 📦 Installation

```bash
pip install swiss-utils 
```

Or using UV:

```bash
uv add swiss-utils
```

Or clone & install manually:

```bash
git clone https://github.com/codigomex/Swiss-Utils.git
cd swiss_utils
pip install -e .
```

---

## 🚀 Quick Start

```python
from swiss_utils.console import pparr, ask_type, clear
from swiss_utils.math import div_prec, precise_round
from swiss_utils.system import show_tmp, init_tmp

# Or you can import everything using (eg):
# from swiss_utils import div_prec, init_tmp, pparr, etc.

# Clear terminal and print formatted message
clear()
pparr("Hello, world!", indent=">>> ")

# Safe division with decimal precision
result = div_prec(10, 3, precision=4)
print(result)  # 3.3333

# Round with specific rounding mode
rounded = precise_round(2.675, decimals=2)   # 2.68 (ROUND_HALF_UP)

# Show any text in a temporary file (opens in system editor)
init_tmp()
show_tmp("Important data\nLine 2", wait=True)
```

---

## 📚 Module Overview

| Module      | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `config`    | Global constants: OS detection, temp dir, ANSI escape, terminal width.     |
| `console`   | Interactive I/O: progress bar, waiting dots, user input validation, dates. |
| `data`      | Dictionary comparison, UUID‑like token generator, pretty data display.     |
| `format`    | Random strings, ANSI stripping, time formatting, terminal colors (`cl`).   |
| `forms`     | Tkinter file & directory dialogs (returns `Path` or `None`).               |
| `math`      | High‑precision rounding, division (with configurable precision), time‑to‑seconds. |
| `py`        | `@immutable` decorator – make class instances read‑only after `__init__`.  |
| `system`    | File execution, temp file handling, error traceback, user input via editor.|
| `units`     | Convert between pixels, mm, points, inches – exact `Decimal` results.      |

---

## 🧩 Detailed Examples

### 1. Console & User Input

```python
# swiss_utils.console
from swiss_utils import ask_verif, ask_date, op_yn, draw_progress_bar

# Yes/No prompt
if op_yn():
    print("User agreed")

# Validate from a set of answers
color = ask_verif("Choose color:", "red", "green", "blue")

# Date input (no future dates allowed)
date = ask_date("Enter birth date (YYYY-MM-DD):", fmt="%Y-%m-%d", future=False)

# Progress bar
for p in range(0, 101, 10):
    draw_progress_bar(p)
```

### 2. Immutable Classes

```python
# swiss_utils.py
from swiss_utils import immutable

@immutable
class Config:
    def __init__(self, host, port):
        self.host = host
        self.port = port

cfg = Config("localhost", 8080)
cfg.host = "other"   # ❌ raises AttributeError
```

### 3. Precise Arithmetic

```python
# swiss_utils.math
from swiss_utils import div_prec, precise_round
from decimal import ROUND_DOWN

# Division with 6 decimal places
result = div_prec(22, 7, precision=6)   # 3.142857

# Round with custom mode
rounded = precise_round(3.14159, decimals=4, rounding_mode=ROUND_DOWN)  # 3.1415
```

### 4. Temporary Files / System

```python

# swiss_utils.system
from swiss_utils import init_tmp, show_tmp, get_user_input

init_tmp(delete=True)          # clean previous temp dir

# Open a text file for long user input
lines = get_user_input("Describe the problem in detail:")
print(f"You wrote {len(lines)} lines")

# Show dictionary/object dump in a temp file
show_tmp("Debug info:\n" + str(some_dict), wait=False)
```

### 5. File Dialogs (no extra GUI loops)

```python
# swiss_utils.forms
from swiss_utils import pic_dir, pic_file

folder = pic_dir(Path.home())      # returns Path or None
file   = pic_file(Path.cwd(), ext="json")
```

### 6. Colors & Formatting

```python
# swiss_utils.format
from swiss_utils import cl

print(f"{cl.bgreen}Success!{cl.endc}")
print(f"{cl.red}Error:{cl.endc} Something went wrong")
```

---

## 🛠 Development & Testing

```bash
# Run all tests (if you add a tests/ folder)
pytest tests/

# Static type check
mypy swiss_utils/
```


## 🤝 Contributing

Pull requests are welcome [@codigomex](https://github.com/codigomex)! For major changes, please open an issue first.

## 📄 License

[GPL‑3.0](LICENSE) © CodigoMex
