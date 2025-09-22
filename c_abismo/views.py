from django.shortcuts import render, redirect
from django.http import JsonResponse 
from core.models import Usuario

# Create your views here.
def home(request):
    nombre_usuario = request.session.get('usuario_nombre', None)
    return render(request, 'index.html', {'usuario_nombre': nombre_usuario})

def inicio(request): 
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'index.html', {'usuario_nombre': nombre_usuario})

def login(request):
    return render(request, 'login.html')

def registrar(request):
    return render(request, 'registrar_usr.html')

def recuperar(request):
    return render(request, 'recuperar_cta.html')

def resta_clave(request):
    return render(request, 'restablecer_clave.html')

def mi_perfil(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'perfil.html', {'usuario_nombre': nombre_usuario})
    
def mod_perfil(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'mod_perfil.html', {'usuario_nombre': nombre_usuario})

def cerrar_sesion(request):
    request.session.flush()
    return redirect('inicio')

def listar_usuarios(request): 
    nombre_usuario =  request.session.get('usuario_nombre', None)
    usuarios = Usuario.objects.all()
    return render(request, 'admin.html', {'usuarios': usuarios, 'usuario_nombre': nombre_usuario})


# categorías
def rpg(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'rpg.html', {'usuario_nombre': nombre_usuario})    

def survival(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'survival.html', {'usuario_nombre': nombre_usuario}) 

def horror(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'horror.html', {'usuario_nombre': nombre_usuario}) 


def estrategia(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'estrategia.html', {'usuario_nombre': nombre_usuario}) 

def vintage(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'vintage.html', {'usuario_nombre': nombre_usuario}) 

def marca(request):
    nombre_usuario =  request.session.get('usuario_nombre', None)
    return render(request, 'marca.html', {'usuario_nombre': nombre_usuario}) 




