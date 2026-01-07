# repositorios/conductor_repo.py

import sqlite3
from modulos.conductor import Conductor


class ConductorRepo:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.crearTablaConductores()

    # ============================
    # TABLA
    # ============================
    def crearTablaConductores(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS conductores (
                noIdentificacion TEXT PRIMARY KEY NOT NULL,
                nombreCompleto TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correoElectronico TEXT NOT NULL,
                placaVehiculo TEXT NOT NULL,
                fechaIngreso TEXT,
                fechaRetiro TEXT,
                indicadorContratado INTEGER NOT NULL,
                turno INTEGER NOT NULL,
                valorTurno REAL NOT NULL,
                valorAhorro REAL NOT NULL,
                valorAdeuda REAL NOT NULL,
                totalAhorradoNoDevuelto REAL NOT NULL,
                FOREIGN KEY (placaVehiculo) REFERENCES vehiculos(placa)
            )
        """)
        self.connection.commit()

    # ============================
    # VALIDACIONES
    # ============================
    def placaExiste(self, placa: str) -> bool:
        self.cursor.execute(
            "SELECT 1 FROM vehiculos WHERE placa = ?",
            (placa,)
        )
        return self.cursor.fetchone() is not None

    # ============================
    # CRUD
    # ============================
    def registrar(self, conductor: Conductor):
        try:
            self.cursor.execute("""
                INSERT INTO conductores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, conductor.como_tupla())
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe un conductor con esa identificación")


    def actualizar(self, conductor: Conductor):
        self.cursor.execute("""
            UPDATE conductores SET
                placaVehiculo=?,
                direccion=?,
                telefono=?,
                correoElectronico=?,
                fechaIngreso=?,
                fechaRetiro=?,
                indicadorContratado=?,
                turno=?,
                valorTurno=?,
                valorAhorro=?,
                valorAdeuda=?,
                totalAhorradoNoDevuelto=?
            WHERE noIdentificacion=?
        """, (
            conductor.placaVehiculo,
            conductor.direccion,
            conductor.telefono,
            conductor.correoElectronico,
            conductor.fechaIngreso,
            conductor.fechaRetiro,
            conductor.indicadorContratado,
            conductor.turno,
            conductor.valorTurno,
            conductor.valorAhorro,
            conductor.valorAdeuda,
            conductor.totalAhorradoNoDevuelto,
            conductor.noIdentificacion
        ))
        self.connection.commit()

    def consultar(self, noIdentificacion: str):
        self.cursor.execute(
            "SELECT * FROM conductores WHERE noIdentificacion = ?",
            (noIdentificacion,)
        )
        fila = self.cursor.fetchone()
        return Conductor(*fila) if fila else None

    def listaActivos(self):
        self.cursor.execute("""
            SELECT noIdentificacion, nombreCompleto, placaVehiculo
            FROM conductores
            WHERE indicadorContratado = 1
        """)
        return self.cursor.fetchall()
