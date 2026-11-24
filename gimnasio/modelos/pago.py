"""
pago.py
Un Pago es la mensualidad que paga un cliente por un mes.
Ejemplo: Ana, mes "2026-11", $90.000, pagado el "2026-11-09".
"""

from datetime import date


def mes_actual() -> str:
    # devuelve el mes de hoy en formato "AAAA-MM", por ejemplo "2026-11"
    return date.today().strftime("%Y-%m")


def validar_mes(mes: str):
    # el mes debe tener el formato "AAAA-MM", por ejemplo "2026-11"
    partes = mes.split("-")
    if len(partes) != 2 or len(partes[0]) != 4 or len(partes[1]) != 2:
        raise ValueError("El mes debe tener el formato AAAA-MM, por ejemplo 2026-11.")
    if not (partes[0].isdigit() and partes[1].isdigit()):
        raise ValueError("El mes debe tener el formato AAAA-MM, por ejemplo 2026-11.")
    if not (1 <= int(partes[1]) <= 12):
        raise ValueError("El número del mes debe estar entre 01 y 12.")


class Pago:
    def __init__(self, cliente, mes: str, valor: int, fecha: str):
        validar_mes(mes)
        if valor <= 0:
            raise ValueError("El valor del pago debe ser mayor que 0.")

        self.cliente = cliente
        self.mes = mes
        self.valor = valor
        self.fecha = fecha
