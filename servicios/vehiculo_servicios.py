# servicios/vehiculo_servicios.py
# ===========================================================
#     LÓGICA DE NEGOCIO / CONTROLADOR DEL MÓDULO VEHÍCULOS
# ===========================================================

from modulos.vehiculo import Vehiculo
from repositorios.vehiculo_repo import RepositorioVehiculo
from tools.validadores import (
    inputObligatorio,
    validarFecha,
    validarEntero,
    convertirPlaca
)
from database.connection import crearConexion


# ===========================================================
#   CONFIGURACIÓN INICIAL DEL MÓDULO
# ===========================================================

connection = crearConexion()
repo = RepositorioVehiculo(connection)


# ===========================================================
#   REGISTRAR VEHÍCULO
# ===========================================================
def registrarVehiculo():
    print("\n--- REGISTRAR NUEVO VEHÍCULO ---")

    datos = {
        "placa": convertirPlaca("Placa: "),
        "marca": inputObligatorio("Marca: "),
        "referencia": inputObligatorio("Referencia: "),
        "modelo": validarEntero("Modelo: "),
        "numero_chasis": inputObligatorio("Número de chasis: "),
        "numero_motor": inputObligatorio("Número de motor: "),
        "color": inputObligatorio("Color: "),
        "concesionario": inputObligatorio("Concesionario: "),
        "fecha_compra_vehiculo": validarFecha("Fecha de compra (DD/MM/AAAA): "),
        "tiempo_garantia": validarEntero("Garantía (meses): "),
        "fecha_compra_poliza_seguro": validarFecha("Fecha compra póliza seguro (DD/MM/AAAA): "),
        "proveedor_poliza_seguro": inputObligatorio("Proveedor póliza de seguro: "),
        "fecha_compra_segObligatorio": validarFecha("Fecha compra seguro obligatorio (DD/MM/AAAA): "),
        "proveedor_segObligatorio": inputObligatorio("Proveedor seguro obligatorio: "),
        "activo": validarEntero("Activo (1=Sí / 2=No): ", ["1", "2"])
    }

    vehiculo = Vehiculo(**datos)

    try:
        repo.guardar(vehiculo)
        print("✅ Vehículo registrado correctamente.")
    except Exception as e:
        print("❌ Error al registrar vehículo:", e)


# ===========================================================
#   CONSULTAR VEHÍCULO
# ===========================================================
def consultarVehiculo():
    print("\n=== CONSULTA DE VEHÍCULO ===\n")

    placa = convertirPlaca("Placa del vehículo a consultar: ")
    vehiculo = repo.buscar_por_placa(placa)

    if vehiculo is None:
        print(f"⚠️ No se encontró ningún vehículo registrado con la placa {placa}.")
        return

    print(f"\n=== Información del Vehículo {placa} ===")
    etiquetas = [
        "Placa", "Marca", "Referencia", "Modelo", "Número chasis",
        "Número motor", "Color", "Concesionario", "Fecha compra",
        "Garantía (meses)", "Fecha póliza", "Proveedor póliza",
        "Fecha SOAT", "Proveedor SOAT", "Activo"
    ]

    for etiqueta, valor in zip(etiquetas, vehiculo.infVehiculo()):
        print(f"{etiqueta}: {valor}")

    print()


# ===========================================================
#   ACTUALIZAR ESTADO (ACTIVO / INACTIVO)
# ===========================================================
def actualizarEstadoVehiculo():
    print("\n=== ACTUALIZAR ESTADO DEL VEHÍCULO ===\n")

    placa = convertirPlaca("Placa del vehículo a actualizar: ")
    vehiculo = repo.buscar_por_placa(placa)

    if vehiculo is None:
        print(f"⚠️ No se encontró un vehículo registrado con la placa {placa}.")
        return

    nuevo_estado = validarEntero("Nuevo estado (1=Activo, 2=Inactivo): ", ["1", "2"])
    repo.actualizar_estado(placa, nuevo_estado)

    print("✅ Estado actualizado correctamente.")


# ===========================================================
#   ACTUALIZAR POLIZAS DEL VEHÍCULO
# ===========================================================
def actualizarPolizaVehiculo():
    print("\n--- ACTUALIZAR PÓLIZAS ---")

    placa = convertirPlaca("Placa del vehículo a actualizar: ")
    vehiculo = repo.buscar_por_placa(placa)

    if vehiculo is None:
        print(f"⚠️ No se encontró un vehículo registrado con la placa {placa}.")
        return

    # Mostrar pólizas actuales
    polizas = vehiculo.obtenerPolizas()
    print(f"\n Póliza Actual → Fecha: {polizas['fecha_poliza']} | Proveedor: {polizas['proveedor_poliza']}")
    print(f" SOAT Actual   → Fecha: {polizas['fecha_seguro_obligatorio']} | Proveedor: {polizas['proveedor_seguro_obligatorio']}")

    # Solicitar nuevos datos
    nueva_fecha_poliza = validarFecha("\nNueva fecha póliza (DD/MM/AAAA): ")
    nuevo_proveedor_poliza = inputObligatorio("Nuevo proveedor póliza: ")

    nueva_fecha_soat = validarFecha("Nueva fecha SOAT (DD/MM/AAAA): ")
    nuevo_proveedor_soat = inputObligatorio("Nuevo proveedor SOAT: ")

    # Actualizar objeto en memoria
    vehiculo.actualizaPoliza(
        nueva_fecha_compra_poliza_seguro=nueva_fecha_poliza,
        nueva_proveedor_poliza_seguro=nuevo_proveedor_poliza,
        nueva_fecha_compra_segObligatorio=nueva_fecha_soat,
        nueva_proveedor_segObligatorio=nuevo_proveedor_soat
    )

    # Persistir
    repo.actualizar_poliza(vehiculo)
    print("✅ Pólizas actualizadas correctamente.")


# ===========================================================
#   LISTA DE VEHÍCULOS ACTIVOS
# ===========================================================
def listaVehiculosActivos():
    filas = repo.lista_activos()

    if not filas:
        print("\n⚠️ No existen vehículos activos registrados.")
        return

    print("\n--- LISTA DE VEHÍCULOS ACTIVOS ---")
    for row in filas:
        print(f"Placa: {row[0]}  Marca: {row[1]}  Ref: {row[2]}  Modelo: {row[3]}  Color: {row[4]}")

    print(f"\nTotal vehículos activos: {len(filas)}")
