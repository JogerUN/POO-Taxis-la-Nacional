from datetime import datetime

class Conductor:

    def __init__(self, noId, nombreCompleto, direccion, telefono, correo,
                 placaVehiculo, fechaIngreso, fechaRetiro, indicadorContratado,
                 turno, valorTurno, valorAhorro, valorAdeuda, totalNoDevuelto):

        self.__noId = noId
        self.__nombreCompleto = nombreCompleto
        self.__direccion = direccion
        self.__telefono = telefono
        self.__correo = correo
        self.__placaVehiculo = placaVehiculo
        self.__fechaIngreso = fechaIngreso
        self.__fechaRetiro = fechaRetiro
        self.__indicadorContratado = indicadorContratado
        self.__turno = turno
        self.__valorTurno = valorTurno
        self.__valorAhorro = valorAhorro
        self.__valorAdeuda = valorAdeuda
        self.__totalNoDevuelto = totalNoDevuelto

    # ---------------------------
    # GETTERS
    # ---------------------------
    def get_id(self):
        return self.__noId

    def get_nombre(self):
        return self.__nombreCompleto

    def get_direccion(self):
        return self.__direccion

    def get_telefono(self):
        return self.__telefono

    def get_correo(self):
        return self.__correo

    def get_placa(self):
        return self.__placaVehiculo

    def get_fecha_ingreso(self):
        return self.__fechaIngreso

    def get_fecha_retiro(self):
        return self.__fechaRetiro

    def get_indicadorContratado(self):
        return self.__indicadorContratado

    def get_turno(self):
        return self.__turno

    def get_valorTurno(self):
        return self.__valorTurno

    def get_valorAhorro(self):
        return self.__valorAhorro

    def get_valorAdeuda(self):
        return self.__valorAdeuda

    def get_totalNoDevuelto(self):
        return self.__totalNoDevuelto

    # ---------------------------
    # SETTERS PARCIALES
    # ---------------------------
    def set_direccion(self, nueva):
        self.__direccion = nueva

    def set_telefono(self, nuevo):
        self.__telefono = nuevo

    def set_correo(self, nuevo):
        self.__correo = nuevo

    def set_fecha_ingreso(self, nueva):
        self.__fechaIngreso = nueva

    def set_fecha_retiro(self, nueva):
        self.__fechaRetiro = nueva

    def set_valor_adeuda(self, nuevo):
        self.__valorAdeuda = nuevo

    def set_total_no_devuelto(self, nuevo):
        self.__totalNoDevuelto = nuevo

    # ---------------------------
    # POLIMORFISMO
    # ---------------------------
    def infConductor(self):
        return (
            self.__noId, self.__nombreCompleto, self.__direccion,
            self.__telefono, self.__correo, self.__placaVehiculo,
            self.__fechaIngreso, self.__fechaRetiro,
            self.__indicadorContratado, self.__turno, self.__valorTurno,
            self.__valorAhorro, self.__valorAdeuda, self.__totalNoDevuelto
        )

    def obtenerEstado(self):
        estados = {1: 'Activo', 2: 'Candidato', 3: 'Despedido'}
        try:
            key = int(self.__indicadorContratado)
        except:
            return "Desconocido"
        return estados.get(key, "Desconocido")

    def actualizarContacto(self, nuevaDir, nuevoTel, nuevoCorreo):
        if nuevaDir: self.__direccion = nuevaDir
        if nuevoTel: self.__telefono = nuevoTel
        if nuevoCorreo: self.__correo = nuevoCorreo
