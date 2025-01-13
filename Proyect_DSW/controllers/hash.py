import hashlib

#=============== Funcion para hashear contraseña ========

def password_hash(password):
    pw_encode = password.encode('utf-8')
    hasher = hashlib.sha512()
    hasher.update(pw_encode)
    new_hash = hasher.hexdigest()
    return new_hash