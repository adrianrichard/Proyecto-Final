import sqlite3

# Conectar a la base de datos SQLite cifrada con SQLCipher
conn = sqlite3.connect('encrypted_database.db')

# Establecer la clave de cifrado
conn.execute("PRAGMA key='key';")  # Reemplaza 'your_secret_key' con tu clave secreta

# Ejecutar cualquier otra configuración necesaria para SQLCipher
conn.execute("PRAGMA cipher_compatibility = 3;")  # Asegura la compatibilidad con SQLCipher

# Crear una tabla (opcional)
conn.execute('''CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value TEXT
            );''')

# Insertar datos en la tabla (opcional)
conn.execute("INSERT INTO data (name, value) VALUES (?, ?)", ('example', 'data'))

# Guardar los cambios
conn.commit()

# Recuperar los datos
cursor = conn.execute("SELECT * FROM data;")
for row in cursor:
    print(row)

# Cerrar la conexión
conn.close()
