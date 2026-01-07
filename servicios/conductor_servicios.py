from datetime import datetime
from modulos.conductor import Conductor
from repositorios.conductor_repo import ConductorRepo
from database.connection import crearConexion

# ============================
# CONFIGURACIÓN
# ============================
connection = crearConexion()
repo = ConductorRepo(connection)

ESTADOS = {1: "Activo", 2: "Candidato", 3: "Despedido"}
TURNOS = {1: "24H", 2: "12H"}

# ============================
# REGISTRAR CONDUCTOR (UI)
# ============================
def registrarConductor(datos: dict):

    obligatorios = [
        "noIdentificacion", "nombreCompleto", "direccion",
        "telefono", "correoElectronico", "placaVehiculo",
        "indicadorContratado", "turno",
        "valorTurno", "valorAhorro",
        "valorAdeuda", "totalAhorradoNoDevuelto"
    ]

    for campo in obligatorios:
        if not datos.get(campo):
            raise ValueError(f"El campo {campo} es obligatorio")

    placa = datos["placaVehiculo"].upper()
    if not repo.placaExiste(placa):
        raise ValueError(f"La placa {placa} no existe")

    conductor = Conductor(
        datos["noIdentificacion"],
        datos["nombreCompleto"],
        datos["direccion"],
        datos["telefono"],
        datos["correoElectronico"],
        placa,
        datos.get("fechaIngreso", ""),
        datos.get("fechaRetiro", ""),
        datos["indicadorContratado"],
        datos["turno"],
        datos["valorTurno"],
        datos["valorAhorro"],
        datos["valorAdeuda"],
        datos["totalAhorradoNoDevuelto"]
    )

    repo.registrar(conductor)
    return "Conductor registrado correctamente"



# ============================
# CONSULTAR CONDUCTOR
# ============================
def consultarConductor(cedula: str):
    conductor = repo.consultar(cedula)
    if conductor is None:
        raise ValueError("Conductor no encontrado")
    return conductor


# ============================
# ACTUALIZAR CONDUCTOR
# ============================
def actualizarConductor(noIdentificacion: str, datos: dict):

    conductor = repo.consultar(noIdentificacion)
    if not conductor:
        raise ValueError("Conductor no encontrado")

    for campo, valor in datos.items():
        if hasattr(conductor, campo):
            setattr(conductor, campo, valor)

    repo.actualizar(conductor)
    return "Conductor actualizado correctamente"




# ============================
# LISTA DE CONDUCTORES ACTIVOS
# ============================
def listaConductoresActivos():
    filas = repo.listaActivos()
    if not filas:
        raise ValueError("No existen conductores activos registrados")
    return filas

