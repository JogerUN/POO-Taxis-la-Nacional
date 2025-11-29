from modulos.vehiculo import Vehiculo
from repositorios.vehiculo_repo import RepositorioVehiculo
from tools.validadores import inputObligatorio, validarFecha, validarEntero, convertirPlaca

repo = RepositorioVehiculo()

#Fuc. que permite registrar nuevos vehiculos 
def registrarVehiculo():
    print("\n--- REGISTRAR NUEVO VEHÍCULO ---")
    
    #creamos un diccionario con los datos que nos da el usuario
    datos = {
            "placa": convertirPlaca("Placa: ").upper(),
            "marca": inputObligatorio("Marca: "),
            "referencia": inputObligatorio("Referencia: "),
            "modelo": validarEntero("Modelo: "),
            "numeroChasis": inputObligatorio("Número de chasis: "),
            "numeroMotor": inputObligatorio("Número de motor: "),
            "color": inputObligatorio("Color: "),
            "concesionario":  inputObligatorio("Concesionario: "),
            "fechaCompraVehiculo": validarFecha("Fecha de compra (DD/MM/AAAA): "),
            "tiempoGarantia": validarEntero("Garantía (meses): "),
            "fechaCompraPolizaSeguro": validarFecha("Fecha compra póliza de seguro (DD/MM/AAAA): "),
            "proveedorPolizaSeguro": inputObligatorio("Proveedor póliza de seguro: "),
            "fechaCompraSegObligatorio": validarFecha("Fecha compra seguro obligatorio (DD/MM/AAAA): "),
            "proveedorSegObligatorio": inputObligatorio("Proveedor seguro obligatorio: "),
            "activo": validarEntero("Activo (1=Sí / 2=No): ", ["1", "2"])
        }        
        
    vehiculo = Vehiculo(**datos)
    repo.guardar(vehiculo)
    print("✅ Vehículo registrado correctamente.")
    
#Permite consultar la informacion de culquier vehiculo previamente registrado
def consultarVehiculo():
    print("\n=== CONSULTA DE VEHÍCULO ===\n")
    
    placa = inputObligatorio("\nPlaca del vehículo a consultar: ").upper()
    vehiculo = repo.buscar_por_placa(placa)
    
    if vehiculo is None:
        print(f"⚠️ No se encontró ningún vehículo registrado con la placa {placa}.")
        return
    
    print(f"\n=== Información del Vehículo {placa} ===")
    datos_vehiculo = [
        "Placa", "Marca", "Referencia", "Modelo", "Número chasis",
        "Número motor", "Color", "Concesionario", "Fecha compra",
        "Garantía (meses)", "Fecha póliza", "Proveedor póliza",
        "Fecha SOAT", "Proveedor SOAT", "Activo"        
    ]
    
    for datos_vehiculo, valor in zip(datos_vehiculo, vehiculo.infVehiculo()):
        print(f"{datos_vehiculo} : {valor}")
    
    print()
    
#Permite actualizar el estado los vehiculos 
def actualizarEstadoVehiculo():
    print("\n=== ACTUALIZAR ESTADO DEL VEHÍCULO ===\n")
    
    placa = inputObligatorio("\nPlaca del vehículo a actualizar: ").upper()
    vehiculo = repo.buscar_por_placa(placa)
    
    if vehiculo is None:
        print(f"⚠️ No se encontró ningún vehículo registrado con la placa {placa}.")
        return
    
    nuevo_estado = inputObligatorio("Nuevo estado (1=Activo, 2=Inactivo): ", ["1", "2"])
    repo.actualizar_estado(placa, int(nuevo_estado))
    print("✅ Estado del vehículo actualizado correctamente.")
    
#Permite actualizar las Polizas del vehculo 
def actualizarPolizaVehiculo():
    print("\n--- ACTUALIZAR POLIZA ---")
    placa = inputObligatorio("\nPlaca del vehículo a actualizar: ")
    vehiculo = repo.buscar_por_placa(placa)
    
     
    #Verificar que se ingrese un numero de placa 
    if not placa:
        print("⚠️ La placa no puede estar vacía.")
        return
    
    
    if vehiculo is None:
        print(f"⚠️ No se encontró ningún vehículo registrado con la placa {placa}.")
        return    #Verificar la existencia del vehiculo en la Base de Datos
    
    
    #Mostrar Informacion actual 
    polizas = vehiculo.obtenerPolizas()
    
    print(f"Poliza de seguro actual: Fecha: {polizas['fecha_poliza']} | Proveedor: {polizas['proveedor_poliza']}")
    print(f"Seguro obligatorio actual: Fecha: {polizas['fecha_seguro_obligatoriot']} | Proveedor: {polizas['proovedor_seguro_obligatorio']}")    
    
    
    
    #Solicitar actualizacionde de polizas
    nuevaFechaCompraPolizaSeguro = validarFecha("\nDigite fecha de la nueva poliza seguro (DD/MM/AAAA): ")
    nuevaProveedorPolizaSeguro = inputObligatorio("Digite el nombre del nuevo proveedor de la poliza seguro: ")
    nuevaFechaCompraSegObligatorio = validarFecha("Digite su fecha del nuevo seguro obligatorio (DD/MM/AAAA): ")
    nuevaProveedorSegObligatorio = inputObligatorio("Digite el nombre del nuevo proveedor del seguro obligatorio: ")

    # --- Actualizar el objeto en memoria ---
    vehiculo.actualizaPoliza(
        nueva_fecha_compra_poliza_seguro = nuevaFechaCompraPolizaSeguro,
        nueva_proveedor_poliza_seguro = nuevaProveedorPolizaSeguro,
        nueva_fecha_compra_segObligatorio = nuevaFechaCompraSegObligatorio,
        nueva_proveedor_segObligatorio = nuevaProveedorSegObligatorio
    )

    # --- Persistir usando el repo (repo espera un Vehiculo) ---
    try:
        repo.actualizar_poliza(vehiculo)
        print("✅ Pólizas actualizadas correctamente.")
    except Exception as e:
        print("❌ Error al actualizar pólizas:", e)
