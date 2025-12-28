class Vehiculo:
    def __init__(self, placa, marca, referencia, modelo,
                 numero_chasis, numero_motor, color,
                 concesionario, fecha_compra_vehiculo,
                 tiempo_garantia, fecha_compra_poliza_seguro,
                 proveedor_poliza_seguro, fecha_compra_segObligatorio,
                 proveedor_segObligatorio, activo):

        self.placa = placa.upper()
        self.marca = marca
        self.referencia = referencia
        self.modelo = int(modelo)
        self.numero_chasis = numero_chasis
        self.numero_motor = numero_motor
        self.color = color
        self.concesionario = concesionario
        self.fecha_compra_vehiculo = fecha_compra_vehiculo
        self.tiempo_garantia = int(tiempo_garantia)
        self.fecha_compra_poliza_seguro = fecha_compra_poliza_seguro
        self.proveedor_poliza_seguro = proveedor_poliza_seguro
        self.fecha_compra_segObligatorio = fecha_compra_segObligatorio
        self.proveedor_segObligatorio = proveedor_segObligatorio
        self.activo = int(activo)

    def como_tupla(self):
        return (
            self.placa, self.marca, self.referencia, self.modelo,
            self.numero_chasis, self.numero_motor, self.color,
            self.concesionario, self.fecha_compra_vehiculo,
            self.tiempo_garantia, self.fecha_compra_poliza_seguro,
            self.proveedor_poliza_seguro, self.fecha_compra_segObligatorio,
            self.proveedor_segObligatorio, self.activo
        )
