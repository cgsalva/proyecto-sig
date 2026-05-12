from django.urls import path
from . import views
from .views import auth, dashboard, productos, categorias, clientes, cuentas, compras, unidades, ventas

urlpatterns = [
    path("", auth.login_view, name="login"),
    path('logout/', auth.logout_view, name='logout'),
    path("dashboard/", dashboard.dashboard, name="dashboard"),

    # Url para perfil de usuario
    path("perfil/", auth.user_profile, name="user_profile"),
    path("perfil/editar/", auth.edit_user_profile, name="edit_user_profile"),
    path("perfil/change_password/", auth.change_password, name="change_password"),
    
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

    # Urls para unidades
    path("unidades/", unidades.listar_unidades, name="listar_unidades"),
    path("unidades/nuevo/", unidades.crear_unidad, name="crear_unidad"),
    path("unidades/editar/<int:id>/", unidades.editar_unidad, name="editar_unidad"),
    path("unidades/eliminar/<int:id>/", unidades.eliminar_unidad, name="eliminar_unidad"),

    # Urls para clientes
    path("clientes/", clientes.listar_clientes, name="listar_clientes"),
    path("clientes/nuevo/", clientes.crear_cliente, name="crear_cliente"),
    path("clientes/editar/<int:id>/", clientes.editar_cliente, name="editar_cliente"),
    path("clientes/eliminar/<int:id>/", clientes.eliminar_cliente, name="eliminar_cliente"),

    # Urls para cuentas
    path("cuentas/", cuentas.listar_cuentas, name="listar_cuentas"),
    path("cuentas/nueva/", cuentas.crear_cuenta, name="crear_cuenta"),
    path("cuentas/editar/<codigo>/", cuentas.editar_cuenta, name="editar_cuenta"),
    path("cuentas/eliminar/<codigo>/", cuentas.eliminar_cuenta, name="eliminar_cuenta"),

    # Urls para compras
    path("compras/", compras.listar_compras, name="listar_compras"),
    path("compras/nueva/", compras.nueva_compra, name="nueva_compra"),

    # Urls para ventas
    path("ventas/", ventas.listar_ventas, name="listar_ventas"),
    path("ventas/nueva/", ventas.nueva_venta, name="nueva_venta"),
]