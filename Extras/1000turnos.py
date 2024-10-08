import random
from datetime import datetime, timedelta

# Lista de odontólogos
odontologos = ["545", "4575", "5000"]

# Lista de prestaciones
prestaciones = ["CONSULTA", "EXTRACCIÓN", "TRATAMIENTO DE CONDUCTO", "LIMPIEZA"]

# Lista de pacientes (puedes expandirla según necesites)
pacientes = [
    "Juan Carlos González",
    "María Laura Fernández",
    "Carlos Alberto Rodríguez",
    "Ana María Pérez",
    "José Luis Martínez",
    "Laura Andrea García",
    "Francisco Javier López",
    "Carmen Beatriz Díaz",
    "Pedro Pablo Ramírez",
    "Patricia Alejandra Torres",
    "Luis Eduardo Gómez",
    "Sandra Verónica Sánchez",
    "Javier Andrés Castillo",
    "Teresa Raquel Herrera",
    "Daniel Alejandro Morales",
    "Elena Marcela Ortiz",
    "Alejandro Ricardo Ríos",
    "Marta Susana Jiménez",
    "Antonio Sebastián Ruiz",
    "Claudia Lorena Romero",
    "Fernando Martín Castro",
    "Isabel Cristina Mendoza",
    "Diego Nicolás Navarro",
    "Rosa Angélica Soto",
    "Ricardo Adrián Peña",
    "Silvia Carolina Delgado",
    "Eduardo Rubén Aguilar",
    "Lucía María Silva",
    "Raúl Enrique Ramos",
    "Victoria Soledad Vega",
    "Alberto David Cruz",
    "Beatriz Graciela Reyes",
    "Santiago Facundo Márquez",
    "Paula Milagros Paredes",
    "David Gabriel Estrada",
    "Gloria Alejandra Estrada",
    "Sergio Fabián Ponce",
    "Carolina Patricia Medina",
    "Andrés Eduardo Escobar",
    "Valeria Natalia Campos",
    "Manuel Esteban Salazar",
    "Julia Noemí Espinoza",
    "Adrián Sebastián Fuentes",
    "Lorena Fernanda Cabrera",
    "Enrique Raúl Aguirre",
    "Gabriela María Luna",
    "Jorge Federico Tapia",
    "Elena Isabel Flores",
    "Rubén Darío Serrano",
    "Sofía Belén Morales"
]


# Generar una fecha aleatoria entre 2024-01-01 y 2024-12-31
def generar_fecha_aleatoria():
    inicio = datetime(2024, 1, 1)
    fin = datetime(2024, 12, 31)
    delta = fin - inicio
    while True:
        dias_aleatorios = random.randint(0, delta.days)
        fecha_aleatoria = inicio + timedelta(days=dias_aleatorios)
        if fecha_aleatoria.weekday() != 6:  # 6 es domingo
            return fecha_aleatoria.strftime('%Y-%m-%d')

# Generar una hora aleatoria entre 8:00 y 20:00 con intervalos de 30 minutos
def generar_hora_aleatoria():
    horas = list(range(8, 21))  # Horas entre 8 y 20
    minutos = [0, 30]  # Minutos 00 y 30
    hora_aleatoria = f"{random.choice(horas):02}:{random.choice(minutos):02}"
    return hora_aleatoria

# Generar 1000 querys como texto
queries = []
for _ in range(1000):
    fecha = generar_fecha_aleatoria()
    hora = generar_hora_aleatoria()
    odontologo = random.choice(odontologos)
    prestacion = random.choice(prestaciones)
    paciente = random.choice(pacientes)  # Seleccionar un paciente aleatorio

    query = f"INSERT INTO Turnos (Fecha, Hora, Paciente, Odontologo, Prestacion) VALUES ('{fecha}', '{hora}', '{paciente}', '{odontologo}', '{prestacion}');"
    queries.append(query)

# Unir todas las querys en un solo texto
query_text = "\n".join(queries)

# Imprimir el resultado
print(query_text)

