from menus.menu_base import Menu
from servicios.mantenimiento_servicios import (
    registrarMantenimiento,
    consultarMantenimiento,
    actualizarMantenimiento,
    borrarMantenimiento
)

class MenuMantenimientos(Menu):
    """
    Menú para gestionar mantenimientos.
    Usa herencia desde Menu y polimorfismo en salir().
    """

    def __init__(self):
        opciones = {
            "1": ("Registrar Mantenimiento", registrarMantenimiento),
            "2": ("Consultar Mantenimiento", consultarMantenimiento),
            "3": ("Actualizar Mantenimiento", actualizarMantenimiento),
            "4": ("Borrar Mantenimiento", borrarMantenimiento),
            "5": ("Volver al Menú Principal", self.salir)
        }

        super().__init__("🛠️ MÓDULO DE MANTENIMIENTOS 🛠️", opciones)

    def salir(self):
        print("\n🔙 Regresando al menú principal...\n")
        return "salir"
