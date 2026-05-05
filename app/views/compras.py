from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def listar_compras(request):
    return render(request, "compras/listar_compras.html")

@login_required
def nueva_compra(request):
    return render(request, "compras/nueva_compra.html")