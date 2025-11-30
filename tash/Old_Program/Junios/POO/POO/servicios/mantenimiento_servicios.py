from repositorios.mantenimiento_repo import RepositorioMantenimiento
from modulos.mantenimiento import Mantenimiento
from database.connection import crearConexion
from datetime import datetime

connection = crearConexion()
repo = RepositorioMantenimiento(connection)

def registrarMantenimiento():
    print("\n--- REGISTRAR MANTENIMIENTO ---")

    try:
        numeroOrden = input("Número de Orden: ")
        placa = input("Placa: ")
        nit = input("Nit: ")
        proveedor = input("Proveedor: ")
        servicio = input("Servicio Prestado: ")
        valor = input("Valor Facturado: ")

        while True:
            fecha = input("Fecha (dd/mm/aaaa): ")
            try:
                fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
                fecha_fmt = fecha_dt.strftime("%Y-%m-%d")
                break
            except:
                print("Fecha inválida, intente de nuevo.")

        mant = Mantenimiento(
            numeroOrden, placa, nit, proveedor,
            servicio, valor, fecha_fmt
        )

        repo.crear(mant)
        print("Mantenimiento registrado correctamente.")

    except Exception as e:
        print("Error:", e)

def consultarMantenimiento():
    numero = input("Número de Orden: ")
    mant = repo.buscar(numero)

    if mant is None:
        print("No existe un mantenimiento con ese número.")
        return

    print("\n--- INFORMACIÓN DEL MANTENIMIENTO ---")
    print("Orden:", mant.numeroOrden)
    print("Placa:", mant.placaVehiculo)
    print("Proveedor:", mant.nombreProveedor)
    print("Nit:", mant.nitProveedor)
    print("Servicio:", mant.descripcionServicio)
    print("Valor:", mant.valorFacturado)
    print("Fecha:", mant.fechaServicio)

def actualizarMantenimiento():
    numero = input("Número Orden a actualizar: ")
    mant = repo.buscar(numero)

    if mant is None:
        print("No existe.")
        return

    try:
        mant.placaVehiculo = input("Nueva Placa: ")
        mant.nitProveedor = input("Nuevo Nit: ")
        mant.nombreProveedor = input("Nuevo Proveedor: ")
        mant.descripcionServicio = input("Nuevo Servicio: ")
        mant.valorFacturado = input("Nuevo Valor: ")

        while True:
            fecha = input("Nueva Fecha (dd/mm/aaaa): ")
            try:
                fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
                mant.fechaServicio = fecha_dt.strftime("%Y-%m-%d")
                break
            except:
                print("Fecha inválida.")

        repo.actualizar(mant)
        print("Actualizado correctamente.")

    except Exception as e:
        print("Error:", e)

def borrarMantenimiento():
    numero = input("Número de Orden: ")
    filas = repo.borrar(numero)

    if filas == 0:
        print("No se encontró ese mantenimiento.")
    else:
        print("Eliminado correctamente.")
