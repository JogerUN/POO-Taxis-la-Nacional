from datetime import datetime
from modulos.mantenimiento import Mantenimiento
from repositorios.mantenimiento_repo import RepositorioMantenimiento
from repositorios.vehiculo_repo import RepositorioVehiculo
from database.connection import crearConexion

connection = crearConexion()
repo = RepositorioMantenimiento(connection)
repoVehiculo = RepositorioVehiculo(connection)

# ============================
# REGISTRAR (UI)
# ============================
def registrarMantenimiento(datos: dict):

    obligatorios = [
        "numeroOrden", "placaVehiculo", "nitProveedor",
        "nombreProveedor", "descripcionServicio",
        "valorFacturado", "fechaServicio"
    ]

    for campo in obligatorios:
        if not datos.get(campo):
            raise ValueError(f"El campo {campo} es obligatorio")

    placa = datos["placaVehiculo"].upper()
    if not repoVehiculo.buscar_por_placa(placa):
        raise ValueError("La placa no existe")

    mantenimiento = Mantenimiento(
        datos["numeroOrden"],
        placa,
        datos["nitProveedor"],
        datos["nombreProveedor"],
        datos["descripcionServicio"],
        datos["valorFacturado"],
        datos["fechaServicio"]
    )

    repo.crear(mantenimiento)
    return "Mantenimiento registrado correctamente"


# ============================
# CONSULTAR
# ============================
def consultarMantenimiento(numeroOrden: str):
    mant = repo.buscar(numeroOrden)
    if not mant:
        raise ValueError("Mantenimiento no encontrado")
    return mant


# ============================
# ACTUALIZAR
# ============================
def actualizarMantenimiento(numeroOrden: str, datos: dict):

    mant = repo.buscar(numeroOrden)
    if not mant:
        raise ValueError("Mantenimiento no encontrado")

    if "placaVehiculo" in datos:
        placa = datos["placaVehiculo"].upper()
        if not repoVehiculo.buscar_por_placa(placa):
            raise ValueError("La placa no existe")
        mant.placaVehiculo = placa

    for campo in [
        "nitProveedor", "nombreProveedor",
        "descripcionServicio", "valorFacturado",
        "fechaServicio"
    ]:
        if campo in datos and datos[campo]:
            setattr(mant, campo, datos[campo])

    repo.actualizar(mant)
    return "Mantenimiento actualizado correctamente"


# ============================
# BORRAR
# ============================
def borrarMantenimiento(numeroOrden: str):
    filas = repo.borrar(numeroOrden)
    if filas == 0:
        raise ValueError("No se encontró el mantenimiento")
    return "Mantenimiento eliminado"
