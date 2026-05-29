# PyUtils – Essential Python Utilities

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://shields.io/github/license/AnzhiZhang/PlayerBehaviorRecord?label=License)](LICENSE)

A collection of **battle‑tested** utility modules for everyday Python tasks: console interaction, file dialogs, precise arithmetic, data handling, string formatting, system operations, and more.

> Designed to be **lightweight**, **self‑contained**, and easy to integrate into any project.

---

## 📦 Installation

```bash
pip install pyutils   # once published
```

Or clone & install manually:

```bash
git clone https://github.com/yourusername/pyutils.git
cd pyutils
pip install -e .
```

---

## 🚀 Quick Start

```python
from pyutils.console import pparr, ask_type, clear
from pyutils.math import div_prec, precise_round
from pyutils.system import show_tmp, init_tmp

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
from pyutils.console import ask_verif, ask_date, op_yn, draw_progress_bar

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
from pyutils.py import immutable

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
from pyutils.math import div_prec, precise_round
from decimal import ROUND_DOWN

# Division with 6 decimal places
result = div_prec(22, 7, precision=6)   # 3.142857

# Round with custom mode
rounded = precise_round(3.14159, decimals=4, rounding_mode=ROUND_DOWN)  # 3.1415
```

### 4. Temporary Files / System

```python
from pyutils.system import init_tmp, show_tmp, get_user_input

init_tmp(delete=True)          # clean previous temp dir

# Open a text file for long user input
lines = get_user_input("Describe the problem in detail:")
print(f"You wrote {len(lines)} lines")

# Show dictionary/object dump in a temp file
show_tmp("Debug info:\n" + str(some_dict), wait=False)
```

### 5. File Dialogs (no extra GUI loops)

```python
from pyutils.forms import pic_dir, pic_file

folder = pic_dir(Path.home())      # returns Path or None
file   = pic_file(Path.cwd(), ext="json")
```

### 6. Colors & Formatting

```python
from pyutils.format import cl

print(f"{cl.bgreen}Success!{cl.endc}")
print(f"{cl.red}Error:{cl.endc} Something went wrong")
```

---

## 🛠 Development & Testing

```bash
# Run all tests (if you add a tests/ folder)
pytest tests/

# Static type check
mypy pyutils/
```

---

## 📦 Publishing to PyPI (once you're ready)

1. Create `pyproject.toml` or `setup.py` (example below).
2. Build:
   ```bash
   python -m build
   ```
3. Upload:
   ```bash
   twine upload dist/*
   ```

**Minimal `setup.py`** (place in project root):

```python
from setuptools import setup, find_packages

setup(
    name="pyutils",
    version="0.1.0",
    author="Your Name",
    description="Essential Python utilities for console, math, system, and more",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    license="MIT",
)
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

[GPL‑3.0](LICENSE) © CodeMex
```

---

## 📌 Additional Recommendations

1. **Create a `LICENSE` file** – choose MIT, Apache‑2.0, or GPL‑3.0.
2. **Add type hints** – your code already has many, that’s great.
3. **Write unit tests** – at least for `math`, `data`, `units`.
4. **Fix the minor issues** in `console.py`:
   - The parameter in `ask_verif` docstring says `resps` but actual name is `answers`.
   - In `ask_choices`, the parameter `*options` is correct but the docstring mentions `resps` again.
5. **`div_prec`** – you currently return `Decimal('0')` when `d == 0`. You previously discussed raising `DivisionByZero`. I recommend removing that special case and letting the exception propagate (or catching it inside if you prefer `None`). For now it’s okay.

Would you like me to also help you write the `setup.py` / `pyproject.toml` and the `__init__.py` to expose the public API? Just let me know.