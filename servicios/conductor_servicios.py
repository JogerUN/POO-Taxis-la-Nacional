from repositorios.conductor_repo import ConductorRepo
from modulos.conductor import Conductor
from database.connection import crearConexion
from datetime import datetime

connection = crearConexion()
repo = ConductorRepo()

# Diccionarios para traducir indicadores y turnos
ESTADOS = {1: "Activo", 2: "Candidato", 3: "Despedido"}
TURNOS = {1: "24H", 2: "12H"}

def registrarConductor():
    #placa
    print("\n--- REGISTRAR CONDUCTOR ---")
    placa = input("Placa del vehículo: ").strip().upper()
    if not repo.placaExiste(placa):
        print(f"❌ Error: La placa '{placa}' no existe.")
        return
    #identificacion
    while True:
        noIdentificacion = input("Número de identificación: ").strip()
        if noIdentificacion.isdigit():
            noIdentificacion = int(noIdentificacion)
            break
        print("❌ Numero no valido.")

    nombreCompleto = input("Nombre completo: ").strip()
    direccion = input("Dirección: ").strip()

    # Teléfono
    while True:
        telefono = input("Teléfono: ").strip()
        if telefono.isdigit():
            break
        print("❌ Solo se aceptan números enteros.")

    correoElectronico = input("Correo electrónico: ").strip()

    # Fecha de ingreso
    while True:
        fechaIngreso = input("Fecha de ingreso (DD/MM/AAAA o vacío): ").strip()
        if fechaIngreso == "":
            fechaIngreso = " "
            break
        try:
            datetime.strptime(fechaIngreso, "%d/%m/%Y")
            break
        except ValueError:
            print("❌ Formato incorrecto. Debe ser DD/MM/AAAA.")

    # Fecha de retiro
    while True:
        fechaRetiro = input("Fecha de retiro (DD/MM/AAAA o vacío): ").strip()
        if fechaRetiro == "":
            fechaRetiro = " "
            break
        try:
            datetime.strptime(fechaRetiro, "%d/%m/%Y")
            break
        except ValueError:
            print("❌ Formato incorrecto. Debe ser DD/MM/AAAA.")

    # Estado
    while True:
        indicadorContratado = input("Estado (1=Activo,2=Candidato,3=Despedido): ").strip()
        if indicadorContratado in {"1","2","3"}:
            indicadorContratado = int(indicadorContratado)
            break
        print("❌ Opción inválida. Debe ser 1, 2 o 3.")

    # Turno
    while True:
        turno = input("Turno (1=24h,2=12h): ").strip()
        if turno in {"1","2"}:
            turno = int(turno)
            break
        print("❌ Opción inválida. Debe ser 1 o 2.")

    # Valores numéricos
    def pedir_numero(prompt):
        while True:
            valor = input(prompt).strip()
            try:
                return float(valor)
            except ValueError:
                print("❌ Solo se aceptan números.")

    valorTurno = pedir_numero("Valor Turno: ")
    valorAhorro = pedir_numero("Valor Ahorro: ")
    valorAdeuda = pedir_numero("Valor Adeuda: ")
    totalAhorradoNoDevuelto = pedir_numero("Total no devuelto: ")

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
    
    # Teléfono
    while True:
        telefono = input(f"Teléfono ({conductor.telefono}): ").strip()
        if telefono == "":
            break
        if telefono.isdigit():
            conductor.telefono = telefono
            break
        print("❌ Dato invalido.")

    conductor.correoElectronico = input(f"Correo ({conductor.correoElectronico}): ").strip() or conductor.correoElectronico
    
    # Fecha de ingreso
    while True:
        fecha = input(f"Fecha ingreso ({conductor.fechaIngreso}): ").strip()
        if fecha == "":
            break
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            conductor.fechaIngreso = fecha
            break
        except ValueError:
            print("❌ Formato incorrecto. Debe ser DD/MM/AAAA.")

    # Fecha de retiro
    while True:
        fecha = input(f"Fecha retiro ({conductor.fechaRetiro}): ").strip()
        if fecha == "":
            break
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            conductor.fechaRetiro = fecha
            break
        except ValueError:
            print("❌ Formato incorrecto. Debe ser DD/MM/AAAA.")

    # Estado
    while True:
        actual_estado = ESTADOS.get(conductor.indicadorContratado, "Desconocido")
        indicador = input(f"Estado ({actual_estado}) \n[1: Activo, 2: Candidato, 3: Despedido]: ").strip()
        if indicador == "":
            # Dejar valor actual
            break
        if indicador in {"1", "2", "3"}:
            conductor.indicadorContratado = int(indicador)
            break
        print("❌ Opción inválida. Debe ser 1, 2 o 3.")

# Turno
    while True:
        actual_turno = TURNOS.get(conductor.turno, "Desconocido")
        turno = input(f"Turno ({actual_turno}) \n[1: 24H, 2: 12H]: ").strip()
        if turno == "":
            break
        if turno in {"1", "2"}:
            conductor.turno = int(turno)
            break
        print("❌ Opción inválida. Debe ser 1 o 2.")

    # Valores numéricos
    def pedir_numero(prompt, actual):
        while True:
            valor = input(f"{prompt} ({actual}): ").strip()
            if valor == "":
                return actual
            try:
                return float(valor)
            except ValueError:
                print("❌ Solo se aceptan números.")

    conductor.valorTurno = pedir_numero("Valor Turno", conductor.valorTurno)
    conductor.valorAhorro = pedir_numero("Valor Ahorro", conductor.valorAhorro)
    conductor.valorAdeuda = pedir_numero("Valor adeudado", conductor.valorAdeuda)
    conductor.totalAhorradoNoDevuelto = pedir_numero("Total no devuelto", conductor.totalAhorradoNoDevuelto)

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


