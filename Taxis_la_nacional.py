import sqlite3
from sqlite3 import Error
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# ------------------------------------------------------------
# CONEXIÓN A BASE DE DATOS
# ------------------------------------------------------------

def crearConexion():
    try:
        connection = sqlite3.connect("taxis_la_nacional.db")
        return connection
    except Error as e:
        print("Error al conectar con la base de datos:", e)
        return None

# ------------------------------------------------------------
# TABLA VEHÍCULOS
# ------------------------------------------------------------

def crearTablaVehiculos(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vehiculos(
                        placa TEXT PRIMARY KEY,
                        marca TEXT NOT NULL,
                        referencia TEXT NOT NULL,
                        modelo INTEGER NOT NULL,
                        numeroChasis TEXT NOT NULL,
                        numeroMotor TEXT NOT NULL,
                        color TEXT NOT NULL,
                        concesionario TEXT NOT NULL,
                        fechaCompraVehiculo TEXT NOT NULL,
                        tiempoGarantia INTEGER NOT NULL,
                        fechaCompraPolizaSeguro TEXT NOT NULL,
                        proveedorPolizaSeguro TEXT NOT NULL,
                        fechaCompraSegObligatorio TEXT NOT NULL,
                        proveedorSegObligatorio TEXT NOT NULL,
                        activo INTEGER NOT NULL
                    )''')
    connection.commit()

#Se encarga de rectificar y evitar valores de entrada "inputs" vacios 
def inputObligatorio(mensaje):
    #metodo .strip() para eliminar espacios en blanco de los extremos de la cadena
    entrada = input(mensaje).strip()
    if entrada == "":
        print(" ⚠️ Lo sentimos el campo no puede estar vacio, porfavor intente de nuevo.")
        print("Regresando al menu anterior...")
        return None
    else:
        return entrada
        
#Fuc. que permite registrar nuevos vehiculos 
def registrarVehiculo(connection):
    print("\n--- REGISTRAR NUEVO VEHÍCULO ---")
    
    campos = [
        "Placa: ", 
        "Marca: ",
        "Referencia: ",
        "Modelo: ",
        "Número de chasis: ",
        "Número de motor: ",
        "Color: ",
        "Concesionario: ",
        "Fecha de compra (DD/MM/AAAA): ",
        "Garantía (meses): ",
        "Fecha compra poliza de seguro (DD/MM/AAAA): ",
        "Proveedor poliza de seguro: ",
        "Fecha compra seguro obligatorio (DD/MM/AAAA): ",
        "Proveedor seguro obligatorio: ",
        "Activo (1=Sí / 2=No): "
    ]
    
    datos=[] #Lista temporal para guardar valores ingresados
    
    #Verifica que se ingresen dator de lo contrario retorna al menu anterior
    for campo in campos:
        entrada = inputObligatorio(campo)
        if entrada is None:
            print("❌ Registro cancelado. No se guardaron datos.")
            return
        datos.append(entrada) #Une cada dato a la lista datos=[] 

    datos = tuple(datos) #convertimos la lista en tupla 
    
#Evita ingresar un vehiculo que ya se encuentre registradio por medio de la  PRIMARY KEY "placa"
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO vehiculos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", datos)
        connection.commit()
        print("✅ Vehículo registrado correctamente.")
    except sqlite3.IntegrityError:
        print(f"❌ Error el vehiculo ya se encuntra registrado: ")
    except Error as e:
        print(f"❌ Error al registrar el vehiculo: ", e)

#Permite consultar la informacion de culquier vehiculo previamente registrado
def consultarVehiculo(connection):
    placa = input("\nPlaca del vehículo a consultar: ")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE placa=?", (placa,))
    row = cursor.fetchone()

    if row:
        print(f"\nInformación del vehículo {placa}:")
        print(f"Marca: {row[1]}")
        print(f"Referencia: {row[2]}")
        print(f"Modelo: {row[3]}")
        print(f"Número de chasis: {row[4]}")
        print(f"Número de motor: {row[5]}")
        print(f"Color: {row[6]}")
        print(f"Concesionario: {row[7]}")
        print(f"Fecha de compra: {row[8]}")
        print(f"Garantía (meses): {row[9]}")
        print(f"Poliza de Seguro: {row[10]} ({row[11]})")
        print(f"Seguro obligatorio: {row[12]} ({row[13]})")
        print(f"Estado: {'Activo' if row[14] == 1 else 'Inactivo'}")
    else:
        print("⚠️ No se encontró ningún vehículo con esa placa.")

#Permite actualizar el estado los vehiculos 
def actualizarEstadoVehiculo(connection):
    placa = input("\nPlaca del vehículo a actualizar: ")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE placa=?", (placa,))
    if not cursor.fetchone():
        print("❌ No se encontró el vehículo.")
        return
    nuevoEstado = input("Nuevo estado (1=Activo / 2=Inactivo): ")
    cursor.execute("UPDATE vehiculos SET activo=? WHERE placa=?", (nuevoEstado, placa))
    connection.commit()
    print("✅ Estado del vehículo actualizado correctamente.")

def actualizarPolizaVehiculo(connection):
    print("\n--- ACTUALIZAR POLIZA ---")
    placa = inputObligatorio("\nDigite la placa del vehículo: ")
    
    #Verificar que se ingrese un numero de placa 
    if not placa:
        print("⚠️ La placa no puede estar vacía.")
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT fechaCompraPolizaSeguro, proveedorPolizaSeguro, fechaCompraSegObligatorio, proveedorSegObligatorio FROM vehiculos WHERE placa=?", (placa,))
    row = cursor.fetchone()
    
    #Verificar la existencia del vehiculo en la Base de Datos
    if not row:
        print("❌ Vehículo no encontrado.")
        return
    
    #Mostrar Informacion actual        
    print(f"Poliza de seguro actual: Fecha: {row[0]} | Proveedor: {row[1]}")
    print(f"Seguro obligatorio actual: Fecha: {row[2]} | Proveedor: {row[3]}")
    
    
    #Solicitar actualizacionde de polizas
    nuevaFechaCompraPolizaSeguro = inputObligatorio("\nDigite fecha de la nueva poliza seguro (DD/MM/AAAA): ")
    nuevaProveedorPolizaSeguro = inputObligatorio("Digite el nombre del nuevo proveedor de la poliza seguro: ")
    nuevaFechaCompraSegObligatorio = inputObligatorio("Digite su fecha del nuevo seguro obligatorio (DD/MM/AAAA): ")
    nuevaProveedorSegObligatorio = inputObligatorio("Digite el nombre del nuevo proveedor del seguro obligatorio: ")

    formatoFechas = "%d/%m/%Y"

    try:
        with connection:  # This ensures atomic transaction management
            cursor = connection.cursor()

            #Obtiene fechas actuales
            fechaCompraPolizaSeguro = datetime.strptime(row[0], formatoFechas)
            fechaCompraSegObligatorio = datetime.strptime(row[2], formatoFechas)
            
            #Pasa las nuevas fechas con el correcto formato
            nuevaFechaCompraPolizaSeguro_dt = datetime.strptime(nuevaFechaCompraPolizaSeguro, formatoFechas)
            nuevaFechaCompraSegObligatorio_dt = datetime.strptime(nuevaFechaCompraSegObligatorio, formatoFechas)
            
            # Actualizacion de datos
            if nuevaFechaCompraPolizaSeguro_dt > fechaCompraPolizaSeguro:
                cursor.execute("""
                    UPDATE vehiculos SET fechaCompraPolizaSeguro=?, proveedorPolizaSeguro=? WHERE placa=? """,
                    (nuevaFechaCompraPolizaSeguro, nuevaProveedorPolizaSeguro, placa))
                print("✅ Póliza de seguro actualizada exitosamente.")
            else:
                print("⚠️ La nueva fecha no puede ser anterior a la actual.")
            
            if nuevaFechaCompraSegObligatorio_dt > fechaCompraSegObligatorio:
                cursor.execute("""
                    UPDATE vehiculos SET fechaCompraSegObligatorio=?, proveedorSegObligatorio=? WHERE placa=? """,
                    (nuevaFechaCompraSegObligatorio, nuevaProveedorSegObligatorio, placa))
                print("✅ Póliza de seguro obligatorio actualizada exitosamente.")
            else:
                print("⚠️ La nueva fecha del SOAT no puede ser anterior a la actual.")

    except ValueError:
        print("\n❌ Formato incorrecto. Use (DD/MM/AAAA).")
    except sqlite3.OperationalError as e:
        print(f"\n❌ Error de base de datos: {e}")

def listaVeiculosActivos(connection):
    print("\n--- LISTA DE VEHICULOS ACTIVOS ---")  
    cursor = connection.cursor()
    cursor.execute("SELECT placa, marca, referencia, modelo, color FROM vehiculos WHERE activo=1")
    filas  = cursor.fetchall()
    
    if not filas:
        print("⚠️ No existen vehiculos registrados.")
        return
    
    for row in filas:
        print(f"PLaca: {row[0]} Marca: {row[1]} Referencia: {row[2]} Modelo: {row[3]} color: {row[4]}")
    print(f"\n Total vehiculos activos: {len(filas)}")
    
    connection.commit()
# ------------------------------------------------------------
# TABLA CONDUCTORES
# ------------------------------------------------------------
def crearTablaConductores(connection):
    cursorObj = connection.cursor()
    cad = '''CREATE TABLE IF NOT EXISTS conductores(
                noIdentificacion TEXT NOT NULL,
                nombreCompleto TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correoElectronico TEXT NOT NULL,
                placaVehiculo TEXT NOT NULL,
                fechaIngreso TEXT,
                fechaRetiro TEXT,
                indicadorContratado INTEGER NOT NULL,
                turno INTEGER NOT NULL,
                valorTurno INTEGER NOT NULL,
                valorAhorro INTEGER NOT NULL,
                valorAdeuda INTEGER NOT NULL,
                totalAhorradoNoDevuelto INTEGER NOT NULL,
                PRIMARY KEY(noIdentificacion),
                FOREIGN KEY (placaVehiculo) REFERENCES vehiculos(placa)
            )'''
    cursorObj.execute(cad)
    connection.commit()


def registrarConductor(connection):
    print("\n--- REGISTRO DE NUEVO CONDUCTOR ---")

    # Activar las claves foráneas por seguridad
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # Captura de datos
    noId = input("Número de identificación: ").strip()
    nombreCompleto = input("Nombre completo: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()
    correo = input("Correo electrónico: ").strip()
    placaVehiculo = input("Placa del vehículo asignado: ").strip().upper()  # Forzar mayúsculas
    fechaIngreso = input("Fecha de ingreso (DD/MM/AAAA o vacío si no aplica): ").strip()
    fechaRetiro = input("Fecha de retiro (DD/MM/AAAA o vacío si no aplica): ").strip()
    indicadorContratado = input("Estado (1=Activo / 2=Candidato / 3=Despedido): ").strip()
    turno = input("Turno (1=24 horas / 2=12 horas): ").strip()
    valorTurno = input("Valor del turno: ").strip()
    valorAhorro = input("Valor ahorro mensual: ").strip()
    valorAdeuda = input("Valor adeudado: ").strip()
    totalNoDevuelto = input("Total ahorrado no devuelto: ").strip()

    # Validar campos obligatorios
    campos_obligatorios = {
        "Número de identificación": noId,
        "Nombre completo": nombreCompleto,
        "Dirección": direccion,
        "Teléfono": telefono,
        "Correo electrónico": correo,
        "Placa del vehículo": placaVehiculo,
        "Estado": indicadorContratado,
        "Turno": turno,
        "Valor del turno": valorTurno,
        "Valor ahorro": valorAhorro,
        "Valor adeudado": valorAdeuda,
        "Total no devuelto": totalNoDevuelto
    }

    for campo, valor in campos_obligatorios.items():
        if not valor:
            print(f"❌ Error: El campo '{campo}' es obligatorio. No se puede registrar el conductor.")
            return

    # Verificar que la placa exista en la tabla vehiculos
    cursor.execute("SELECT placa FROM vehiculos WHERE placa = ?", (placaVehiculo,))
    vehiculo_existente = cursor.fetchone()

    if not vehiculo_existente:
        print(f"❌ Error: La placa '{placaVehiculo}' no existe en la base de datos de vehículos.")
        return

    # Si pasa todas las validaciones, registrar el conductor
    datos = (
        noId, nombreCompleto, direccion, telefono, correo, placaVehiculo,
        fechaIngreso, fechaRetiro, indicadorContratado, turno,
        valorTurno, valorAhorro, valorAdeuda, totalNoDevuelto
    )

    try:
        cursor.execute('''INSERT INTO conductores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', datos)
        connection.commit()
        print("✅ Conductor registrado correctamente.")
    except sqlite3.IntegrityError:
        print("❌ Error: Ya existe un conductor con ese número de identificación.")
    except sqlite3.Error as e:
        print("⚠ Error al registrar conductor:", e)


    # Intentar insertar
    try:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO conductores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', datos)
        connection.commit()
        print("✅ Conductor registrado correctamente.")
    except sqlite3.IntegrityError:
        print("❌ Error: Ya existe un conductor con ese número de identificación.")
    except sqlite3.Error as e:
        print("⚠ Error al registrar conductor:", e)



def actualizarConductor(connection):
    print("\n--- ACTUALIZAR INFORMACIÓN DE CONDUCTOR ---")
    noId = input("Número de identificación del conductor: ")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noId,))
    fila = cursor.fetchone()

    # Si no se encuentra el conductor, avisar y salir
    if not fila:
        print("❌ No se encontró el conductor.")
        return

    # Mostrar los datos actuales
    print(f"\nDatos actuales del conductor {fila[1]}:")
    print(f"Dirección actual: {fila[2]}")
    print(f"Teléfono actual: {fila[3]}")
    print(f"Correo actual: {fila[4]}")
    print(f"Fecha ingreso actual: {fila[6]}")
    print(f"Fecha retiro actual: {fila[7]}")
    print(f"Valor adeudado actual: {fila[12]}")
    print(f"Total ahorrado no devuelto actual: {fila[13]}\n")

    # Pedir nuevos valores, permitiendo dejar en blanco
    direccion = input("Nueva dirección (Enter para mantener actual): ") or fila[2]
    telefono = input("Nuevo teléfono (Enter para mantener actual): ") or fila[3]
    correo = input("Nuevo correo electrónico (Enter para mantener actual): ") or fila[4]
    fechaIngreso = input("Nueva fecha de ingreso (Enter para mantener actual): ") or fila[6]
    fechaRetiro = input("Nueva fecha de retiro (Enter para mantener actual): ") or fila[7]
    valorAdeuda = input("Nuevo valor adeudado (Enter para mantener actual): ") or fila[12]
    totalNoDevuelto = input("Nuevo total ahorrado no devuelto (Enter para mantener actual): ") or fila[13]
    
    try:
        cursor.execute('''UPDATE conductores SET 
                            direccion=?, telefono=?, correoElectronico=?, 
                            fechaIngreso=?, fechaRetiro=?, valorAdeuda=?, 
                            totalAhorradoNoDevuelto=? 
                          WHERE noIdentificacion=?''',
                       (direccion, telefono, correo, fechaIngreso, fechaRetiro,
                        valorAdeuda, totalNoDevuelto, noId))
        connection.commit()
        print("✅ Información actualizada correctamente.")
    except Error as e:
        print("⚠ Error al actualizar:", e)

