
# servicios/conductor_servicios.py

from modulos.conductor import Conductor
from repositorios.conductor_repo import ConductorRepositorio
from datetime import datetime

# ------------------------------------------------------------
# UTILIDADES DE VALIDACIÓN
# ------------------------------------------------------------

def validar_fecha(fecha):
    if fecha.strip() == "":
        return ""  # permitido
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return fecha
    except:
        print("❌ Fecha inválida (formato DD/MM/AAAA).")
        return None

def validar_numero(texto, nombre):
    if texto.strip() == "":
        print(f"❌ El valor '{nombre}' no puede estar vacío.")
        return None
    try:
        return float(texto)
    except:
        print(f"❌ '{nombre}' debe ser numérico.")
        return None

# ------------------------------------------------------------
# REGISTRAR CONDUCTOR
# ------------------------------------------------------------

def registrarConductor(connection):
    repo = ConductorRepositorio(connection)
    print("\n--- REGISTRO DE NUEVO CONDUCTOR ---")

    noId = input("Número de identificación: ").strip()
    nombre = input("Nombre completo: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()
    correo = input("Correo electrónico: ").strip()
    placa = input("Placa del vehículo asignado: ").strip().upper()

    # Validar placa
    c = connection.cursor()
    c.execute("SELECT placa FROM vehiculos WHERE placa=?", (placa,))
    if not c.fetchone():
        print(f"❌ Error: La placa '{placa}' no existe en la BD.")
        return

    fechaIng = validar_fecha(input("Fecha de ingreso (DD/MM/AAAA o vacío): "))
    if fechaIng is None: return

    fechaRet = validar_fecha(input("Fecha de retiro (DD/MM/AAAA o vacío): "))
    if fechaRet is None: return

    estado = input("Estado (1=Activo / 2=Candidato / 3=Despedido): ").strip()
    while estado not in ('1','2','3'):
        print("❌ Estado inválido. Debe ser 1, 2 o 3.")
        estado = input("Estado (1=Activo / 2=Candidato / 3=Despedido): ").strip()

    turno = input("Turno (1=24 horas / 2=12 horas): ").strip()
    while turno not in ('1','2'):
        print("❌ Turno inválido. Debe ser 1 o 2.")
        turno = input("Turno (1=24 horas / 2=12 horas): ").strip()

    valorTurno = validar_numero(input("Valor del turno: "), "Valor del turno")
    if valorTurno is None: return

    valorAhorro = validar_numero(input("Valor ahorro: "), "Valor ahorro")
    if valorAhorro is None: return

    valorAdeuda = validar_numero(input("Valor adeudado: "), "Valor adeudado")
    if valorAdeuda is None: return

    totalNoDev = validar_numero(input("Total no devuelto: "), "Total no devuelto")
    if totalNoDev is None: return

    # Crear objeto Conductor
    conductor = Conductor(
        noId, nombre, direccion, telefono, correo, placa,
        fechaIng, fechaRet, estado, turno,
        valorTurno, valorAhorro, valorAdeuda, totalNoDev
    )

    # Guardar en BD
    if repo.guardar(conductor):
        print("✅ Conductor registrado correctamente.")

# ------------------------------------------------------------
# CONSULTAR CONDUCTOR
# ------------------------------------------------------------

def consultarConductor(connection):
    repo = ConductorRepositorio(connection)
    noId = input("ID del conductor: ").strip()

    conductor = repo.buscar_por_id(noId)
    if not conductor:
        print("❌ No existe ese conductor.")
        return

    # Mostrar toda la información
    print("\n--- INFORMACIÓN DEL CONDUCTOR ---")
    print(f"Nombre completo: {conductor.get_nombre()}")
    print(f"ID: {conductor.get_id()}")
    print(f"Dirección: {conductor._Conductor__direccion}")
    print(f"Teléfono: {conductor._Conductor__telefono}")
    print(f"Correo: {conductor._Conductor__correo}")
    print(f"Placa asignada: {conductor.get_placa()}")
    print(f"Fecha de ingreso: {conductor._Conductor__fechaIngreso}")
    print(f"Fecha de retiro: {conductor._Conductor__fechaRetiro}")
    print(f"Estado: {conductor.obtenerEstado()}")
    print(f"Turno: {'24 horas' if conductor._Conductor__turno=='1' else '12 horas'}")
    print(f"Valor del turno: {conductor._Conductor__valorTurno}")
    print(f"Valor ahorro: {conductor._Conductor__valorAhorro}")
    print(f"Valor adeudado: {conductor._Conductor__valorAdeuda}")
    print(f"Total no devuelto: {conductor._Conductor__totalNoDevuelto}")

# ------------------------------------------------------------
# ACTUALIZAR CONTACTO
# ------------------------------------------------------------

def actualizarContacto(connection):
    repo = ConductorRepositorio(connection)
    noId = input("ID del conductor: ").strip()

    conductor = repo.buscar_por_id(noId)
    if not conductor:
        print("❌ No existe ese conductor.")
        return

    print("\n--- DATOS ACTUALES ---")
    print("Dirección, teléfono y correo pueden actualizarse.")

    nuevaDir = input("Nueva dirección (enter para dejar igual): ")
    nuevoTel = input("Nuevo teléfono (enter para dejar igual): ")
    nuevoCorreo = input("Nuevo correo (enter para dejar igual): ")

    conductor.actualizarContacto(nuevaDir, nuevoTel, nuevoCorreo)
    repo.actualizar_contacto(conductor)

    print("✅ Datos actualizados.")

# ------------------------------------------------------------
# LISTAR CONDUCTORES ACTIVOS
# ------------------------------------------------------------

def listarConductoresActivos(connection):
    repo = ConductorRepositorio(connection)
    activos = repo.listar_activos()

    if not activos:
        print("⚠ No hay conductores activos.")
        return

    print("\n--- CONDUCTORES ACTIVOS ---")
    for c in activos:
        print(f"- {c.get_id()} | {c.get_nombre()} | {c.get_placa()} | Estado: {c.obtenerEstado()}")
