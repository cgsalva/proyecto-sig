from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from ..models import Cuenta

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['codigo', 'nombre', 'tipo', 'descripcion']

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
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción'
            }),
        }