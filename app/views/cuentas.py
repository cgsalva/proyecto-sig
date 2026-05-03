from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from ..models import Cuenta

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['codigo', 'nombre', 'tipo']

        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de la cuenta'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la cuenta'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

@login_required
def listar_cuentas(request):
    cuentas = Cuenta.objects.all()
    return render(request, 'cuentas/listar_cuentas.html', {'cuentas': cuentas})

@login_required
def crear_cuenta(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cuentas')
    else:
        form = CuentaForm()

    return render(request, 'cuentas/form_cuenta.html', {
        'form': form,
        'titulo': 'Agregar cuenta'
    })

@login_required
def editar_cuenta(request, codigo):
    cuenta = get_object_or_404(Cuenta, codigo=codigo)

    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('listar_cuentas')
    else:
        form = CuentaForm(instance=cuenta)

    return render(request, 'cuentas/form_cuenta.html', {
        'form': form,
        'titulo': 'Editar cuenta'
    })

@login_required
def eliminar_cuenta(request, codigo):
    cuenta = get_object_or_404(Cuenta, codigo=codigo)
    cuenta.delete()
    return redirect('listar_cuentas')