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