from django.urls import path
from .views import home, inicio, login, registrar, recuperar, mi_perfil, resta_clave, mod_perfil, cerrar_sesion, listar_usuarios,  rpg, survival, horror, estrategia, vintage, marca

urlpatterns = [
    path('home', home, name="home"),
    path('inicio', inicio, name="inicio"),
    path('login', login, name="login"),
    path('registrar', registrar, name="registrar"),
    path('recuperar', recuperar, name="recuperar"),
    path('resta_clave', resta_clave, name="resta_clave"),
    path('mi_perfil', mi_perfil, name="mi_perfil"),
    path('mod_perfil', mod_perfil, name="mod_perfil"),
    path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
    path('listar_usuarios', listar_usuarios, name="listar_usuarios"),
    path('rpg', rpg, name="rpg"),
    path('survival', survival, name="survival"),
    path('horror', horror, name="horror"),
    path('estrategia', estrategia, name="estrategia"),
    path('vintage', vintage, name="vintage"),
    path('marca', marca, name="marca"),
]
