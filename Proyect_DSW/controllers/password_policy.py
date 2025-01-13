import re

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