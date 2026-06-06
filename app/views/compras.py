from decimal import Decimal
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django import forms
from django.contrib.auth.decorators import login_required
from ..models import Unidad, Producto, Compra, DetalleCompra, AsientoContable, MovimientoContable, Cuenta

# Create your views here.
@login_required
def listar_compras(request):
    compras = Compra.objects.all()
    return render(request, "compras/listar_compras.html", {"compras": compras})

@login_required
def nueva_compra(request):
    unidades = Unidad.objects.all()
    productos = Producto.objects.all()
    return render(request, "compras/nueva_compra.html", {"unidades": unidades, "productos": productos})

@login_required
@transaction.atomic
def crear_compra(request):
    if request.method == "POST":

        data = json.loads(request.body)

        detalles_compra = data["detalle_compra"]
        total = Decimal(str(data["total"]))

        # =========================
        # CREAR COMPRA
        # =========================

        compra = Compra.objects.create(
            costo_total=total
        )

        # =========================
        # DETALLES DE COMPRA
        # =========================

        for item in detalles_compra:

            producto = Producto.objects.get(
                codigo=item["codigo"]
            )

            cantidad = int(item["cantidad"])

            costo_unitario = Decimal(
                str(item["precio_compra"])
            )

            subtotal = cantidad * costo_unitario

            DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                costo_unitario=costo_unitario,
                subtotal=subtotal
            )

            # Actualizar stock

            producto.stock_actual += cantidad
            producto.save()

        # =========================
        # ASIENTO CONTABLE
        # =========================

        asiento = AsientoContable.objects.create(
            fecha=compra.fecha.date(),
            descripcion=f"Compra #{compra.id}"
        )

        cuenta_inventario = Cuenta.objects.get(
            codigo="1101"
        )

        cuenta_proveedores = Cuenta.objects.get(
            codigo="2101"
        )

        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuenta_inventario,
            debe=total,
            haber=0
        )

        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuenta_proveedores,
            debe=0,
            haber=total
        )

        return JsonResponse({
            "success": True,
            "compra_id": compra.id,
            "asiento_id": asiento.id
        })

    return redirect("nueva_compra")