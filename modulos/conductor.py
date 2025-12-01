class Conductor:
    def __init__(self, noIdentificacion, nombreCompleto, direccion, telefono, correoElectronico,
                 placaVehiculo, fechaIngreso=None, fechaRetiro=None, indicadorContratado=1,
                 turno=1, valorTurno=0, valorAhorro=0, valorAdeuda=0, totalAhorradoNoDevuelto=0):
        self._noIdentificacion = noIdentificacion
        self._nombreCompleto = nombreCompleto
        self._direccion = direccion
        self._telefono = telefono
        self._correoElectronico = correoElectronico
        self._placaVehiculo = placaVehiculo
        self._fechaIngreso = fechaIngreso
        self._fechaRetiro = fechaRetiro
        self._indicadorContratado = indicadorContratado
        self._turno = turno
        self._valorTurno = valorTurno
        self._valorAhorro = valorAhorro
        self._valorAdeuda = valorAdeuda
        self._totalAhorradoNoDevuelto = totalAhorradoNoDevuelto

    # ------------------- Getters y Setters -------------------

    @property
    def noIdentificacion(self):
        return self._noIdentificacion

    @noIdentificacion.setter
    def noIdentificacion(self, valor):
        if not valor:
            raise ValueError("La identificación no puede estar vacía")
        self._noIdentificacion = valor

    @property
    def nombreCompleto(self):
        return self._nombreCompleto

    @nombreCompleto.setter
    def nombreCompleto(self, valor):
        if not valor:
            raise ValueError("El nombre completo no puede estar vacío")
        self._nombreCompleto = valor

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = valor or ""

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor or ""

    @property
    def correoElectronico(self):
        return self._correoElectronico

    @correoElectronico.setter
    def correoElectronico(self, valor):
        self._correoElectronico = valor or ""

    @property
    def placaVehiculo(self):
        return self._placaVehiculo

    @placaVehiculo.setter
    def placaVehiculo(self, valor):
        if not valor:
            raise ValueError("La placa no puede estar vacía")
        self._placaVehiculo = valor

    @property
    def fechaIngreso(self):
        return self._fechaIngreso

    @fechaIngreso.setter
    def fechaIngreso(self, valor):
        self._fechaIngreso = valor or ""

    @property
    def fechaRetiro(self):
        return self._fechaRetiro

    @fechaRetiro.setter
    def fechaRetiro(self, valor):
        self._fechaRetiro = valor or ""

    @property
    def indicadorContratado(self):
        return self._indicadorContratado

    @indicadorContratado.setter
    def indicadorContratado(self, valor):
        if valor not in [1, 2, 3]:
            raise ValueError("Indicador contratado debe ser 1, 2 o 3")
        self._indicadorContratado = valor

    @property
    def turno(self):
        return self._turno

    @turno.setter
    def turno(self, valor):
        if valor not in [1, 2]:
            raise ValueError("Turno debe ser 1 o 2")
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
