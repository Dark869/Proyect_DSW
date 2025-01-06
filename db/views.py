#Librerias de django
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render, redirect
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

# Create your views here.
def verificarFirma(request):
    html = "verificarFirmas.html"
    return render(request, html)

def login(request):
    t = 'login.html'
    if request.method == 'GET':
        return render(request, t)
    elif request.method == 'POST':
        usuario = request.POST.get('usuario', '')
        password = request.POST.get('password', '')
        usuario = usuario.strip()
        password = password.strip()
        errores = []
        if not usuario or not password:
            errores.append('El usuario o contraseña no pueden estar vacíos')
        try:
            pss_codificada = password.encode('utf-8')
            hasher = hashlib.sha256()
            hasher.update(pss_codificada)
            hash_final = hasher.hexdigest()
            models.Usuarios.objects.get(user=usuario, passH=hash_final)
        except:
            errores.append('Usuario o contraseña incorrectos')
        
        if errores:
            request.session['logueado'] = False
            return render(request, t, {'errores': errores})
        request.session['logueado'] = True
        request.session['usuario'] = usuario
        return redirect('/modal')
    

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

#=============== Funcion de registro ===================
def register(request):
    t = 'register.html'
    if request.method == 'GET':
        return render(request, t)
    elif request.method == 'POST':
        name = request.POST.get('name', '')
        nick = request.POST.get('nick', '')
        passwd = request.POST.get('passwd', '')
        confirpasswd = request.POST.get('confirmPasswd', '')
        email = request.POST.get('mail', '')

        name = name.strip()
        nick = nick.strip()
        passwd = passwd.strip()
        confirpasswd = confirpasswd.strip()
        email = email.strip()

        errores = []
        if not name or not nick or not passwd or not confirpasswd or not email:
            errores.append('Los campos no deben ir vacios')
        if passwd == confirpasswd:
            errores.append('Las contraseñas no son iguales')
        if errores:
            #request.session['logueado'] = False
            return render(request, t, {'errores': errores})
        else:
            #Generacion de llaves
            key_private = generar_llave_privada()
            key_public = generar_llave_publica(key_private)
            #Cifrar llave privada
            llave_AES = generar_llave_aes(passwd)
            iv = os.urandom(16)
            cifrado = cifrar(key_private, llave_AES, iv)
            #
            return redirect('/login')