# main.py
# =====================================================================
#               SISTEMA DE GESTIÓN TAXIS LA NACIONAL
#                       MENÚ PRINCIPAL (CLI)
# =====================================================================

import sys

# Importamos los servicios (capa lógica)
from servicios.vehiculo_servicios import (
    registrarVehiculo,
    consultarVehiculo,
    actualizarEstadoVehiculo,
    actualizarPolizaVehiculo,
    listaVehiculosActivos
)

# =====================================================================
#   MENÚ VEHÍCULOS
# =====================================================================

def menuVehiculos():
    while True:
        print("\n" + "="*60)
        print("                🚕 MÓDULO DE VEHÍCULOS 🚕")
        print("="*60)
        print("1. Registrar Vehículo")
        print("2. Consultar Vehículo")
        print("3. Actualizar Estado del Vehículo")
        print("4. Actualizar Pólizas del Vehículo")
        print("5. Listar Vehículos Activos")
        print("6. Volver al Menú Principal")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrarVehiculo()

        elif opcion == "2":
            consultarVehiculo()

        elif opcion == "3":
            actualizarEstadoVehiculo()

        elif opcion == "4":
            actualizarPolizaVehiculo()

        elif opcion == "5":
            listaVehiculosActivos()

        elif opcion == "6":
            print("🔙 Regresando al menú principal...\n")
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")


# =====================================================================
#   MENÚ PRINCIPAL DEL SISTEMA
# =====================================================================

def menuPrincipal():
    while True:
        print("\n" + "="*60)
        print("          SISTEMA DE GESTIÓN - TAXIS LA NACIONAL")
        print("="*60)
        print("1. Módulo Vehículos")
        print("2. Módulo Conductores (Próximamente)")
        print("3. Módulo Mantenimientos (Próximamente)")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            menuVehiculos()

        elif opcion == "2":
            print("\n🚧 Módulo Conductores en desarrollo…")
        
        elif opcion == "3":
            print("\n🚧 Módulo Mantenimientos en desarrollo…")

        elif opcion == "4":
            print("\n👋 Gracias por usar el sistema. ¡Hasta luego!")
            sys.exit()

        else:
            print("❌ Opción inválida. Intente de nuevo.")


# =====================================================================
#   EJECUCIÓN DEL PROGRAMA
# =====================================================================

if __name__ == "__main__":
    menuPrincipal()
