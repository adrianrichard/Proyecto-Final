import re

largo = re.compile(r'.{8,}')
digito = re.compile(r'\d+')
letra_may = re.compile(r'[A-Z]+')
letra_min = re.compile(r'[a-z]+')

validaciones = [(largo, "largo menor que ocho"),
                (digito, "no tiene digitos"),
                (letra_min, "no tiene letras minúsculas"),
                (letra_may, "no tiene letras mayúsculas")]

tests = [
    "1$22b2A234",
    "12345678Ab",
    "abcedfgh",
    "ABCDEFGH",
    "Va-12-da"
]

for test in tests:
    valida = True
    for validacion, mensaje in validaciones:
        if not validacion.search(test):
            print(f"{test}: {mensaje}")
            valida = False

    if valida:
        print(f"{test} ok")