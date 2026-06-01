from decimal import Decimal
from django.db import transaction
from .models import (
    Compra,
    DetalleCompra,
    Producto,
    AsientoContable,
    MovimientoContable,
    Cuenta
)

@transaction.atomic
def registrar_compra(datos_compra, detalles_compra):
    pass