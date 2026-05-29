__all__ = [
    'precise_round',
    'qseconds',
    'div_prec',
]


from decimal import ROUND_HALF_UP, Decimal, localcontext


def precise_round(
    number: int | float | Decimal, decimals: int = 2, rounding_mode: str = ROUND_HALF_UP
) -> Decimal:
    """
    Rounds a number to a specified number of decimal places using
    a given rounding mode (default is ROUND_HALF_UP).
    :param number: The number to round
    :param decimals: decimal places to round to, defaults to 2
    :param rounding_mode: desired rounding strategy, defaults to ROUND_HALF_UP
    :return: The rounded number as a Decimal object
    """
    # Convert the number to a Decimal (string is recommended for precision)
    decimal_number: Decimal
    if isinstance(number, float):
        decimal_number = Decimal(str(number))
    else:
        decimal_number = Decimal(number)

    # Define the precision format (e.g., '0.01' for 2 decimal places)
    quantize_pattern = Decimal('1e-{}'.format(decimals))

    # Apply quantize with the specific rounding mode
    rounded_number = decimal_number.quantize(quantize_pattern, rounding=rounding_mode)

    return rounded_number


def qseconds(st_time: str) -> int:
    """
    Calculates how many seconds a string in hh:mm:ss format represents.
    It can arrive as mm:ss or ss. Represents a time period, not a time of day.
    :param st_time: str representing a time period.
    :return: int of total seconds
    """
    # If st_time already represents an int, return the integer
    if str(st_time).isdigit():
        return int(st_time)

    parts: list[str] = st_time.split(':')

    if len(parts) > 3:
        raise ValueError(f'Unsupported time format: {st_time}')

    try:
        # Reversed so the index matches the power of 60
        # sec: 60**0, min: 60**1, hrs: 60**2
        tot_seg: int = 0
        for i, t in enumerate(reversed(parts)):
            val: int = int(t)
            if not (0 <= val <= 60):
                raise ValueError(f'Value out of range (0-60): {t}')
            tot_seg += val * (60**i)
        return tot_seg

    except ValueError as e:
        raise ValueError(f'Time format error: {st_time}') from e


def div_prec(n: int | float | str, d: int | float | str, precision: int = 6) -> Decimal:
    """
    Divides two numbers with a given precision. Returns a Decimal rounded to
    the specified number of decimal places.

    The division uses a temporary context with increased precision
    (precision + 2) to reduce rounding errors, then quantizes the result
    to the exact requested precision.

    Args:
        n: Numerator (int, float, or numeric string)
        d: Denominator (int, float, or numeric string)
        precision: Number of decimal places in the result (default 6)

    Returns:
        Decimal: The result of n / d rounded to `precision` decimal places.

    Raises:
        DivisionByZero: If `d` evaluates to zero (from decimal module).
        InvalidOperation: If conversion from string fails (e.g., non-numeric).
    """

    with localcontext() as ctx:
        # Prepare the "calculator" with a margin of error (8 digits)
        ctx.prec = precision + 2

        # Perform the division (internally has 8 digits)
        dirty = Decimal(str(n)) / Decimal(str(d))

        # Clean up and leave exactly the requested decimal places
        return dirty.quantize(Decimal(f'1.{"0" * precision}'))
