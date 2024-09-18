from datetime import *
import sqlite3

print("probando")
mes_turno =  datetime.today().month
#date_str = start_date.strftime('%d-%m-%Y')
print(mes_turno)
mes_turno="09"
try:        
    conn= sqlite3.connect('../bd/turnos.db')
    cur= conn.cursor()
    query = f"SELECT strftime('%d', fecha) FROM turno WHERE strftime('%m', fecha)= ?"
    cur.execute(query, (mes_turno,))
    turnos_dados = cur.fetchall()
    conn.commit()
    print(turnos_dados)
except:
    print("No hay turnos")
print(turnos_dados[1][0])
resultados_list = [list(fila) for fila in turnos_dados]
for fila in turnos_dados:
    print(fila[0])