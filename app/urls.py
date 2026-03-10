from django.urls import path
from . import views
from .views import auth, dashboard, productos, categorias

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
]