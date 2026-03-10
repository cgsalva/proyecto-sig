from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from ..models import Categoria

# Create your views here.

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
        }

@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "categorias/categorias.html", {
        "categorias": categorias
    })

@login_required
def crear_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_categorias")
    else:
        form = CategoriaForm()

    return render(request, "categorias/form_categoria.html", {
        "form": form,
        "titulo": "Agregar categoria"
    })

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("listar_categorias")
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, "categorias/form_categoria.html", {
        "form": form,
        "titulo": "Editar categoria"
    })

@login_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('listar_categorias')