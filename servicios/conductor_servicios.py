# conductor_servicios.py
from repositorios.conductor_repo import ConductorRepo
from modulos.conductor import Conductor
from database.connection import crearConexion

connection = crearConexion()
repo = ConductorRepo()

# Diccionarios para traducir indicadores y turnos
ESTADOS = {1: "Activo", 2: "Candidato", 3: "Despedido"}
TURNOS = {1: "24H", 2: "12H"}

def registrarConductor():
    print("\n--- REGISTRAR CONDUCTOR ---")
    placa = input("Placa del vehículo: ").strip().upper()
    if not repo.placaExiste(placa):
        print(f"❌ Error: La placa '{placa}' no existe.")
        return

    noIdentificacion = input("Número de identificación: ").strip()
    nombreCompleto = input("Nombre completo: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()
    correoElectronico = input("Correo electrónico: ").strip()
    fechaIngreso = input("Fecha de ingreso (DD/MM/AAAA o vacío): ").strip() or " "
    fechaRetiro = input("Fecha de retiro (DD/MM/AAAA o vacío): ").strip() or " "
    indicadorContratado = int(input("Estado (1=Activo,2=Candidato,3=Despedido): ").strip() or 1)
    turno = int(input("Turno (1=24h,2=12h): ").strip() or 1)
    valorTurno = float(input("Valor Turno: ").strip() or 0)
    valorAhorro = float(input("Valor Ahorro: ").strip() or 0)
    valorAdeuda = float(input("Valor Adeuda: ").strip() or 0)
    totalAhorradoNoDevuelto = float(input("Total no devuelto: ").strip() or 0)

    conductor = Conductor(
        noIdentificacion, nombreCompleto, direccion, telefono, correoElectronico,
        placa, fechaIngreso, fechaRetiro, indicadorContratado, turno,
        valorTurno, valorAhorro, valorAdeuda, totalAhorradoNoDevuelto
    )

    print(repo.registrar(conductor))


def consultarConductor():
    noId = input("Número de identificación del conductor: ").strip()
    fila = repo.consultar(noId)
    if not fila:
        print("❌ No se encontró información del conductor.")
        return

    estado = ESTADOS.get(fila[8], "Desconocido")
    turnoTexto = TURNOS.get(fila[9], "No definido")

    print(f'''
--- INFORMACIÓN DEL CONDUCTOR ---
IDENTIFICACIÓN: {fila[0]}
NOMBRE COMPLETO: {fila[1]}
DIRECCIÓN: {fila[2]}
TELÉFONO: {fila[3]}
CORREO: {fila[4]}
PLACA VEHÍCULO: {fila[5]}
FECHA INGRESO: {fila[6]}
FECHA RETIRO: {fila[7]}
ESTADO: {estado}
TURNO: {turnoTexto}
VALOR TURNO: {fila[10]}
VALOR AHORRO: {fila[11]}
VALOR ADEUDA: {fila[12]}
TOTAL NO DEVUELTO: {fila[13]}
''')


def actualizarConductor():
    noId = input("Número de identificación del conductor a actualizar: ").strip()
    fila = repo.consultar(noId)
    if not fila:
        print("❌ No se encontró el conductor.")
        return

    conductor = Conductor(
        noIdentificacion=fila[0],
        nombreCompleto=fila[1],
        direccion=fila[2],
        telefono=fila[3],
        correoElectronico=fila[4],
        placaVehiculo=fila[5],
        fechaIngreso=fila[6],
        fechaRetiro=fila[7],
        indicadorContratado=fila[8],
        turno=fila[9],
        valorTurno=fila[10],
        valorAhorro=fila[11],
        valorAdeuda=fila[12],
        totalAhorradoNoDevuelto=fila[13]
    )

    print(f"\nActualizando conductor: {conductor.nombreCompleto}")
    print("Deje vacío para mantener el valor actual.\n")

    # Actualizar placa con verificación
    nueva_placa = input(f"Placa del vehículo ({conductor.placaVehiculo}): ").strip().upper()
    if nueva_placa:
        if not repo.placaExiste(nueva_placa):
            print(f"❌ Error: La placa '{nueva_placa}' no existe. No se puede actualizar.")
            return
        conductor.placaVehiculo = nueva_placa

    conductor.direccion = input(f"Dirección ({conductor.direccion}): ").strip() or conductor.direccion
    conductor.telefono = input(f"Teléfono ({conductor.telefono}): ").strip() or conductor.telefono
    conductor.correoElectronico = input(f"Correo ({conductor.correoElectronico}): ").strip() or conductor.correoElectronico
    conductor.fechaIngreso = input(f"Fecha ingreso ({conductor.fechaIngreso}): ").strip() or conductor.fechaIngreso
    conductor.fechaRetiro = input(f"Fecha retiro ({conductor.fechaRetiro}): ").strip() or conductor.fechaRetiro

    # Estado y Turno mostrando texto
    actual_estado = ESTADOS.get(conductor.indicadorContratado, "Desconocido")
    indicador = input(f"Estado ({actual_estado}) \n[1: Activo, 2: Candidato, 3: Despedido]: ").strip()
    if indicador in ["1", "2", "3"]:
        conductor.indicadorContratado = int(indicador)

    actual_turno = TURNOS.get(conductor.turno, "Desconocido")
    turno = input(f"Turno ({actual_turno}) \n[1: 24H, 2: 12H]: ").strip()
    if turno in ["1", "2"]:
        conductor.turno = int(turno)

    valorAdeuda = input(f"Valor adeudado ({conductor.valorAdeuda}): ").strip()
    conductor.valorAdeuda = float(valorAdeuda) if valorAdeuda else conductor.valorAdeuda
    totalNoDevuelto = input(f"Total no devuelto ({conductor.totalAhorradoNoDevuelto}): ").strip()
    conductor.totalAhorradoNoDevuelto = float(totalNoDevuelto) if totalNoDevuelto else conductor.totalAhorradoNoDevuelto

    print(repo.actualizar(conductor))


def listaConductoresActivos():
    activos = repo.listaActivos()
    if not activos:
        print("No hay conductores activos.")
        return

    print("\n--- CONDUCTORES ACTIVOS ---")
    print("Identificación | Nombre | Placa")
    for c in activos:
        print(f"{c[0]} | {c[1]} | {c[2]}")


