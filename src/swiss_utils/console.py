__all__ = [
    'ask_verif',
    'clear',
    'draw_progress_bar',
    'pparr',
    'window_title',
    'op_yn',
    'waiti',
    'start_dots',
    'stop_dots',
    'tellme',
    'tobool',
    'ask_date',
    'ask_type',
    'ask_choice',
    'ask_choices',
    'ask_date_fmt_iso8601',
]


import textwrap
from datetime import datetime
from subprocess import run
from threading import Event, Thread
from time import sleep
from typing import Literal

from .config import DT_FMT, IND, OS_NAME, STDOUT_WIDTH

_stop_event = None
_dot_thread = None


def draw_progress_bar(percentage: int) -> None:
    """Renders a scannable progress bar in the terminal."""

    nobar = STDOUT_WIDTH - 9

    bar_length = nobar if nobar > 30 else 30
    filled_length = int(bar_length * percentage // 100)

    # Constructing the visual block [██████░░░░░░░░░]
    bar = '█' * filled_length + '░' * (bar_length - filled_length)

    # \r forces the cursor to the start of the line, avoiding scrolling down
    print(f'\r[{bar}] {percentage}%', end='', flush=True)

    # Print a new line only when completely finished
    if percentage == 100:
        print()


def _waiting_dot(stop_event: Event, char: str, delay: float) -> None:
    """Internal function that runs in the background thread."""
    while not stop_event.is_set():
        print(f'{char}', end='', flush=True)
        stop_event.wait(delay)


def start_dots(char: str = '.', delay: float = 0.5) -> None:
    """Starts the background dot animation safely."""
    global _stop_event, _dot_thread

    if _dot_thread and _dot_thread.is_alive():
        return

    _stop_event = Event()
    _dot_thread = Thread(
        target=_waiting_dot, args=(_stop_event, char, delay), daemon=True
    )
    _dot_thread.start()


def stop_dots() -> None:
    """Stops the background dot animation and cleans up."""
    global _stop_event, _dot_thread

    if _stop_event and _dot_thread:
        _stop_event.set()
        _dot_thread.join()
        print()
        _stop_event = None
        _dot_thread = None


def ask_verif(
    message: str, *answers: str, indent: str = IND, nl_bfore: int = 0, nl_after: int = 0
) -> str:
    """
    Asks a question and waits for a valid response from answers.
    The question is formatted with pparr using the provided parameters.
    :param message: question string
    :param answers: accepted responses
    :param indent: indentation, defaults to SNG
    :param nl_bfore: new lines before
    :param nl_after: new lines after
    :return: validated response string
    """
    if message:
        pparr(message, indent, nl_bfore, nl_after)

    while True:
        answer: str = input(f'{indent}')

        if answer in answers:
            return answer

        ops = '/'.join(answers)
        pparr(
            f'Invalid response. Please choose one of these: [{ops}]',
            indent=indent,
        )


def clear() -> None:
    """Clears the command terminal screen."""
    command: Literal['cls', 'clear'] = 'cls' if OS_NAME == 'Windows' else 'clear'
    run(args=command, shell=True, check=False)


def window_title(title: str) -> None:
    """
    Changes the window title for the terminal.
    :param title: new title
    :return: None
    """
    if OS_NAME == 'Windows':
        import ctypes

        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif OS_NAME in ['Linux', 'Darwin']:
        print(f'\33]0;{title}\a', end='', flush=True)


def _parr(
    message: str,
    indent: str = IND,
    nl_bfore: int = 0,
    nl_after: int = 0,
    width: int = STDOUT_WIDTH,
) -> str:
    """Formats and returns the string. Does not print anything."""
    if not message.strip():
        return ''

    indent_n: str = ' ' * len(indent)

    def format_line(tx: str, first: bool) -> str:
        ini = indent if first else indent_n
        return textwrap.fill(
            text=tx,
            initial_indent=ini,
            subsequent_indent=indent_n,
            width=width,
        )

    lines: list[str] = message.splitlines()
    wlines = [format_line(lines[0], True)]
    for ln in lines[1:]:
        wlines.append(format_line(ln, False))

    fmt = '\n'.join(wlines)
    return f'{"\n" * nl_bfore}{fmt}{"\n" * nl_after}'


def pparr(
    message: str,
    indent: str = IND,
    nl_bfore: int = 0,
    nl_after: int = 0,
    width: int = STDOUT_WIDTH,
) -> None:
    """Prints the formatted result from _parr."""
    print(
        _parr(
            message=message,
            indent=indent,
            nl_bfore=nl_bfore,
            nl_after=nl_after,
            width=width,
        )
    )


def waiti(indent: str = IND) -> None:
    """Only waits for user input to pause execution."""
    _ = input(indent)


def op_yn(indent: str = IND) -> bool:
    """
    Waits for a standard user input equivalent to yes/no.
    :return: bool indicating yes (True) or no (False)
    """
    while True:
        resp: str = input(indent)
        if resp.lower() in ['s', 'si', 'yes', 'y', '1']:
            return True
        elif resp.lower() in ['n', 'no', 'noup', 'nel', 'false', '0']:
            return False
        else:
            pparr('Please enter a yes/no response!!!', indent)
            sleep(0.2)


def tellme(indent: str = IND, msg: str = '') -> str:
    """
    Similar to waiti, but returns a string typed by the user.
    Does not validate for empty strings.
    :param sangria: indentation, defaults to SNG
    :param msg: prompt message, defaults to empty
    :return: user response string
    """
    ret: str = input(f'{indent}{msg}')
    return ret


def tobool(val: str) -> bool:
    """
    Receives a value and interprets it as a bool. Raises an exception
    if the value cannot be recognized.
    :param val: value to interpret
    :return: corresponding bool
    """
    if str(val).lower() in ['ok', 'si', 'true', 'verdadero', '1', 'yes', 'y']:
        ret = True
    elif str(val).lower() in ['no', 'falso', 'false', '0', 'n']:
        ret = False
    else:
        raise Exception(f'Value ({val}) is not recognized as a bool...')
    return ret


def ask_date(
    message: str,
    fmt: str = DT_FMT,
    future: bool = False,
    indent: str = IND,
    nl_bfore: int = 0,
    nl_after: int = 0,
) -> datetime:
    """
    Asks for and validates a date string based on a given format.
    :param message: question prompt
    :param fmt: expected date format
    :param future: bool indicating if the date can be in the future
    :param indent: indentation, defaults to SNG
    :param nl_bfore: new lines before
    :param nl_after: new lines after
    :return: parsed datetime object
    """
    pparr(message, indent, nl_bfore, nl_after)
    while True:
        answer: str = input(f'{indent}')
        try:
            ret: datetime = datetime.strptime(answer, fmt)
            if not future and ret > datetime.now():
                pparr(
                    'Date cannot be greater than the current one! Try again.',
                    indent=indent,
                )
            else:
                break
        except ValueError:
            pparr(f'Unrecognized response, use format {fmt}', indent=indent)

    return ret


def ask_type(
    message: str,
    exp_type: type,
    indent: str = IND,
    nl_bfore: int = 0,
    nl_after: int = 0,
):
    """
    Asks a question and waits for a response castable to 'tipo'.
    :param message: question prompt
    :param tipo: expected type of the response
    :param indent: indentation, defaults to SNG
    :param nl_bfore: new lines before
    :param nl_after: new lines after
    :return: response casted to the requested type
    """
    pparr(message, indent, nl_bfore, nl_after)

    while True:
        answer: str = input(f'{indent}')
        try:
            return exp_type(answer)
        except (ValueError, TypeError):
            pparr(
                f'Error: Expected a [{exp_type.__name__}]. Try again.',
                indent=indent,
            )


def ask_choices(
    message: str = '',
    *options: str,
    sep: str = ',',
    indent: str = IND,
    nl_bfore: int = 0,
    nl_after: int = 0,
) -> list[str]:
    """
    Asks a question and expects one or more valid responses from options.
    :param message: question prompt
    :param options: accepted options or responses
    :param sep: response separator
    :param indent: indentation, defaults to SNG
    :param nl_bfore: new lines before
    :param nl_after: new lines after
    :return: list of validated selections
    """
    if message:
        pparr(message, indent, nl_bfore, nl_after)

    while True:
        user_answers = input(f'{indent}').split(sep)
        selection = [r.strip() for r in user_answers if r.strip()]

        if all(item in options for item in selection) and selection:
            return selection

        pparr(
            f'Error. Enter only valid options separated by "{sep}":',
            indent=indent,
        )
        print(f'{indent}{f" {sep} ".join(options)}')
        pparr('Avoid extra spaces between the separator.', indent=indent)


def ask_choice(*ops: str, q: str = 'What is your selection?', nlines_ops: bool = False):
    """
    Presents a list of options (*ops) and returns the chosen option.
    :param q: question prompt
    :param ops: list of options
    :param nlines_ops: if true, adds a newline between each option
    :return: chosen option string
    """
    width: int = len(str(len(ops)))

    print(f'\n{IND}{q}\n')

    for i, op in enumerate(ops, 1):
        print(f'  ({i:>{width}}) {op}')
        if nlines_ops:
            print()

    valid_options = [str(i) for i in range(1, len(ops) + 1)]
    num = ask_verif('', *valid_options)

    return ops[int(num) - 1]


def ask_date_fmt_iso8601(
    q: str = 'Enter a date in YYYY-MM-DD format:', fmt: str = '%Y-%m-%d'
):
    """
    Asks for a date input in ISO 8601 format, or the one indicated by fmt.
    :param q: question prompt
    :param fmt: date format string
    :return: date string
    """
    print(f'{IND}{q}')
    while True:
        dt: str = input(f'{IND}')
        try:
            _ = datetime.strptime(dt, fmt)
            break
        except ValueError:
            print(f'{IND}Please enter the requested format...')

    return dt
