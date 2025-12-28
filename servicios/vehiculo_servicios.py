from datetime import datetime
from modulos.vehiculo import Vehiculo
from repositorios.vehiculo_repo import RepositorioVehiculo
from database.connection import crearConexion

connection = crearConexion()
repo = RepositorioVehiculo(connection)

# ============================
# REGISTRAR VEHÍCULO (UI)
# ============================
def registrarVehiculo(datos: dict):

    obligatorios = [
        "placa", "marca", "referencia", "modelo",
        "numero_chasis", "numero_motor", "color",
        "concesionario", "fecha_compra_vehiculo",
        "tiempo_garantia", "fecha_compra_poliza_seguro",
        "proveedor_poliza_seguro", "fecha_compra_segObligatorio",
        "proveedor_segObligatorio", "activo"
    ]

    for campo in obligatorios:
        if not datos.get(campo):
            raise ValueError(f"El campo {campo} es obligatorio")

    # Validaciones de formato
    for fecha in [
        "fecha_compra_vehiculo",
        "fecha_compra_poliza_seguro",
        "fecha_compra_segObligatorio"
    ]:
        try:
            datetime.strptime(datos[fecha], "%d/%m/%Y")
        except:
            raise ValueError(f"Fecha inválida en {fecha}")

    vehiculo = Vehiculo(**datos)
    repo.guardar(vehiculo)

# ============================
# CONSULTAR VEHÍCULO
# ============================
def consultarVehiculo(placa: str):
    vehiculo = repo.buscar_por_placa(placa)
    if vehiculo is None:
        raise ValueError("Vehículo no encontrado")
    return vehiculo

# ============================
# ACTUALIZAR ESTADO DEL VEHÍCULO
# ============================
def actualizarEstado(placa: str, nuevo_estado: int):
    if nuevo_estado not in [1, 2]:
        raise ValueError("Estado inválido")    
    repo.actualizarEstado(placa, nuevo_estado)
    
# ===========================================================
#   ACTUALIZAR POLIZAS DEL VEHÍCULO
# ===========================================================
from datetime import datetime

def actualizarPolizaVehiculo(placa: str, datos: dict):
    vehiculo = repo.buscar_por_placa(placa)
    if vehiculo is None:
        raise ValueError("Vehículo no encontrado")

    obligatorios = [
        "fecha_compra_poliza_seguro",
        "proveedor_poliza_seguro",
        "fecha_compra_segObligatorio",
        "proveedor_segObligatorio"
    ]

    for campo in obligatorios:
        if not datos.get(campo):
            raise ValueError(f"El campo {campo} es obligatorio")

    # Validar fechas
    try:
        nueva_poliza = datetime.strptime(datos["fecha_compra_poliza_seguro"], "%d/%m/%Y")
        nuevo_soat = datetime.strptime(datos["fecha_compra_segObligatorio"], "%d/%m/%Y")
    except:
        raise ValueError("Formato de fecha inválido (DD/MM/AAAA)")

    fecha_poliza_actual = datetime.strptime(
        vehiculo.fecha_compra_poliza_seguro, "%d/%m/%Y"
    )
    fecha_soat_actual = datetime.strptime(
        vehiculo.fecha_compra_segObligatorio, "%d/%m/%Y"
    )

    if nueva_poliza <= fecha_poliza_actual:
        raise ValueError("La nueva fecha de póliza debe ser mayor a la actual")

    if nuevo_soat <= fecha_soat_actual:
        raise ValueError("La nueva fecha de SOAT debe ser mayor a la actual")
    
    repo.actualizar_poliza(placa, datos)

def listaVehiculosActivos():
    filas = repo.lista_activos()
    if not filas:
        raise ValueError("No existen vehículos activos registrados")
    return filas