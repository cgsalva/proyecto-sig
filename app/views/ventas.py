from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from ..models import Unidad, Producto

# Create your views here.
@login_required
def listar_ventas(request):
    #ventas = Venta.objects.all()
    return render(request, "ventas/listar_ventas.html", {"ventas": []})

@login_required
def nueva_venta(request):
    unidades = Unidad.objects.all()
    if request.method == "POST":
        # Aquí puedes manejar la lógica para guardar la nueva venta
        return redirect("listar_ventas")
    return render(request, "ventas/nueva_venta.html", {"unidades": unidades})