
# ------------------------------------------------------------
# REPOSITORIO: Acceso a la base de datos para Conductores.
# ------------------------------------------------------------

import sqlite3
from modulos.conductor import Conductor

class ConductorRepositorio:

    def __init__(self, connection):
        self.conn = connection

    # ------------------------------------------------------------
    # GUARDAR (INSERTAR)
    # ------------------------------------------------------------

    def guardar(self, conductor: Conductor):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO conductores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, conductor.infConductor())
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("❌ Error: Ese conductor ya existe.")
            return False

    # ------------------------------------------------------------
    # BUSCAR POR ID
    # ------------------------------------------------------------

    def buscar_por_id(self, noId):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noId,))
        fila = cursor.fetchone()

        if fila:
            return Conductor(*fila)
        return None

    # ------------------------------------------------------------
    # ACTUALIZAR CONTACTO
    # ------------------------------------------------------------

    def actualizar_contacto(self, conductor: Conductor):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE conductores 
            SET direccion=?, telefono=?, correoElectronico=?
            WHERE noIdentificacion=?
        """, (conductor.infConductor()[2], conductor.infConductor()[3],
              conductor.infConductor()[4], conductor.get_id()))
        self.conn.commit()

    # ------------------------------------------------------------
    # ACTUALIZAR VALORES ECONÓMICOS
    # ------------------------------------------------------------

    def actualizar_valores(self, conductor: Conductor):
        tupla = conductor.infConductor()
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE conductores SET valorAdeuda=?, totalAhorradoNoDevuelto=?
            WHERE noIdentificacion=?
        """, (tupla[12], tupla[13], conductor.get_id()))
        self.conn.commit()

    # ------------------------------------------------------------
    # LISTAR ACTIVOS
    # ------------------------------------------------------------

    def listar_activos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM conductores WHERE indicadorContratado='1'")
        filas = cursor.fetchall()
        return [Conductor(*fila) for fila in filas]
