from decimal import ROUND_HALF_UP, Decimal


def precise_round(
    number: int | float | Decimal, decimals: int=2, rounding_mode: str=ROUND_HALF_UP
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
    Calcula cuantos segundos representa un string del tipo
    hh:mm:ss, puede llegar como mm:ss o ss, se espera que
    si es un grupo de dígitos sean segundos, si son dos grupos, minutos
    y segundos, y si son tres grupos, horas, minutos y segundos.
    Es un período de tiempo, no una hora de algún día.
    :param st_time: st representando un período de tiempo.
    :return: int de segundos
    """

    # Si st_time ya representa un int, regresamos el entero
    if str(st_time).isdigit():
        return int(st_time)

    partes: list[str] = st_time.split(':')
    
    if len(partes) > 3:
        raise ValueError(f'Formato de tiempo no soportado: {st_time}')

    try:
        # Revertimos para que el índice coincida con la potencia de 60
        # seg: 60**0, min: 60**1, hrs: 60**2
        tot_seg: int = 0
        for i, t in enumerate(reversed(partes)):
            val: int = int(t)
            if not (0 <= val <= 60):
                raise ValueError(f'Valor fuera de rango (0-60): {t}')
            tot_seg += val * (60 ** i)
        return tot_seg
        
    except ValueError as e:
        raise ValueError(f'Error en el formato de tiempo: {st_time}') from e

