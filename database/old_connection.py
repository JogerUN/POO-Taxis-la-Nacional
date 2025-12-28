import sqlite3

def crearConexion():
    try:
        connection = sqlite3.connect("taxis_la_nacional.db")
        return connection
    except sqlite3.IntegrityError as e:
        print("Error al conectar con la base de datos:", e)
        return None
