# menus/menu_base.py

class Menu:
    """
    Clase base para construir menús de consola.
    Proporciona:
    - título
    - opciones {opcion: (texto, función)}
    - método mostrar() reutilizable
    """

    def __init__(self, titulo: str, opciones: dict):
        self.titulo = titulo
        self.opciones = opciones

    def mostrar(self):
        """Renderiza el menú y ejecuta la acción seleccionada."""
        while True:
            print("\n" + "="*60)
            print(self.titulo.center(60))
            print("="*60)

            # Mostrar las opciones
            for key, (texto, _) in self.opciones.items():
                print(f"{key}. {texto}")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion in self.opciones:
                texto, funcion = self.opciones[opcion]

                resultado = funcion()

                # Todos los menús deben retornar "salir" para finalizar
                if resultado == "salir":
                    return
            else:
                print("❌ Opción inválida. Intente de nuevo.")
