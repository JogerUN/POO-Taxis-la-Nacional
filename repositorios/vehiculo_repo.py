import sqlite3
from modulos.vehiculo import Vehiculo

class RepositorioVehiculo:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                placa TEXT PRIMARY KEY,
                marca TEXT,
                referencia TEXT,
                modelo INTEGER,
                numero_chasis TEXT,
                numero_motor TEXT,
                color TEXT,
                concesionario TEXT,
                fecha_compra_vehiculo TEXT,
                tiempo_garantia INTEGER,
                fecha_compra_poliza_seguro TEXT,
                proveedor_poliza_seguro TEXT,
                fecha_compra_segObligatorio TEXT,
                proveedor_segObligatorio TEXT,
                activo INTEGER
            )
        """)
        self.connection.commit()

    def guardar(self, vehiculo: Vehiculo):
        self.cursor.execute(
            "INSERT INTO vehiculos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            vehiculo.como_tupla()
        )
        self.connection.commit()

    def buscar_por_placa(self, placa):
        self.cursor.execute(
            "SELECT * FROM vehiculos WHERE placa=?",
            (placa.upper(),)
        )
        fila = self.cursor.fetchone()
        return Vehiculo(*fila) if fila else None
    
    def actualizarEstado(self, placa, nuevo_estado):
        self.cursor.execute(
            "UPDATE vehiculos SET activo=? WHERE placa=?",
            (nuevo_estado, placa.upper())
        )
        self.connection.commit()
        
    def actualizar_poliza(self, placa: str, datos: dict):
        # 🔥 ACTUALIZAR DIRECTAMENTE EN BD (SIN TOCAR vehiculo.py)
        self.cursor.execute("""
            UPDATE vehiculos SET
                fecha_compra_poliza_seguro = ?,
                proveedor_poliza_seguro = ?,
                fecha_compra_segObligatorio = ?,
                proveedor_segObligatorio = ?
            WHERE placa = ?
        """, (
            datos["fecha_compra_poliza_seguro"],
            datos["proveedor_poliza_seguro"],
            datos["fecha_compra_segObligatorio"],
            datos["proveedor_segObligatorio"],
            placa.upper()
        ))

        self.connection.commit()

    def lista_activos(self):
        self.cursor.execute('''
            SELECT placa, marca, referencia, modelo, color
            FROM vehiculos
            WHERE activo = 1
        ''')
        return self.cursor.fetchall()
     
