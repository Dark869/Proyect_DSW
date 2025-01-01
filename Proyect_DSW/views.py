from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from .controllers.decorator import login_request
from db import models
import Proyect_DSW.settings as config
import Proyect_DSW.controllers.codigos as codigo

@login_request
def index_view(request):
    return render(request, 'index.html')

@login_request
def home_view(request):
    username = request.session.get('user')
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
            #Cifrar llave privada
            llave_AES = codigo.generar_llave_aes(passwod)
            iv = codigo.os.urandom(16)
            cifrado = codigo.cifrar(key_private, llave_AES, iv)
            #Guardar nuevas llaves
            key_new = models.Keys(user=user, private_key_file= cifrado, public_key_file=key_public, iv= iv)
            key_new.save()
            return render(request, t, {'username': username})

@login_request
def verificarFirma_view(request):
    username = request.session.get('user')
    return render(request, 'verificarFirmas.html', {'username': username})

@login_request
def logout_view(request):
    request.session.flush()  

    return redirect('/login/')