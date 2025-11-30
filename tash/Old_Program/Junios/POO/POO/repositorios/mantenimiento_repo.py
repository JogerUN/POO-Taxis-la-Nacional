import sqlite3
from modulos.mantenimiento import Mantenimiento

class RepositorioMantenimiento:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mantenimientos (
                numeroOrden TEXT PRIMARY KEY NOT NULL,
                placaVehiculo TEXT NOT NULL,
                nitProveedor TEXT NOT NULL,
                nombreProveedor TEXT NOT NULL,
                descripcionServicio TEXT NOT NULL,
                valorFacturado REAL NOT NULL,
                fechaServicio TEXT NOT NULL,
                FOREIGN KEY (placaVehiculo) REFERENCES vehiculos(placa)
            )
        ''')
        self.connection.commit()

    def fila_a_objeto(self, fila):
        if fila is None:
            return None
        return Mantenimiento(*fila)

    def crear(self, mantenimiento: Mantenimiento):
        try:
            self.cursor.execute(
                "INSERT INTO mantenimientos VALUES (?,?,?,?,?,?,?)",
                mantenimiento.como_tupla()
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise Exception("Número de orden repetido.")

    def buscar(self, numeroOrden):
        self.cursor.execute(
            "SELECT * FROM mantenimientos WHERE numeroOrden=?",
            (numeroOrden,)
        )
        fila = self.cursor.fetchone()
        return self.fila_a_objeto(fila)

    def actualizar(self, mantenimiento: Mantenimiento):
        cad = f"""
            UPDATE mantenimientos SET
                placaVehiculo='{mantenimiento.placaVehiculo}',
                nitProveedor='{mantenimiento.nitProveedor}',
                nombreProveedor='{mantenimiento.nombreProveedor}',
                descripcionServicio='{mantenimiento.descripcionServicio}',
                valorFacturado='{mantenimiento.valorFacturado}',
                fechaServicio='{mantenimiento.fechaServicio}'
            WHERE numeroOrden='{mantenimiento.numeroOrden}'
        """
        self.cursor.execute(cad)
        self.connection.commit()

    def borrar(self, numeroOrden):
        self.cursor.execute(
            "DELETE FROM mantenimientos WHERE numeroOrden=?",
            (numeroOrden,)
        )
        self.connection.commit()
        return self.cursor.rowcount
