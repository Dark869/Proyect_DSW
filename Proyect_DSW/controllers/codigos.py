#Librerias para la generacion de llaves
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import sys
#Librerias para cifrar a formato AES
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
#Librerias para hashear
import hashlib
#Libreria para expresiones regulares
import re
#Librerias para firmar archivos
from cryptography.exceptions import InvalidSignature

#========= Funciones para generar llaves =====================

def generar_llave_privada():
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    return private_key


def generar_llave_publica(llave_privada):
    return llave_privada.public_key()

#============= Llaves a byte a pem y viceversa ===================

def convertir_llave_privada_bytes(llave_privada):
    """
    Convierte de bytes a PEM
    """
    resultado = llave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    return resultado


def convertir_bytes_llave_privada(contenido_texto):
    """
    Convierte de PEM a bytes
    """
    resultado = serialization.load_pem_private_key(
        contenido_texto,
        backend=default_backend(),
        password=None)
    return resultado

def convertir_llave_publica_bytes(llave_publica):
    resultado = llave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return resultado


def convertir_bytes_llave_publica(contenido_texto):
    resultado = serialization.load_pem_public_key(
        contenido_texto,
        backend=default_backend())
    return resultado


#========= Funciones para cifrar AES =====================
def generar_llave_aes(password):
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),
                       length=32,
                       salt=None,
                       info=b'handshake data ',
                       backend=default_backend()).derive(password)
    return derived_key


def cifrar(key, llave_aes, iv):
    key = convertir_llave_privada_bytes(key)
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(key)
    cifrador.finalize()
    return cifrado

def descifrar(cifrado, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano

#=============== Funcion para firmar ========

def firmar(file, cifrado, passwd, iv):
    key_AES = generar_llave_aes(passwd)
    key_private = descifrar(cifrado, key_AES, iv)
    key_private = convertir_bytes_llave_privada(key_private)
    file_firmado = key_private.sign(file, ec.ECDSA(hashes.SHA256()))
    return file_firmado

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
    patron_especial = r'[\_\.\-@]' 
    return (
        len(passwd) >= 12
        and re.search(patron_digito, passwd)
        and re.search(patron_mayuscula, passwd)
        and re.search(patron_especial, passwd)
    )