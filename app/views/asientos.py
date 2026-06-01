from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from ..models import AsientoContable, MovimientoContable, Cuenta

class AsientoContableForm(forms.ModelForm):
    class Meta:
        model = AsientoContable
        fields = ['fecha', 'descripcion']

        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí la descripción del asiento'
            }),
        }

@login_required
def listar_asientos(request):
    asientos = AsientoContable.objects.all()
    return render(request, "asientos/listar_asientos.html", {
        "asientos": asientos
    })

@login_required
def crear_asiento(request):
    if request.method == 'POST':
        form = AsientoContableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_asientos')
    else:
        form = AsientoContableForm()
    return render(request, "asientos/crear_asiento.html", {
        "form": form
    })