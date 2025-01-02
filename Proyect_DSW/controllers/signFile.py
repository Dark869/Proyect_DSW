import db.models as models

from cryptography.exceptions import InvalidSignature
from db.views import descifrar, generar_llave_aes

def sing_file (passwd, file, user):
    userId = models.User.objects.get(nick=user)
    keys = models.Keys.objects.get(user=userId)

    llave_aes = generar_llave_aes(passwd)

    private_key = descifrar(keys.private_key_file, llave_aes, keys.iv)

    signature = private_key.sign(file.encode(), None)

    try:
        public_key = keys.public_key_file.encode()
        public_key.verify(signature, file.encode(), None)
        print("Firma correcta", signature)
    except InvalidSignature:
        print("Firma incorrecta")

    print("Firmar archivo", keys.private_key_file)
