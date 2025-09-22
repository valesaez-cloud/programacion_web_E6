from django.http import JsonResponse
# Create your views here.
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario
import json


@csrf_exempt
def registrar_usuario(request):
    ok, msg = False, ""
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    obligatorios = ['nombre', 'apellidos', 'correo', 'direccion', 'telefono', 'clave', 'rol']
    for campo in obligatorios:
        if not str(data.get(campo, '')).strip():
            return JsonResponse({'success': False, 'error': f'Campo {campo} es obligatorio.'}, status=400)

    if Usuario.objects.filter(correo=data['correo']).exists():
        return JsonResponse({'success': False, 'error': 'El correo ya está registrado.'}, status=409)
    
        #validación de clave segura
    ok, msg = validar_clave_segura(data['clave'])
    if not ok:
        return JsonResponse({'success': False, 'error': msg}, status=400)

    # Convierte el rol que llega del form (texto o número) a int 1/2
    rol_raw = str(data.get('rol', '')).strip()
    if rol_raw.isdigit():
        rol_val = int(rol_raw)
    else:
        rol_val = 1 if rol_raw.lower().startswith('admin') else 2

    try:
        Usuario.objects.create(
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            correo=data['correo'],
            direccion=data['direccion'],
            telefono=data['telefono'],
            rol=int(data['rol']),
            contrasena=make_password(data['clave'])
        )
        return JsonResponse({'success': True, 'mensaje': 'Usuario registrado correctamente.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
def iniciar_sesion(request):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    correo = str(data.get('correo', '')).strip()
    clave  = str(data.get('clave', '')).strip()
    if not correo or not clave:
        return JsonResponse({'success': False, 'error': 'Correo y contraseña son obligatorios.'}, status=400)

    try:
        usuario = Usuario.objects.get(correo=correo)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El correo no está registrado.'}, status=404)

    if not check_password(clave, usuario.contrasena):
        return JsonResponse({'success': False, 'error': 'Contraseña incorrecta.'}, status=401)

    # Guarda datos mínimos en sesión
    request.session['usuario_id'] = usuario.id
    request.session['usuario_nombre'] = usuario.nombre
    request.session['usuario_rol'] = usuario.rol
    
    return JsonResponse({'success': True, 'mensaje': 'Inicio de sesión exitoso.'})

@csrf_exempt
def validar_clave_segura(clave: str):
    if len(clave) < 7:
        return False, "La contraseña debe tener al menos 7 caracteres."
    if clave.isalpha() or clave.isdigit():
        return False, "Usa letras y números."
    if " " in clave:
        return False, "La contraseña no debe tener espacios."
    return True, "ok"


@csrf_exempt
def restablecer_clave(request):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        data = request.POST

    c1 = (data.get("clave1") or "").strip()
    c2 = (data.get("clave2") or "").strip()

    ok, msg = validar_clave_segura(c1)   # <-- ¡usa c1, NO data['clave1']!
    if not ok:
        return JsonResponse({'success': False, 'error': msg}, status=400)

    if c1 != c2:
        return JsonResponse({'success': False, 'error': 'Las contraseñas no coinciden.'}, status=400)

    uid = request.session.get("reset_uid") or request.session.get("usuario_id")
    if not uid:
        return JsonResponse({'success': False, 'error': 'No hay solicitud de reseteo activa.'}, status=401)

    try:
        u = Usuario.objects.get(id=uid)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'}, status=404)

    u.contrasena = make_password(c1)
    u.save()

    if 'reset_uid' in request.session:
        del request.session['reset_uid']

    return JsonResponse({'success': True, 'mensaje': 'Contraseña actualizada correctamente.'})


@csrf_exempt
def recuperar_clave(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            data = request.POST

        correo = (data.get("correo") or "").strip().lower()
        try:
            u = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return JsonResponse({"success": False, "error": "Correo no registrado"}, status=404)

        # Guarda un uid temporal para el reseteo
        request.session["reset_uid"] = u.id
        return JsonResponse({"success": True, "redirect": "/resta_clave"})

    return render(request, "recuperar_cta.html")


@csrf_exempt
def restablecer_clave(request):
    # Solo POST (lo llama tu JS)
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

    # Acepta JSON o form-data
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        data = request.POST

    c1 = (data.get("clave1") or "").strip()
    c2 = (data.get("clave2") or "").strip()

    if c1 != c2:
        return JsonResponse({'success': False, 'error': 'Las contraseñas no coinciden.'}, status=400)
    
    uid = request.session.get("reset_uid") or request.session.get("usuario_id")
    if not uid:
        return JsonResponse({'success': False, 'error': 'No hay solicitud de reseteo activa.'}, status=401)

    # Busca el usuario y guarda la nueva clave hasheada
    try:
        u = Usuario.objects.get(id=uid)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'}, status=404)

    u.contrasena = make_password(c1)  # si tu campo se llama distinto, cámbialo aquí
    u.save()

    # Limpia reset_uid si venía de “recuperar”
    if 'reset_uid' in request.session:
        del request.session['reset_uid']

    return JsonResponse({'success': True, 'mensaje': 'Contraseña actualizada correctamente.'})

@csrf_exempt
def actualizar_datos(request):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

    uid = request.session.get('usuario_id')
    if not uid:
        return JsonResponse({'success': False, 'error': 'Usuario no autenticado.'}, status=401)
    
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    try:
        usuario = Usuario.objects.get(id=uid)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'}, status=404)

    # Solo actualiza lo que venga
    if data.get("nombre"):
        usuario.nombre = data["nombre"].strip()
    if data.get("apellidos"):
        usuario.apellidos = data["apellidos"].strip()
    if data.get("correo") or data.get("mail"):
        usuario.correo = (data.get("correo") or data.get("mail")).strip()
    if data.get("direccion"):
        usuario.direccion = data["direccion"].strip()
    if data.get("telefono"):
        usuario.telefono = data["telefono"].strip()
    if data.get("rol") and str(data["rol"]).isdigit():
        usuario.rol = int(data["rol"])
    usuario.save()
    return JsonResponse({'success': True, 'mensaje': 'Datos actualizados correctamente.'})



@csrf_exempt 
def eliminar_usuario(request):
    if request.method == "POST":
        usuario_id = request.POST.get("id")

        if not usuario_id:
            return JsonResponse({"success": False, "error": "El campo id es obligatorio."}, status=400)

        try:
            usuario = Usuario.objects.get(id=usuario_id)
            usuario.delete()
            return JsonResponse({
                "success": True,
                "mensaje": f"Usuario con id {usuario_id} eliminado correctamente."
            })
        except Usuario.DoesNotExist:
            return JsonResponse({"success": False, "error": "Usuario no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Método no permitido."}, status=405)