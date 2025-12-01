from menus.menu_base import Menu
from servicios.conductor_servicios import (
    registrarConductor,
    consultarConductor,
    actualizarConductor,
    listaConductoresActivos,
)

class MenuConductores(Menu):
    def __init__(self):
        opciones = {
            "1": ("Registrar conductor", registrarConductor),
            "2": ("Consultar conductor", consultarConductor),
            "3": ("Actualizar conductor", actualizarConductor),
            "4": ("Lista de conductores activos", listaConductoresActivos),
            "5": ("Volver al Menú Principal", self.salir)
        }
        super().__init__("🚖 MÓDULO DE CONDUCTORES 🚖", opciones)

    def salir(self):
        print("\n🔙 Regresando al menú principal...\n")
        return "salir"
