from datetime import datetime

class Mantenimiento:

    def __init__(self, numeroOrden, placaVehiculo, nitProveedor,
                 nombreProveedor, descripcionServicio, valorFacturado,
                 fechaServicio):

        # Usamos setters para validar internamente
        self.numeroOrden = numeroOrden
        self.placaVehiculo = placaVehiculo
        self.nitProveedor = nitProveedor
        self.nombreProveedor = nombreProveedor
        self.descripcionServicio = descripcionServicio
        self.valorFacturado = valorFacturado
        self.fechaServicio = fechaServicio  # Debe llegar en DD/MM/AAAA

    # ===========================
    # GETTERS
    # ===========================
    @property
    def numeroOrden(self):
        return self.__numeroOrden

    @property
    def placaVehiculo(self):
        return self.__placaVehiculo

    @property
    def nitProveedor(self):
        return self.__nitProveedor

    @property
    def nombreProveedor(self):
        return self.__nombreProveedor

    @property
    def descripcionServicio(self):
        return self.__descripcionServicio

    @property
    def valorFacturado(self):
        return self.__valorFacturado

    @property
    def fechaServicio(self):
        return self.__fechaServicio

    # ===========================
    # SETTERS con validación
    # ===========================

    @numeroOrden.setter
    def numeroOrden(self, valor):
        if valor.strip() == "":
            raise ValueError("El número de orden no puede estar vacío.")
        self.__numeroOrden = valor

    @placaVehiculo.setter
    def placaVehiculo(self, valor):
        if valor.strip() == "":
            raise ValueError("La placa no puede estar vacía.")
        self.__placaVehiculo = valor

    @nitProveedor.setter
    def nitProveedor(self, valor):
        if valor.strip() == "":
            raise ValueError("El NIT no puede estar vacío.")
        self.__nitProveedor = valor

    @nombreProveedor.setter
    def nombreProveedor(self, valor):
        if valor.strip() == "":
            raise ValueError("El nombre del proveedor no puede estar vacío.")
        self.__nombreProveedor = valor

    @descripcionServicio.setter
    def descripcionServicio(self, valor):
        if valor.strip() == "":
            raise ValueError("La descripción del servicio no puede estar vacía.")
        self.__descripcionServicio = valor

    @valorFacturado.setter
    def valorFacturado(self, valor):
        try:
            valor = float(valor)
        except:
            raise ValueError("El valor facturado debe ser un número.")
        self.__valorFacturado = valor

    @fechaServicio.setter
    def fechaServicio(self, valor):
        # Debe venir en formato DD/MM/AAAA
        try:
            datetime.strptime(valor, "%d/%m/%Y")
        except:
            raise ValueError("La fecha debe estar en formato DD/MM/AAAA.")
        self.__fechaServicio = valor

    # ===========================
    # Para SQL
    # ===========================
    def como_tupla(self):
        return (
            self.__numeroOrden,
            self.__placaVehiculo,
            self.__nitProveedor,
            self.__nombreProveedor,
            self.__descripcionServicio,
            self.__valorFacturado,
            self.__fechaServicio
        )
