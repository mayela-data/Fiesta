import sqlite3

# Conexión a SQLite
conn = sqlite3.connect('fiesta.db')
c = conn.cursor()

# Crear tabla de invitados
c.execute('''
CREATE TABLE IF NOT EXISTS invitados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    telefono TEXT,
    correo TEXT,
    asistira TEXT CHECK(asistira IN ('Si', 'No', 'No ha confirmado')) DEFAULT 'No ha confirmado',
    num_acompanantes INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
print("Base de datos y tabla 'invitados' creada correctamente.")
