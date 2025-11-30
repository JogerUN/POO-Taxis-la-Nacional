import sys
from menus.menu_base import Menu
from menus.menu_vehiculos import MenuVehiculos
from menus.menu_conductores import MenuConductores
from database.connection import crearConexion  # <-- IMPORTAR CONEXIÓN

class MenuPrincipal(Menu):

    def __init__(self):
        # Crear la conexión una sola vez
        self.connection = crearConexion()

        opciones = {
            "1": ("Módulo Vehículos", self.menuVehiculos),
            "2": ("Módulo Conductores", self.conductores),
            "3": ("Módulo Mantenimientos (Próximamente)", self.mantenimientos),
            "4": ("Salir", self.salir)
        }

        super().__init__("SISTEMA DE GESTIÓN - TAXIS LA NACIONAL", opciones)

    def menuVehiculos(self):
        MenuVehiculos().mostrar()  

    def conductores(self):
        MenuConductores(self.connection).mostrar() 

    def mantenimientos(self):
        print("\n🚧 Módulo de Mantenimientos en desarrollo…\n")

    def salir(self):
        print("\n👋 Gracias por usar el sistema. ¡Hasta luego!")
        sys.exit()
