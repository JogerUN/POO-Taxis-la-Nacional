import sys
from menus.menu_base import Menu
from menus.menu_vehiculos import MenuVehiculos
from menus.menu_conductores import MenuConductores 
from menus.menu_mantenimientos import MenuMantenimientos
from tools.crear_pdf import generarFichaVehiculoPDF
from tools.validadores import convertirPlaca


class MenuPrincipal(Menu):

    def __init__(self):
        opciones = {
            "1": ("Módulo Vehículos", self.menuVehiculos),
            "2": ("Módulo Conductores", self.conductores),
            "3": ("Módulo Mantenimientos", self.mantenimientos),
            "4": ("Generar Ficha PDF del Vehículo", lambda: generarFichaVehiculoPDF(convertirPlaca("Placa: "))),
            "5": ("Salir", self.salir)
        }

        super().__init__("SISTEMA DE GESTIÓN - TAXIS LA NACIONAL", opciones)

    def menuVehiculos(self):
        MenuVehiculos().mostrar()

    def conductores(self):
        MenuConductores().mostrar()

    def mantenimientos(self):
        MenuMantenimientos().mostrar()

    def salir(self):
        print("\n👋 Gracias por usar el sistema. ¡Hasta luego!")
        sys.exit()