def consultarConductor(connection):
    print("\n--- CONSULTAR CONDUCTOR ---")
    noId = input("Número de identificación del conductor: ")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noId,))
    fila = cursor.fetchone()

    if not fila:
        print("❌ No se encontró información del conductor.")
        return

    estado = { '1': 'Activo', '2': 'Candidato', '3': 'Despedido' }.get(str(fila[8]), 'Desconocido')
    turnoTexto = { '1': '24 horas', '2': '12 horas' }.get(str(fila[9]), 'No definido')

    print(f'''
    IDENTIFICACIÓN: {fila[0]}
    NOMBRE COMPLETO: {fila[1]}
    DIRECCIÓN: {fila[2]}
    TELÉFONO: {fila[3]}
    CORREO: {fila[4]}
    PLACA VEHÍCULO: {fila[5]}
    FECHA INGRESO: {fila[6]}
    FECHA RETIRO: {fila[7]}
    ESTADO: {estado}
    TURNO: {turnoTexto}
    VALOR TURNO: {fila[10]}
    VALOR AHORRO: {fila[11]}
    VALOR ADEUDA: {fila[12]}
    TOTAL NO DEVUELTO: {fila[13]}
    ''')

# ------------------------------------------------------------
# TABLA MANTENIMIENTOS
# ------------------------------------------------------------

