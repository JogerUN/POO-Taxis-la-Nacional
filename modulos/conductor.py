# modulos/conductor.py
from datetime import datetime


class Conductor:
    def __init__(
        self,
        noIdentificacion,
        nombreCompleto,
        direccion,
        telefono,
        correoElectronico,
        placaVehiculo,
        fechaIngreso="",
        fechaRetiro="",
        indicadorContratado=1,
        turno=1,
        valorTurno=0,
        valorAhorro=0,
        valorAdeuda=0,
        totalAhorradoNoDevuelto=0
    ):
        self.noIdentificacion = noIdentificacion
        self.nombreCompleto = nombreCompleto
        self.direccion = direccion
        self.telefono = telefono
        self.correoElectronico = correoElectronico
        self.placaVehiculo = placaVehiculo
        self.fechaIngreso = fechaIngreso
        self.fechaRetiro = fechaRetiro
        self.indicadorContratado = indicadorContratado
        self.turno = turno
        self.valorTurno = valorTurno
        self.valorAhorro = valorAhorro
        self.valorAdeuda = valorAdeuda
        self.totalAhorradoNoDevuelto = totalAhorradoNoDevuelto

    # =========================
    # VALIDACIONES (UI-FRIENDLY)
    # =========================

    @property
    def noIdentificacion(self):
        return self._noIdentificacion

    @noIdentificacion.setter
    def noIdentificacion(self, valor):
        if not valor:
            raise ValueError("La identificación es obligatoria")
        self._noIdentificacion = str(valor)

    @property
    def nombreCompleto(self):
        return self._nombreCompleto

    @nombreCompleto.setter
    def nombreCompleto(self, valor):
        if not valor:
            raise ValueError("El nombre completo es obligatorio")
        self._nombreCompleto = valor.strip()

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = valor.strip() if valor else ""

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor and not valor.isdigit():
            raise ValueError("El teléfono solo debe contener números")
        self._telefono = valor or ""

    @property
    def correoElectronico(self):
        return self._correoElectronico

    @correoElectronico.setter
    def correoElectronico(self, valor):
        self._correoElectronico = valor.strip() if valor else ""

    @property
    def placaVehiculo(self):
        return self._placaVehiculo

    @placaVehiculo.setter
    def placaVehiculo(self, valor):
        if not valor:
            raise ValueError("La placa del vehículo es obligatoria")
        self._placaVehiculo = valor.upper()

    @property
    def fechaIngreso(self):
        return self._fechaIngreso

    @fechaIngreso.setter
    def fechaIngreso(self, valor):
        if valor:
            try:
                datetime.strptime(valor, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Fecha de ingreso inválida (DD/MM/AAAA)")
        self._fechaIngreso = valor or ""

    @property
    def fechaRetiro(self):
        return self._fechaRetiro

    @fechaRetiro.setter
    def fechaRetiro(self, valor):
        if valor:
            try:
                datetime.strptime(valor, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Fecha de retiro inválida (DD/MM/AAAA)")
        self._fechaRetiro = valor or ""

    @property
    def indicadorContratado(self):
        return self._indicadorContratado

    @indicadorContratado.setter
    def indicadorContratado(self, valor):
        valor = int(valor)
        if valor not in (1, 2, 3):
            raise ValueError("Estado inválido (1=Activo, 2=Candidato, 3=Despedido)")
        self._indicadorContratado = valor

    @property
    def turno(self):
        return self._turno

    @turno.setter
    def turno(self, valor):
        valor = int(valor)
        if valor not in (1, 2):
            raise ValueError("Turno inválido (1=24H, 2=12H)")
        self._turno = valor

    @property
    def valorTurno(self):
        return self._valorTurno

    @valorTurno.setter
    def valorTurno(self, valor):
        self._valorTurno = float(valor or 0)

    @property
    def valorAhorro(self):
        return self._valorAhorro

    @valorAhorro.setter
    def valorAhorro(self, valor):
        self._valorAhorro = float(valor or 0)

    @property
    def valorAdeuda(self):
        return self._valorAdeuda

    @valorAdeuda.setter
    def valorAdeuda(self, valor):
        self._valorAdeuda = float(valor or 0)

    @property
    def totalAhorradoNoDevuelto(self):
        return self._totalAhorradoNoDevuelto

    @totalAhorradoNoDevuelto.setter
    def totalAhorradoNoDevuelto(self, valor):
        self._totalAhorradoNoDevuelto = float(valor or 0)

    # =========================
    # UTILIDAD PARA UI / REPO
    # =========================

    def como_tupla(self):
        return (
            self.noIdentificacion,
            self.nombreCompleto,
            self.direccion,
            self.telefono,
            self.correoElectronico,
            self.placaVehiculo,
            self.fechaIngreso,
            self.fechaRetiro,
            self.indicadorContratado,
            self.turno,
            self.valorTurno,
            self.valorAhorro,
            self.valorAdeuda,
            self.totalAhorradoNoDevuelto
        )
