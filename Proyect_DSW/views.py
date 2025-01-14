from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
import mimetypes
from .controllers.decorator import login_request
from db import models
import Proyect_DSW.controllers.password_policy as policy
import Proyect_DSW.controllers.cifrado_AES as AES
import Proyect_DSW.controllers.hash as hasheo
import Proyect_DSW.controllers.keys as keysss
import Proyect_DSW.controllers.keys_controllers as controllers
import os
#Libreria para tiempo
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

@login_request
def index_view(request):
    return render(request, 'index.html')

@login_request
def home_view(request):
    t = 'signatureFile.html'
    if request.method == 'GET':
        username = request.session.get('user')
        return render(request, t, {'username': username})
    elif request.method == 'POST':
        username = request.session.get('user')
        passwd = request.POST.get('passwd', '')
        file = request.FILES.get('file')
        passwd = passwd.strip()
        errores = []
        if not passwd:  
            errores.append('Campos no pueden ir vacios')
            return render(request, t, {'username': username,
                                       'errores': errores})
        try:
            passwd_cifrado = hasheo.password_hash(passwd)
            models.User.objects.get(nick=username, passwd=passwd_cifrado)
        except:
            errores.append('Contraseña incorrecta')
        if errores:
            return render(request, t, {'username': username,
                                       'errores': errores})
        else:
            user = models.User.objects.get(nick=username, passwd=passwd_cifrado)
            key = models.Keys.objects.get(user=user)
            caducidad = key.caducidad
            if timezone.now() < caducidad:
                key_private_cifrada = key.private_key_file
                key_public = key.public_key_file
                iv = key.iv
                file_bytes = file.read()
                file_firmado = controllers.firmar(file_bytes, key_private_cifrada, passwd, iv)
                key_public = keysss.convertir_bytes_llave_publica(key_public)
                if controllers.verificar(key_public, file_firmado, file_bytes):
                    response = HttpResponse(ContentFile(file_firmado))
                    content_type, encoding = mimetypes.guess_type(file.name)
                    response['Content-Type'] = content_type
                    response['Content-Disposition'] = f'attachment; filename="{file.name}_firmado"'
                    return response
                else:
                    errores.append('Error al firmar')
                    return render(request, t, {'username': username,
                                                'errores': errores})
            else:
                errores.append('Llave caducada, cree otra')
                return render(request, t, {'username': username,
                                            'errores': errores})


@login_request
def gestorLLaves_view(request):
    t = 'gestorLLaves.html'
    if request.method == 'GET':
        username = request.session.get('user')
        return render(request, t, {'username': username})
    elif request.method == 'POST':
        passwod = request.POST.get('passwd', '')
        username = request.session.get('user')
        passwod = passwod.strip()
        errores = []
        confirmacion = []
        if not passwod:
            errores.append('Campos no pueden ir vacios')
            return render(request, t, {'username': username,
                                       'errores': errores})
        try:
            passwd_cifrado = hasheo.password_hash(passwod)
            models.User.objects.get(nick=username, passwd=passwd_cifrado)
        except:
            errores.append('Contraseña incorrecta')
        if errores:
            return render(request, t, {'username': username,
                                       'errores': errores})
        else:
            user = models.User.objects.get(nick=username, passwd=passwd_cifrado)
            #Borrar llaves
            key_old = models.Keys.objects.get(user=user)
            key_old.delete()
            #Crear llaves
            key_private = keysss.generar_llave_privada()
            key_public = keysss.generar_llave_publica(key_private)
            key_public = keysss.convertir_llave_publica_bytes(key_public)
            caducidad = datetime.now() + timedelta(minutes=10)
            #Cifrar llave privada
            llave_AES = AES.generar_llave_aes(passwod)
            iv = os.urandom(16)
            cifrado = AES.cifrar(key_private, llave_AES, iv)
            #Guardar nuevas llaves
            key_new = models.Keys(user=user, private_key_file= cifrado, public_key_file=key_public, iv= iv, caducidad= caducidad)
            key_new.save()
            confirmacion.append('Nuevo par de llaves generados exitosamente')
            return render(request, t, {'username': username,
                                       'confirmacion': confirmacion})

