import secrets
from pprint import pformat
from typing import Any

from .system import show_tmp


def octa_uuid(fmt: bool = True, comparar: list[str] | None = None) -> str:
    """
    Genera un identificador hexadecimal de 8 caracteres.
    Ejemplo: 'A1B2-C3D4' o 'A1B2C3D4'
    """

    while True:
        token = secrets.token_hex(4).upper()
        ret = f'{token[:4]}-{token[4:]}' if fmt else token
        if comparar:
            if ret not in comparar:
                return ret
        else:
            return ret


def comp_dicts(new: dict[Any, Any], old: dict[Any, Any]) -> tuple[bool, list[str]]:
    """
    Compara 2 diccionarios, ve si son nuevos, y caso no, presenta las
    diferencias
    :param new: diccionario "nuevo"
    :param old: diccionario "antiguo"
    :return: bool indicando igualdad + posible lista diferencias
    """

    if new == old:
        return True, []

    diffs: list[str] = []
    k_new, k_old = set[Any](new), set[Any](old)

    # Campos nuevos y eliminados
    for k in k_new - k_old:
        diffs.append(f'Nuevo Campo: [{k}] = {new[k]}')

    for k in k_old - k_new:
        diffs.append(f'Campo Suprimido: [{k}] = {old[k]}')

    # Valores que cambiaron (intersección de llaves)
    for k in k_new & k_old:
        if new[k] != old[k]:
            diffs.append(f'Campo [{k}] cambió de {old[k]} a {new[k]}')

    return False, diffs


def show_data(data: dict[str, object]) -> None:
    """
    Muestra un objeto pformat que es un dict que contiene
    en su key un valor y un objeto/clase como valor.
    :param data: objeto a mostrar
    :return: nada
    """
    ret: list[str] = []
    for k, v in data.items():
        # Usamos v.__dict__ directo como prefieres
        ret.append(f'KEY {k}\n{pformat(v.__dict__, width=70)}\n')

    show_tmp('\n'.join(ret))
