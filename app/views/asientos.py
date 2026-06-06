from decimal import Decimal

from django.contrib import messages
from django.db import transaction

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
@transaction.atomic
def crear_asiento(request):
    if request.method == 'POST':

        fecha = request.POST.get('fecha')
        descripcion = request.POST.get('descripcion')

        cuentas = request.POST.getlist('cuenta[]')
        debes = request.POST.getlist('debe[]')
        haberes = request.POST.getlist('haber[]')

        total_debe = Decimal('0.00')
        total_haber = Decimal('0.00')

        for debe in debes:
            total_debe += Decimal(debe)

        for haber in haberes:
            total_haber += Decimal(haber)

        # Validar que el asiento esté balanceado
        if total_debe != total_haber:

            messages.error(
                request,
                'El asiento contable no está balanceado.'
            )

            return redirect('crear_asiento')

        # Crear asiento
        asiento = AsientoContable.objects.create(
            fecha=fecha,
            descripcion=descripcion
        )

        # Crear movimientos
        for i in range(len(cuentas)):

            cuenta = Cuenta.objects.get(
                codigo=cuentas[i]
            )

            MovimientoContable.objects.create(
                asiento=asiento,
                cuenta=cuenta,
                debe=Decimal(debes[i]),
                haber=Decimal(haberes[i])
            )

        messages.success(
            request,
            'Asiento contable registrado correctamente.'
        )
        print(fecha, descripcion)  # Aquí puedes ver el asiento creado en la consola para depuración
        print(cuentas, debes, haberes)  # Aquí puedes ver los movimientos creados en la consola para depuración
        print(total_debe, total_haber)  # Aquí puedes ver los totales de debe y haber en la consola para depuración
        #return redirect('listar_asientos')

    cuentas = Cuenta.objects.all()

    return render(
        request,
        'asientos/crear_asiento.html',
        {
            'cuentas': cuentas
        }
    )