#Librerias de django
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
from db import models
import Proyect_DSW.settings as config
#Librerias para la generacion de llaves
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import sys
#Librerias para cifrar a formato AES
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
#Librerias para hashear
import hashlib
#Libreria para expresiones regulares
import re

#========= Funciones para generar llaves =====================

def generar_llave_privada():
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    return private_key


def generar_llave_publica(llave_privada):
    return llave_privada.public_key()

#========= Funciones para cifrar AES =====================
def generar_llave_aes(password):
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),
                       length=32,
                       salt=None,
                       info=b'handshake data ',
                       backend=default_backend()).derive(password)
    return derived_key


def cifrar(mensaje, llave_aes, iv):
    mensaje = b'mensaje'
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return cifrado


def descifrar(cifrado, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano

#=============== Funcion para hashear contraseña ========

def password_hash(password):
    pw_encode = password.encode('utf-8')
    hasher = hashlib.sha512()
    hasher.update(pw_encode)
    new_hash = hasher.hexdigest()
    return new_hash

#=============== Funcion de politica de contraseña ======

def politica_pass(passwd):
    patron_digito = r'\d'
    patron_mayuscula = r'[A-Z]'
    patron_especial = r'[!@#$%^&*()_+=-]'
    return (
        len(passwd) >= 12
        and re.search(patron_digito, passwd)
        and re.search(patron_mayuscula, passwd)
        and re.search(patron_especial, passwd)
    )

#=============== Funcion de registro ===================
def register(request):
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
        if not politica_pass(passw):
            errores.append('La contraseña debe tener al menos 12 caracteres, una mayúscula, un número y un caracter especial.')
        if errores:
            return render(request, t, {'errores': errores})
        else:
            #Generacion de llaves
            key_private = generar_llave_privada()
            key_public = generar_llave_publica(key_private)
            #Cifrar llave privada
            llave_AES = generar_llave_aes(passw)
            iv = os.urandom(16)
            cifrado = cifrar(key_private, llave_AES, iv)
            #hashear contraseña
            passwd_cifrado = password_hash(passw)
            usuario = models.User(full_name = name, nick = nick, email = email, passwd = passwd_cifrado)
            usuario.save()
            keys = models.Keys(user=usuario, private_key_file= cifrado, public_key_file=key_public, iv= iv)
            keys.save()
            return redirect('/login')
        
#========== Funcion de login ===============

def login(request):
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
            passwd_cifrado = password_hash(passwd)
            models.User.objects.get(nick=nick, passwd=passwd_cifrado)
        except:
            errores.append('nick o contraseña incorrectos')
        
        if errores:
            return render(request, t, {'errores': errores})
        else:
            return redirect('/vfirma')