# conductor_repo.py

import sqlite3
from modulos.conductor import Conductor
        
class ConductorRepo:
    def __init__(self):
        self.connection = sqlite3.connect("taxis_la_nacional.db")
        self.crearTablaConductores()

    def crearTablaConductores(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conductores(
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
        ''')
        self.connection.commit()

    def placaExiste(self, placa):
        cursor = self.connection.cursor()
        cursor.execute("SELECT placa FROM vehiculos WHERE placa = ?", (placa,))
        return cursor.fetchone() is not None
    
    def registrar(self, conductor: Conductor):
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO conductores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                conductor.noIdentificacion,
                conductor.nombreCompleto,
                conductor.direccion,
                conductor.telefono,
                conductor.correoElectronico,
                conductor.placaVehiculo,
                conductor.fechaIngreso,
                conductor.fechaRetiro,
                conductor.indicadorContratado,
                conductor.turno,
                conductor.valorTurno,
                conductor.valorAhorro,
                conductor.valorAdeuda,
                conductor.totalAhorradoNoDevuelto
            ))
            self.connection.commit()
            return "✅ Conductor registrado correctamente."
        except sqlite3.IntegrityError:
            return "❌ Error: Ya existe un conductor con ese número de identificación."
        except sqlite3.Error as e:
            return f"⚠ Error al registrar conductor: {e}"

    def actualizar(self, conductor: Conductor):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE conductores SET
                placaVehiculo=?,direccion=?, telefono=?, correoElectronico=?,
                fechaIngreso=?, fechaRetiro=?,indicadorContratado=?,turno=?,valorAdeuda=?,
                totalAhorradoNoDevuelto=?
            WHERE noIdentificacion=?
        ''', (
            conductor.placaVehiculo,
            conductor.direccion,
            conductor.telefono,
            conductor.correoElectronico,
            conductor.fechaIngreso,
            conductor.fechaRetiro,
            conductor.indicadorContratado,
            conductor.turno,
            conductor.valorAdeuda,
            conductor.totalAhorradoNoDevuelto,
            conductor.noIdentificacion
        ))
        self.connection.commit()
        return "✅ Conductor actualizado correctamente."

    def consultar(self, noIdentificacion):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noIdentificacion,))
        return cursor.fetchone()

    def listaActivos(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT noIdentificacion, nombreCompleto, placaVehiculo FROM conductores WHERE indicadorContratado=1")
        return cursor.fetchall()
