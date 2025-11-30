from menus.menu_base import Menu
from servicios.conductor_servicios import (
    registrarConductor,
    consultarConductor,
    actualizarContacto,
    listarConductoresActivos
)
class MenuConductores(Menu):
    """
    Menú para gestionar conductores.
    Hereda de Menu para mantener estilo y flujo.
    """

    def __init__(self, connection):
        self.connection = connection

        # Opciones del menú, pasamos self.connection directamente
        opciones = {
            "1": ("Registrar Conductor", self.registrar),
            "2": ("Consultar Conductor", self.consultar),
            "3": ("Actualizar Contacto", self.actualizar_contacto),
            "4": ("Listar Conductores Activos", self.listar_activos),
            "5": ("Volver al Menú Principal", self.salir)
        }

        super().__init__("🚖 MÓDULO DE CONDUCTORES 🚖", opciones)

    # Métodos intermedios para pasar la conexión
    def registrar(self):
        registrarConductor(self.connection)

    def consultar(self):
        consultarConductor(self.connection)

    def actualizar_contacto(self):
        actualizarContacto(self.connection)

    def listar_activos(self):
        listarConductoresActivos(self.connection)

    def salir(self):
        print("\n🔙 Regresando al menú principal...\n")
        return "salir"
