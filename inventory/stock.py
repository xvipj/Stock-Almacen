"""Reglas de negocio para calcular existencias a partir de los movimientos.

Se mantiene en un módulo sin imports de modelos para que `catalog` pueda usarlo
sin crear importaciones circulares.
"""

ENTRADA = "ENTRADA"
SALIDA = "SALIDA"
AJUSTE = "AJUSTE"


def calcular_stock(movimientos):
    """Recorre los movimientos en orden cronológico y devuelve el stock actual.

    - ENTRADA suma unidades.
    - SALIDA resta unidades.
    - AJUSTE fija el stock exacto al valor indicado (útil tras un conteo físico).
    """
    stock = 0
    for movimiento in sorted(movimientos, key=lambda m: (m.fecha, m.pk or 0)):
        if movimiento.tipo == ENTRADA:
            stock += movimiento.cantidad
        elif movimiento.tipo == SALIDA:
            stock -= movimiento.cantidad
        else:  # AJUSTE
            stock = movimiento.cantidad
    return stock
