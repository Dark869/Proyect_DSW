from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import Proyect_DSW.controllers.cifrado_AES as AES
import Proyect_DSW.controllers.keys as keys

#=============== Funcion para firmar ========

def firmar(file, cifrado, passwd, iv):
    key_AES = AES.generar_llave_aes(passwd)
    key_private = AES.descifrar(cifrado, key_AES, iv)
    key_private = keys.convertir_bytes_llave_privada(key_private)
    file_firmado = key_private.sign(file, ec.ECDSA(hashes.SHA256()))
    return file_firmado

#=============== Funcion para firmar ========

def verificar(key_public ,firma, datos):
    try:
        key_public.verify(firma, datos, ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False
