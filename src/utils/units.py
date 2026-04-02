from decimal import Decimal


def px_to_mm(px: int, dpi: int) -> Decimal:
    return Decimal(px) * Decimal('25.4') / Decimal(dpi)


def px_to_pt(px: int, dpi: int) -> Decimal:
    return Decimal(px) * Decimal('72') / Decimal(dpi)


def mm_to_pt(mm: int) -> Decimal:
    return Decimal(mm) * Decimal('72') / Decimal('25.4')


def in_to_pt(inches: int | float) -> Decimal:
    return Decimal(str(inches)) * Decimal('72')


def pt_to_mm(points: Decimal) -> Decimal:
    return points / Decimal('72') * Decimal('25.4')

def pt_to_in(points: Decimal) -> Decimal:
    return points / Decimal('72')
