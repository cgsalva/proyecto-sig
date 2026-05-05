from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from ..models import Unidad

# Create your views here.

class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['nombre', 'nombre_corto']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la unidad'
            }),
            'nombre_corto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre corto de la unidad'
            }),
        }

@login_required
def listar_unidades(request):
    unidades = Unidad.objects.all()
    return render(request, "unidades/listar_unidades.html", {"unidades": unidades})

@login_required
def crear_unidad(request):  
    if request.method == "POST":
        form = UnidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_unidades")
    else:
        form = UnidadForm()

    return render(request, "unidades/form_unidad.html", {
        "form": form,
        "titulo": "Agregar unidad"
    })

@login_required
def editar_unidad(request, id):
    unidad = get_object_or_404(Unidad, id=id)

    if request.method == "POST":
        form = UnidadForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect("listar_unidades")
    else:
        form = UnidadForm(instance=unidad)

    return render(request, "unidades/form_unidad.html", {
        "form": form,
        "titulo": "Editar unidad"
    })

@login_required
def eliminar_unidad(request, id):
    unidad = get_object_or_404(Unidad, id=id)
    unidad.delete()
    return redirect("listar_unidades")