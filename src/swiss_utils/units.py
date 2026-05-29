__all__ = [
    'px_to_mm',
    'mm_to_pt',
    'in_to_pt',
    'px_to_pt',
    'pt_to_mm',
    'pt_to_in',
]


from decimal import Decimal


def px_to_mm(px: int, dpi: int) -> Decimal:
    """
    Converts pixels to millimeters based on the provided DPI.
    :param px: number of pixels
    :param dpi: dots per inch
    :return: equivalent length in millimeters as Decimal
    """
    return Decimal(px) * Decimal('25.4') / Decimal(dpi)


def px_to_pt(px: int, dpi: int) -> Decimal:
    """
    Converts pixels to points based on the provided DPI.
    :param px: number of pixels
    :param dpi: dots per inch
    :return: equivalent length in points as Decimal
    """
    return Decimal(px) * Decimal('72') / Decimal(dpi)


def mm_to_pt(mm: int) -> Decimal:
    """
    Converts millimeters to points.
    :param mm: number of millimeters
    :return: equivalent length in points as Decimal
    """
    return Decimal(mm) * Decimal('72') / Decimal('25.4')


def in_to_pt(inches: int | float) -> Decimal:
    """
    Converts inches to points.
    :param inches: number of inches
    :return: equivalent length in points as Decimal
    """
    return Decimal(str(inches)) * Decimal('72')


def pt_to_mm(points: Decimal) -> Decimal:
    """
    Converts points to millimeters.
    :param points: number of points as Decimal
    :return: equivalent length in millimeters as Decimal
    """
    return points / Decimal('72') * Decimal('25.4')


def pt_to_in(points: Decimal) -> Decimal:
    """
    Converts points to inches.
    :param points: number of points as Decimal
    :return: equivalent length in inches as Decimal
    """
    return points / Decimal('72')