@login_request
def verificarFirma_view(request):
    username = request.session.get('user')
    t = 'verificarFirmas.html'
    if request.method == 'GET':
        return render(request, t, {'username': username})
    elif request.method == 'POST':
        user = request.POST.get('user', '')
        file = request.FILES.get('archivo')
        file_firmado = request.FILES.get('firma')
        user = user.strip()
        errores = []
        confirmacion = []
        if not user:
            errores.append('Campos no pueden ir vacios')
            return render(request, t, {'username': username,
                                       'errores': errores})
        try:
            models.User.objects.get(nick=user)
        except:
            errores.append('Nick no valido')
        if errores:
            return render(request, t, {'username': username,
                                       'errores': errores})
        else:
            user = models.User.objects.get(nick=user)
            key = models.Keys.objects.get(user=user)
            caducidad = key.caducidad
            if timezone.now() < caducidad:
                key_public = key.public_key_file
                file_bytes = file.read()
                file_firma_bytes = file_firmado.read()
                key_public = keysss.convertir_bytes_llave_publica(key_public)
                if controllers.verificar(key_public, file_firma_bytes, file_bytes):
                    confirmacion.append('Firmado valida')
                    return render(request, t, {'username': username,
                                                'confirmacion': confirmacion})
                else:
                    errores.append('Error al firmar')
                    return render(request, t, {'username': username,
                                                'errores': errores})
            else:
                errores.append('Llave caducada')
                return render(request, t, {'username': username,
                                            'errores': errores})
@login_request
def logout_view(request):
    request.session.flush()  

    return redirect('/login/')

#=============== Funcion de registro ===================
def register(request):
    if request.session.get('logged'):
        return redirect('/')

    t = 'register.html'
    if request.method == 'GET':
        return render(request, t)
    elif request.method == 'POST':
        name = request.POST.get('name', '')
        nick = request.POST.get('nick', '')
        passw = request.POST.get('passwd', '')
        confirpasswd = request.POST.get('confirmPasswd', '')
        email = request.POST.get('mail', '')
        name = name.strip()
        nick = nick.strip()
        passw = passw.strip()
        confirpasswd = confirpasswd.strip()
        email = email.strip()
        errores = []
        if not name or not nick or not passw or not confirpasswd or not email:
            errores.append('Los campos no deben ir vacios')
        if passw != confirpasswd:
            errores.append('Las contraseñas no son iguales')
        if models.User.objects.filter(nick = nick).exists():
            errores.append('Nick ya registrado')
        if models.User.objects.filter(email = email).exists():
            errores.append('Correo ya registrado')
        if not policy.politica_pass(passw):
            errores.append('La contraseña debe tener al menos 12 caracteres, una mayúscula, un número y un caracter especial.')
        if errores:
            return render(request, t, {'errores': errores})
        else:
            #Generacion de llaves
            key_private = keysss.generar_llave_privada()
            key_public = keysss.generar_llave_publica(key_private)
            key_public = keysss.convertir_llave_publica_bytes(key_public)
            #Creacion de vida util de llave
            caducidad = datetime.now() + timedelta(minutes=10)
            #Cifrar llave privada
            llave_AES = AES.generar_llave_aes(passw)
            iv = os.urandom(16)
            cifrado = AES.cifrar(key_private, llave_AES, iv)
            #hashear contraseña
            passwd_cifrado = hasheo.password_hash(passw)
            usuario = models.User(full_name = name, nick = nick, email = email, passwd = passwd_cifrado)
            usuario.save()
            keys = models.Keys(user=usuario, private_key_file= cifrado, public_key_file=key_public, iv= iv, caducidad= caducidad)
            keys.save()
            return redirect('/login')
        
#========== Funcion de login ===============

def login(request):
    if request.session.get('logged'):
        return redirect('/')
    
    t = 'login.html'
    if request.method == 'GET':
        return render(request, t)
    elif request.method == 'POST':
        nick = request.POST.get('nick', '')
        passwd = request.POST.get('passwd', '')
        nick = nick.strip()
        passwd = passwd.strip()
        errores = []
        if not nick or not passwd:
            errores.append('El usuario o contraseña no pueden estar vacíos')
            return render(request, t, {'errores': errores})
        try:
            #hashear contraseña
            passwd_cifrado = hasheo.password_hash(passwd)
            models.User.objects.get(nick=nick, passwd=passwd_cifrado)
        except:
            errores.append('nick o contraseña incorrectos')
            request.session['logged'] = False
        
        if errores:
            return render(request, t, {'errores': errores})
        else:
            request.session['logged'] = True
            request.session['user'] = nick
            return redirect('/')
