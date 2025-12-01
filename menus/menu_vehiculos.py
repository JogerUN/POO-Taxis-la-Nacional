from menus.menu_base import Menu
from servicios.vehiculo_servicios import (
    registrarVehiculo,
    consultarVehiculo,
    actualizarEstadoVehiculo,
    actualizarPolizaVehiculo,
    listaVehiculosActivos
)

class MenuVehiculos(Menu):
    """
    Menú para gestionar vehículos.
    Demuestra herencia y polimorfismo sobrescribiendo salir().
    """

    def __init__(self):
        opciones = {
            "1": ("Registrar Vehículo", registrarVehiculo),
            "2": ("Consultar Vehículo", consultarVehiculo),
            "3": ("Actualizar Estado del Vehículo", actualizarEstadoVehiculo),
            "4": ("Actualizar Pólizas del Vehículo", actualizarPolizaVehiculo),
            "5": ("Listar Vehículos Activos", listaVehiculosActivos),
            "6": ("Volver al Menú Principal", self.salir)
        }

        super().__init__("🚕 MÓDULO DE VEHÍCULOS 🚕", opciones)

    def salir(self):
        print("\n🔙 Regresando al menú principal...\n")
        return "salir"
