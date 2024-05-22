import re

def validar_contrasenia(password):
    largo = re.compile(r'.{8,}')
    digito = re.compile(r'\d+')
    letra_may = re.compile(r'[A-Z]+')
    letra_min = re.compile(r'[a-z]+')
    longitud=False
    numero=False
    mayuscula=False
    minuscula=False
    valido=False
    a="Debe contener más de 8 caracteres"
    if(largo.search(password)):
        a=""
        longitud=True
    b="\nagregar un digito"
    if(digito.search(password)):
        b=""
        numero=True
    c="\nagregar una mayuscula"
    if(letra_may.search(password)):
        c=""
        mayuscula=True
    d="\nagregar una minuscula"
    if(letra_min.search(password)):
        d=""
        minuscula=True
    if(largo and numero and mayuscula and minuscula):
        valido = True

    cadena=a+b+c+d
    print(cadena)
    return valido

if(validar_contrasenia("NAD01748")):
    print("valido")
else:
    print("ERROR")
