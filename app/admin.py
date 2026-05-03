from django.contrib import admin
from .models import Categoria, Producto, Cliente, Cuenta

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Cuenta)