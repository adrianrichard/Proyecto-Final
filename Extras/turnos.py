from datetime import *
import sqlite3

print("probando")
mes_turno =  datetime.today().month
anio_turno= str(datetime.today().year)
#date_str = start_date.strftime('%d-%m-%Y')
print(mes_turno, anio_turno)
mes_turno="09"

try:        
    conn= sqlite3.connect('../bd/turnos.db')
    cur= conn.cursor()
    query = """
    SELECT strftime('%d', fecha) AS dia
    FROM turno
    WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?
    """
    cur.execute(query, ( anio_turno, mes_turno,  ))
    turnos_dados  = [fila[0] for fila in cur.fetchall()]
    
    # query = f"SELECT fecha FROM turno"
    # cur.execute(query)
    # turnos= cur.fetchall()
    
    print("turnos:",turnos_dados)
    #print("turnos2:",turnos)
except:
    print("No hay turnos")
#print(turnos_dados[1][0])
# resultados_list = [list(fila) for fila in turnos_dados]
# for fila in turnos_dados:
#     print(fila[0])
#SELECT strftime('%d', '2023-09-15') AS dia;
import sqlite3

def obtener_dias_por_mes_anio(db_path, anio, mes):
    # Conectar a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    
    # Crear la consulta SQL
    consulta = """
    SELECT strftime('%d', fecha) AS dia
    FROM turno
    WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?
    """
    
    # Ejecutar la consulta
    cursor.execute(consulta, (anio, mes,))
    
    # Obtener los resultados
    dias = [fila[0] for fila in cursor.fetchall()]
    
    # Cerrar la conexión
    conexion.close()
    
    return dias

# Ejemplo de uso
# db_path es la ruta de la base de datos SQLite
# Suponiendo que hay una tabla 'eventos' con una columna 'fecha' en formato 'YYYY-MM-DD'
dias = obtener_dias_por_mes_anio('../bd/turnos.db', '2024', '09')
print(dias)
