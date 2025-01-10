#Librerias de django
from django.shortcuts import render, redirect
from db import models
#Llamada a funciones
import Proyect_DSW.controllers.codigos as codigo
#Decorador

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
        if not codigo.politica_pass(passw):
            errores.append('La contraseña debe tener al menos 12 caracteres, una mayúscula, un número y un caracter especial.')
        if errores:
            return render(request, t, {'errores': errores})
        else:
            #Generacion de llaves
            key_private = codigo.generar_llave_privada()
            key_public = codigo.generar_llave_publica(key_private)
            key_public = codigo.convertir_llave_publica_bytes(key_public)
            #Cifrar llave privada
            llave_AES = codigo.generar_llave_aes(passw)
            iv = codigo.os.urandom(16)
            cifrado = codigo.cifrar(key_private, llave_AES, iv)
            #hashear contraseña
            passwd_cifrado = codigo.password_hash(passw)
            usuario = models.User(full_name = name, nick = nick, email = email, passwd = passwd_cifrado)
            usuario.save()
            keys = models.Keys(user=usuario, private_key_file= cifrado, public_key_file=key_public, iv= iv)
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
            passwd_cifrado = codigo.password_hash(passwd)
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
