# ==================================================================================
# MOLDE de un Vehículo — clase que contiene datos y lógica mínima del vehículo.
# ==================================================================================

class Vehiculo:
    """
    Representa un vehículo del sistema.
    El constructor normaliza placa a mayúsculas y convierte campos numéricos a int.
    """

    def __init__(
        self,
        placa: str,
        marca: str,
        referencia: str,
        modelo,
        numero_chasis: str,
        numero_motor: str,
        color: str,
        concesionario: str,
        fecha_compra_vehiculo: str,
        tiempo_garantia,
        fecha_compra_poliza_seguro: str,
        proveedor_poliza_seguro: str,
        fecha_compra_segObligatorio: str,
        proveedor_segObligatorio: str,
        activo
    ):
        # Normalizaciones y conversiones mínimas
        self._placa = placa.upper().strip()
        self._marca = marca.strip()
        self._referencia = referencia.strip()
        try:
            self._modelo = int(modelo)
        except (ValueError, TypeError):
            # si no se puede convertir aquí, dejar como está y validar en servicios
            self._modelo = modelo
        self._numero_chasis = numero_chasis.strip()
        self._numero_motor = numero_motor.strip()
        self._color = color.strip()
        self._concesionario = concesionario.strip()
        self._fecha_compra_vehiculo = fecha_compra_vehiculo.strip()
        try:
            self._tiempo_garantia = int(tiempo_garantia)
        except (ValueError, TypeError):
            self._tiempo_garantia = tiempo_garantia
        self._fecha_compra_poliza_seguro = fecha_compra_poliza_seguro.strip()
        self._proveedor_poliza_seguro = proveedor_poliza_seguro.strip()
        self._fecha_compra_segObligatorio = fecha_compra_segObligatorio.strip()
        self._proveedor_segObligatorio = proveedor_segObligatorio.strip()
        try:
            self._activo = int(activo)
        except (ValueError, TypeError):
            self._activo = activo

    # ---------------------------
    # Encapsulamiento / getters
    # ---------------------------
    @property
    def placa(self):
        """Placa en mayúsculas (solo lectura)."""
        return self._placa

    # ---------------------------
    # Serialización a tupla (orden SQL)
    # ---------------------------
    def infVehiculo(self):
        """
        Devuelve una tupla con los campos exactamente en el mismo orden
        que la tabla SQL 'vehiculos' para INSERT/UPDATE.
        """
        return (
            self._placa,
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

    # ---------------------------
    # Polizas: obtener y actualizar
    # ---------------------------
    def obtenerPolizas(self):
        """Devuelve un dict con la información de pólizas (consulta en memoria)."""
        return {
            "fecha_poliza": self._fecha_compra_poliza_seguro,
            "proveedor_poliza": self._proveedor_poliza_seguro,
            "fecha_seguro_obligatorio": self._fecha_compra_segObligatorio,
            "proveedor_seguro_obligatorio": self._proveedor_segObligatorio
        }

    def actualizaPoliza(
        self,
        nueva_fecha_compra_poliza_seguro: str,
        nueva_proveedor_poliza_seguro: str,
        nueva_fecha_compra_segObligatorio: str,
        nueva_proveedor_segObligatorio: str
    ):
        """Actualiza las pólizas en el objeto (cambios en memoria)."""
        self._fecha_compra_poliza_seguro = nueva_fecha_compra_poliza_seguro.strip()
        self._proveedor_poliza_seguro = nueva_proveedor_poliza_seguro.strip()
        self._fecha_compra_segObligatorio = nueva_fecha_compra_segObligatorio.strip()
        self._proveedor_segObligatorio = nueva_proveedor_segObligatorio.strip()

    # ---------------------------
    # Utilidades
    # ---------------------------
    def __repr__(self):
        return (
            f"Vehiculo(placa={self._placa}, marca={self._marca}, referencia={self._referencia}, "
            f"modelo={self._modelo}, activo={self._activo})"
        )
