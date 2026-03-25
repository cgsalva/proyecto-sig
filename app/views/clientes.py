from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from ..models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email', 'direccion']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí el nombre'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí el teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí el correo electrónico'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí el dirección'
            }),
        }


@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/listar_clientes.html", {
        "clientes": clientes
    })

@login_required
def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_clientes")
    else:
        form = ClienteForm()

    return render(request, "clientes/form_cliente.html", {
        "form": form,
        "titulo": "Agregar cliente"
    })

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("listar_clientes")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "clientes/form_cliente.html", {
        "form": form,
        "titulo": "Editar cliente"
    })

@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('listar_clientes')