import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from ..models import Unidad, Producto

# Create your views here.
@login_required
def listar_compras(request):
    return render(request, "compras/listar_compras.html")

@login_required
def nueva_compra(request):
    unidades = Unidad.objects.all()
    productos = Producto.objects.all()
    return render(request, "compras/nueva_compra.html", {"unidades": unidades, "productos": productos})

@login_required
def crear_compra(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)  # Aquí puedes ver los datos recibidos en la consola para depuración    
        # Aquí puedes manejar la lógica para crear una nueva compra con los datos recibidos

        datos_compra = {
            "proveedor": "AAA"
        }

        detalles_compra = data["detalle_compra"]

        print(datos_compra)
        print(detalles_compra)

        return JsonResponse({"message": "Compra creada exitosamente"})
    return redirect("nueva_compra")