from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django import forms
from ..models import Producto

# Create your views here.

# Formulario de productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'precio', 'stock_actual', 'stock_minimo', 'categoria']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe aquí el codigo'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe aquí el nombre'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':'2'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Escribe aquí el precio de venta'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

@login_required
def listar_productos(request):
    productos = Producto.objects.select_related("categoria").all()
    return render(request, "productos/productos.html", {
        "productos": productos
    })

@login_required
def obtener_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    data = {
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "precio": str(producto.precio),
        "stock_actual": producto.stock_actual
    }
    return JsonResponse(data)

@login_required
def productos_autocomplete(request):
    termino = request.GET.get("q", "")

    productos = Producto.objects.filter(
        Q(codigo__icontains=termino) |
        Q(nombre__icontains=termino)
    )[:5]

    data = list(
        productos.values(
            "codigo",
            "nombre",
            "precio",
            "stock_actual"
        )
    )

    return JsonResponse(data, safe=False)

@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_productos")
    else:
        form = ProductoForm()

    return render(request, "productos/form_producto.html", {
        "form": form,
        "titulo": "Agregar producto"
    })

@login_required
def editar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("listar_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "productos/form_producto.html", {
        "form": form,
        "titulo": "Editar producto"
    })

@login_required
def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.delete()
    return redirect('listar_productos')