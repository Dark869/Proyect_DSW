from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
import mimetypes
from .controllers.decorator import login_request
from db import models
import Proyect_DSW.settings as config
import Proyect_DSW.controllers.codigos as codigo
#Librerias para validar firma
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import os

from .controllers.signFile import sing_file

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
            passwd_cifrado = codigo.password_hash(passwd)
            models.User.objects.get(nick=username, passwd=passwd_cifrado)
        except:
            errores.append('Contraseña incorrecta')
        if errores:
            return render(request, t, {'username': username,
                                       'errores': errores})
        else:
            user = models.User.objects.get(nick=username, passwd=passwd_cifrado)
            key = models.Keys.objects.get(user=user)
            key_private_cifrada = key.private_key_file
            key_public = key.public_key_file
            iv = key.iv
            file_bytes = file.read()
            file_firmado = codigo.firmar(file_bytes, key_private_cifrada, passwd, iv)
            try:
                key_public = codigo.convertir_bytes_llave_publica(key_public)
                key_public.verify(file_firmado, file_bytes, ec.ECDSA(hashes.SHA256()))
                response = HttpResponse(ContentFile(file_firmado))
                content_type, encoding = mimetypes.guess_type(file.name)
                response['Content-Type'] = content_type
                response['Content-Disposition'] = f'attachment; filename="{file.name}_firmado"'
                return response
            except:
                errores.append('Error al firmar')
                return render(request, t, {'username': username,
                                            'errores': errores})
            

    username = request.session.get('user')

    if request.method == 'GET':
        return render(request, 'signatureFile.html', {'username': username})
    else:
        file = request.POST.get('file')
        passwd = request.POST.get('passwd')
        sing_file(passwd, file, username)
        return render(request, 'signatureFile.html', {'username': username})


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
            passwd_cifrado = codigo.password_hash(passwod)
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
            key_private = codigo.generar_llave_privada()
            key_public = codigo.generar_llave_publica(key_private)
            key_public = codigo.convertir_llave_publica_bytes(key_public)
            #Cifrar llave privada
            llave_AES = codigo.generar_llave_aes(passwod)
            iv = codigo.os.urandom(16)
            cifrado = codigo.cifrar(key_private, llave_AES, iv)
            #Guardar nuevas llaves
            key_new = models.Keys(user=user, private_key_file= cifrado, public_key_file=key_public, iv= iv)
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
        user = request.POST.get('nick', '')
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
            key_public = key.public_key_file
            file_bytes = file.read()
            file_firma_bytes = file_firmado.read()
            try:
                key_public = codigo.convertir_bytes_llave_publica(key_public)
                key_public.verify(file_firma_bytes, file_bytes, ec.ECDSA(hashes.SHA256()))
                confirmacion.append('Firmado valida')
                return render(request, t, {'username': username,
                                            'confirmacion': confirmacion})
            except:
                errores.append('Firma invalida')
                return render(request, t, {'username': username,
                                            'errores': errores})

@login_request
def logout_view(request):
    request.session.flush()  

    return redirect('/login/')