def crearTablaMantenimientos(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mantenimientos (
            numeroOrden TEXT PRIMARY KEY NOT NULL,
            placaVehiculo TEXT NOT NULL,
            nitProveedor TEXT NOT NULL,
            nombreProveedor TEXT NOT NULL,
            descripcionServicio TEXT NOT NULL,
            valorFacturado REAL NOT NULL,
            fechaServicio TEXT NOT NULL,
            FOREIGN KEY (placaVehiculo) REFERENCES vehiculos(placa) ON DELETE CASCADE
        )
    ''')
    connection.commit()

def LeerInformacionMantenimiento():
    numeroDeOrden = input("Número de Orden: ")
    placaVehiculo = input("Placa del Vehículo: ")
    nit = input("NIT del proveedor: ")
    nombreProveedor = input("Nombre del proveedor: ")
    descripcionServicio = input("Descripción del servicio: ")
    valorFacturado = input("Valor facturado: ")

    # Validar formato de fecha
    while True:
        fechaServicio = input("Fecha del servicio (DD/MM/AAAA): ")
        try:
            datetime.strptime(fechaServicio, "%d/%m/%Y")
            break
        except ValueError:
            print("⚠ Fecha inválida. Intente de nuevo (formato DD/MM/AAAA).")

    mantenimiento = (
        numeroDeOrden, placaVehiculo, nit, nombreProveedor,
        descripcionServicio, valorFacturado, fechaServicio
    )
    return mantenimiento


def CrearMantenimiento(connection, mant):
    try:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO mantenimientos
                          (numeroOrden, placaVehiculo, nitProveedor, nombreProveedor,
                           descripcionServicio, valorFacturado, fechaServicio)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', mant)
        connection.commit()
        print("✅ Mantenimiento registrado correctamente.")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("⚠ Número de orden repetido. No se puede registrar nuevamente.")
        else:
            print("⚠ Error: Campos vacíos o duplicados no permitidos.")
    except sqlite3.Error as e:
        print("❌Error al registrar mantenimiento:", e)


def ConsultarMantenimientoRealizado(connection):
    try:
        cursor = connection.cursor()
        numeroDeOrden = input("Número de orden a consultar: ")

        cursor.execute('''
            SELECT numeroOrden, placaVehiculo, nitProveedor, nombreProveedor,
                   descripcionServicio, valorFacturado, fechaServicio
            FROM mantenimientos
            WHERE numeroOrden = ?
        ''', (numeroDeOrden,))
        fila = cursor.fetchone()

        if fila is None:
            print("❌ No se encontró mantenimiento con ese número de orden.")
            return

        print("\n--- INFORMACIÓN DEL MANTENIMIENTO ---")
        print(f"Número de Orden: {fila[0]}")
        print(f"Placa del Vehículo: {fila[1]}")
        print(f"NIT del Proveedor: {fila[2]}")
        print(f"Nombre del Proveedor: {fila[3]}")
        print(f"Descripción del Servicio: {fila[4]}")
        print(f"Valor Facturado: {fila[5]}")
        print(f"Fecha del Servicio: {fila[6]}")
        print("----------------------------------------")

    except sqlite3.Error as e:
        print("⚠ Error al consultar mantenimiento:", e)


def ActualizarMantenimientoRealizado(connection):
    cursor = connection.cursor()
    numeroDeOrden = input("Número de orden a actualizar: ")

    cursor.execute("SELECT * FROM mantenimientos WHERE numeroOrden = ?", (numeroDeOrden,))
    fila = cursor.fetchone()

    if not fila:
        print("❌ No se encontró el mantenimiento especificado.")
        return

    print("\nIngrese los nuevos datos (deje vacío para mantener el valor actual):")

    placaVehiculo = input(f"Placa ({fila[1]}): ") or fila[1]
    nit = input(f"NIT proveedor ({fila[2]}): ") or fila[2]
    nombreProveedor = input(f"Nombre proveedor ({fila[3]}): ") or fila[3]
    descripcionServicio = input(f"Descripción ({fila[4]}): ") or fila[4]
    valorFacturado = input(f"Valor facturado ({fila[5]}): ") or fila[5]
    fechaServicio = input(f"Fecha servicio ({fila[6]}): ") or fila[6]

    try:
        cursor.execute('''UPDATE mantenimientos
                          SET placaVehiculo=?, nitProveedor=?, nombreProveedor=?,
                              descripcionServicio=?, valorFacturado=?, fechaServicio=?
                          WHERE numeroOrden=?''',
                       (placaVehiculo, nit, nombreProveedor, descripcionServicio,
                        valorFacturado, fechaServicio, numeroDeOrden))
        connection.commit()
        print("✅ Mantenimiento actualizado correctamente.")
    except sqlite3.Error as e:
        print("❌ Error al actualizar mantenimiento:", e)


def BorrarMantenimiento(connection):
    try:
        cursor = connection.cursor()
        numeroDeOrden = input("Número de orden a eliminar: ")

        cursor.execute("DELETE FROM mantenimientos WHERE numeroOrden = ?", (numeroDeOrden,))
        if cursor.rowcount == 0:
            print("⚠ No se encontró el mantenimiento. No se eliminó ningún registro.")
        else:
            print("✅ Mantenimiento eliminado correctamente.")
        connection.commit()
    except sqlite3.Error as e:
        print("❌ Error al eliminar mantenimiento:", e)
# ------------------------------------------------------------
# GENERAR FICHA VEHÍCULO EN PDF
# ------------------------------------------------------------

def generarFichaVehiculoPDF(connection):
    placa = input("\nIngrese la placa del vehículo para generar ficha: ")
    cursor = connection.cursor()

    # Consultar vehículo
    cursor.execute("SELECT * FROM vehiculos WHERE placa=?", (placa,))
    vehiculo = cursor.fetchone()
    if not vehiculo:
        print("❌ No se encontró el vehículo.")
        return

    # Consultar conductor asignado
    cursor.execute("SELECT nombreCompleto, telefono, correoElectronico FROM conductores WHERE placaVehiculo=?", (placa,))
    conductor = cursor.fetchone()

    # Consultar mantenimientos
    cursor.execute("SELECT numeroOrden, nombreProveedor, nitproveedor, descripcionServicio , valorFacturado, valorFacturado FROM mantenimientos WHERE placaVehiculo=?", (placa,))
    mantenimientos = cursor.fetchone()

    archivo = f"Ficha_Vehiculo_{placa}.pdf"
    c = canvas.Canvas(archivo, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(200, 750, "FICHA DE VEHÍCULO")
    c.drawString(50, 720, f"Placa: {vehiculo[0]}")
    c.drawString(50, 700, f"Marca: {vehiculo[1]}")
    c.drawString(50, 680, f"Referencia: {vehiculo[2]}")
    c.drawString(50, 660, f"Modelo: {vehiculo[3]}")
    c.drawString(50, 640, f"Color: {vehiculo[6]}")
    c.drawString(50, 620, f"Concesionario: {vehiculo[7]}")
    c.drawString(50, 600, f"Activo: {'Sí' if vehiculo[14]==1 else 'No'}")

    if conductor:
        c.drawString(50, 570, f"Conductor: {conductor[0]}")
        c.drawString(50, 550, f"Teléfono: {conductor[1]}")
        c.drawString(50, 530, f"Correo: {conductor[2]}")
    else:
        c.drawString(50, 570, "Conductor: No asignado")

    c.drawString(50, 500, "Mantenimientos realizados:")
    y = 480
    if mantenimientos:
        c.drawString(60, 480, f"Numero de Orden: {mantenimientos[0]}")
        c.drawString(60, 460, f"Nombre del Proveedor: {mantenimientos[1]}")
        c.drawString(60, 440, f"Nit del Proveedor: {mantenimientos[2]}")
        c.drawString(60, 420, f"Descripciòn del Servicio: {mantenimientos[3]}")
        c.drawString(60, 400, f"Valor Facturado: {mantenimientos[4]}")
        c.drawString(60, 380, f"Fecha el Servicio: {mantenimientos[5]}")
    else:
        c.drawString(50, y, "No hay manteniemientos")

        y -= 20

    c.save()
    print(f"✅ Ficha PDF generada: {archivo}")

# ------------------------------------------------------------
# MENÚS
# ------------------------------------------------------------

def menuVehiculos(connection):
    while True:
        print("\n=== MENÚ VEHÍCULOS ===")
        print("1. Registrar vehículo")
        print("2. Consultar vehículo")
        print("3. Actualizar Estado del vehiculo")
        print("4. Actualizar Polizas")
        print("5. Lista de Vehiculos activos")
        print("6. Volver al menú principal")

        opcion = input("Seleccione: ")
        if opcion == "1":
            registrarVehiculo(connection)
        elif opcion == "2":
            consultarVehiculo(connection)
        elif opcion == "3":
            actualizarEstadoVehiculo(connection)
        elif opcion == "4":
            actualizarPolizaVehiculo(connection)
        elif opcion =="5":
            listaVeiculosActivos(connection)
        elif opcion == "6":
            break
        else:
            print("⚠ Opción no válida.")

def menuConductores(connection):
    while True:
        print("\n=== MENÚ CONDUCTORES ===")
        print("1. Registrar conductor")
        print("2. Consultar conductor")
        print("3. Actualizar conductor")
        print("4. Volver al menú principal")

        opcion = input("Seleccione: ")
        if opcion == "1":
            registrarConductor(connection)
        elif opcion == "2":
            consultarConductor(connection)
        elif opcion == "3":
            actualizarConductor(connection)
        elif opcion == "4":
            break
        else:
            print("⚠ Opción no válida.")

def menuMantenimientos(connection):
    salirMantenimiento=True
    while True:
        print("\n=== MENÚ MANTENIMIENTOS ===")
        print("1. Registrar mantenimiento")
        print("2. Consultar Mantenimiento Realizado")
        print("3. Borrar Manteniento")
        print("4. Actualizar mantenimiento")
        print("5. Volver al menú principal")
        opcMantenimientos = input("Seleccione: ")
        if  (opcMantenimientos=='1'):
                MiMantenimiento=LeerInformacionMantenimiento()
                CrearMantenimiento(connection,MiMantenimiento)
        elif    (opcMantenimientos=='2'):
                ConsultarMantenimientoRealizado(connection)
        elif    (opcMantenimientos=='3'):
                BorrarMantenimiento(connection)
        elif (opcMantenimientos=='4'):
                ActualizarMantenimientoRealizado(connection)
        elif    (opcMantenimientos=='5'):
                  break
        
        else:
            print("⚠ Opción no válida.")

# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------

def menuPrincipal():
    connection = crearConexion()
    crearTablaVehiculos(connection)
    crearTablaConductores(connection)
    crearTablaMantenimientos(connection)

    while True:
        print("\n=== SISTEMA TAXIS LA NACIONAL ===")
        print("1. Gestión de vehículos")
        print("2. Gestión de conductores")
        print("3. Gestión de mantenimientos")
        print("4. Generar ficha técnica")
        print("5. Salir")

        opcion = input("Seleccione: ")
        if opcion == "1":
            menuVehiculos(connection)
        elif opcion == "2":
            menuConductores(connection)
        elif opcion == "3":
            menuMantenimientos(connection)
        elif opcion == "4":
            generarFichaVehiculoPDF(connection)
        elif opcion == "5":
            print("Saliendo...")
            connection.close()
            break
        else:
            print("⚠ Opción no válida.")

# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

if __name__ == "__main__":
    menuPrincipal()
    
