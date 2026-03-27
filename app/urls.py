from django.urls import path
from . import views
from .views import auth, dashboard, productos, categorias, clientes, proveedores

urlpatterns = [
    path("", auth.login_view, name="login"),
    path('logout/', auth.logout_view, name='logout'),
    path("dashboard/", dashboard.dashboard, name="dashboard"),
    
    # Urls para productos
    path("productos/", productos.listar_productos, name="listar_productos"),
    path("productos/nuevo/", productos.crear_producto, name="crear_producto"),
    path("productos/editar/<codigo>/", productos.editar_producto, name="editar_producto"),
    path("productos/eliminar/<codigo>/", productos.eliminar_producto, name="eliminar_producto"),

    # Urls para categorias
    path("categorias/", categorias.listar_categorias, name="listar_categorias"),
    path("categorias/nuevo/", categorias.crear_categoria, name="crear_categoria"),
    path("categorias/editar/<int:id>/", categorias.editar_categoria, name="editar_categoria"),
    path("categorias/eliminar/<int:id>/", categorias.eliminar_categoria, name="eliminar_categoria"),

    # Urls para clientes
    path("clientes/", clientes.listar_clientes, name="listar_clientes"),
    path("clientes/nuevo/", clientes.crear_cliente, name="crear_cliente"),
    path("clientes/editar/<int:id>/", clientes.editar_cliente, name="editar_cliente"),
    path("clientes/eliminar/<int:id>/", clientes.eliminar_cliente, name="eliminar_cliente"),

    # Urls para proveedores
    path("proveedores/", proveedores.listar_proveedores, name="listar_proveedores"),
    path("proveedores/nuevo/", proveedores.crear_proveedor, name="crear_proveedor"),
    path("proveedores/editar/<int:id>/", proveedores.editar_proveedor, name="editar_proveedor"),
    path("proveedores/eliminar/<int:id>/", proveedores.eliminar_proveedor, name="eliminar_proveedor"),
]