import sys
from menus.menu_base import Menu
from menus.menu_mantenimientos import MenuMantenimientos


class MenuPrincipal(Menu):

    def __init__(self):
        opciones = {
            "2": ("Módulo Conductores (Próximamente)", self.conductores),
            "3": ("Módulo Mantenimientos", self.menuMantenimientos),
            "4": ("Salir", self.salir)
        }

        super().__init__("SISTEMA DE GESTIÓN - TAXIS LA NACIONAL", opciones)

    # ==== Menú de mantenimientos ====
    def menuMantenimientos(self):
        MenuMantenimientos().mostrar()

    # ==== Conductores aún no implementado ====
    def conductores(self):
        print("\n🚧 Módulo de Conductores en desarrollo…\n")

    # ==== Salida del programa ====
    def salir(self):
        print("\n👋 Gracias por usar el sistema. ¡Hasta luego!")
        sys.exit()
