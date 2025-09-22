from django.urls import path
from .views import registrar_usuario, iniciar_sesion, recuperar_clave, restablecer_clave, validar_clave_segura, actualizar_datos, eliminar_usuario

urlpatterns = [
    path('registrar_usuario', registrar_usuario, name="registrar_usuario"),
    path('iniciar_sesion', iniciar_sesion, name="iniciar_sesion"),
    path('recuperar_clave', recuperar_clave, name="recuperar_clave"), 
    path('restablecer_clave', restablecer_clave, name="restablecer_clave"), 
    path('validar_clave_segura', validar_clave_segura, name="validar_clave_segura"), 
    path('actualizar_datos', actualizar_datos, name="actualizar_datos"),
    path('eliminar_usuario', eliminar_usuario, name="eliminar_usuario"), 
]