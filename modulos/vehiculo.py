    # ==================================================================================
    # Es el MOLDE de mi Vehiculo, esta clase maneja los datos y la logica del vehiculo
    # ==================================================================================

class Vehiculo:
    # ---------------------------------------
    # 1. Constructor: recibe toda la info
    # ---------------------------------------
    
    def __init__(self, placa, marca, referencia, modelo, numero_chasis, numero_motor, color, concesionario, fecha_compra_vehiculo,
            tiempo_garantia, fecha_compra_poliza_seguro, proveedor_poliza_seguro, fecha_compra_segObligatorio, proveedor_segObligatorio, activo):
        
        # Usamos atributos privados "_" para proteger los datos
        self._placa = placa.upper().strip()
        self._marca = marca
        self._referencia = referencia
        self._modelo = int(modelo)
        self._numero_chasis = numero_chasis
        self._numero_motor = numero_motor
        self._color = color
        self._concesionario = concesionario
        self._fecha_compra_vehiculo = fecha_compra_vehiculo
        self._tiempo_garantia = int(tiempo_garantia)
        self._fecha_compra_poliza_seguro = fecha_compra_poliza_seguro
        self._proveedor_poliza_seguro = proveedor_poliza_seguro
        self._fecha_compra_segObligatorio = fecha_compra_segObligatorio
        self._proveedor_segObligatorio = proveedor_segObligatorio
        self._activo = int(activo)
    pass

    # Getter de la placa (Solo lectura, no modifica)
    @property
    def placa(self):
        return self._placa
    
    # Este metodo devuelve toda la info del vehiculo para guardarlo en la DB
    #Exactamente ene el mismo oren que la tabla de SQL 
    def infVehiculo(self):
        return(self._placa, 
               self._marca, 
               self._referencia, 
               self._modelo, 
               self._numero_chasis, 
               self._numero_motor, 
               self._color, 
               self._concesionario, 
               self._fecha_compra_vehiculo, 
               self._tiempo_garantia, 
               self._fecha_compra_poliza_seguro, 
               self._proveedor_poliza_seguro, 
               self._fecha_compra_segObligatorio, 
               self._proveedor_segObligatorio, 
               self._activo
               )
    
    @property
    #Getter para obtener las polizas y actualizrlas
    def obtenerPolizas(self):
        return {"fecha_poliza": self._fecha_compra_poliza_seguro,
                "proovedor_poliza": self._proveedor_poliza_seguro,
                "fecha_seguro_obligatorio": self._fecha_compra_segObligatorio,
                "proovedor_seguro_obligatorio": self._proveedor_segObligatorio}
   
    #Metodod para actualizar Polizas dentro del objeto
    def actualizaPoliza(self, nueva_fecha_compra_poliza_seguro, nueva_proveedor_poliza_seguro,
                        nueva_fecha_compra_segObligatorio, nueva_proveedor_segObligatorio):
        
        self._fecha_compra_poliza_seguro = nueva_fecha_compra_poliza_seguro
        self._proveedor_poliza_seguro = nueva_proveedor_poliza_seguro
        self._fecha_compra_segObligatorio = nueva_fecha_compra_segObligatorio
        self._proveedor_segObligatorio = nueva_proveedor_segObligatorio
        
