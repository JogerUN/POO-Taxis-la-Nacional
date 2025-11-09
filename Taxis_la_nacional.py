import sqlite3
from sqlite3 import Error

#permite crear archivos PDF desde Python.
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
                        fechaCompraSeguro TEXT NOT NULL,
                        proveedorSeguro TEXT NOT NULL,
                        fechaCompraSegObligatorio TEXT NOT NULL,
                        proveedorSegObligatorio TEXT NOT NULL,
                        activo INTEGER NOT NULL
                    )''')
    connection.commit()

def registrarVehiculo(connection):
    print("\n--- REGISTRAR NUEVO VEHÍCULO ---")
    
    datos = (
        input("Placa: "), 
        input("Marca: "),
        input("Referencia: "),
        input("Modelo: "),
        input("Número de chasis: "),
        input("Número de motor: "),
        input("Color: "),
        input("Concesionario: "),
        input("Fecha de compra (DD/MM/AAAA): "),
        input("Garantía (meses): "),
        input("Fecha compra seguro (DD/MM/AAAA): "),
        input("Proveedor seguro: "),
        input("Fecha compra seguro obligatorio (DD/MM/AAAA): "),
        input("Proveedor seguro obligatorio: "),
        input("Activo (1=Sí / 2=No): ")
    )

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO vehiculos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", datos)
        connection.commit()
        print("✅ Vehículo registrado correctamente.")
    except Error as e:
        print(f"❌ Error el vehiculo ya se encuntra registrado: ", e)

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
        print(f"Fecha compra: {row[8]}")
        print(f"Garantía (meses): {row[9]}")
        print(f"Seguro: {row[10]} ({row[11]})")
        print(f"Seguro obligatorio: {row[12]} ({row[13]})")
        print(f"Estado: {'Activo' if row[14] == 1 else 'Inactivo'}")
    else:
        print("⚠️ No se encontró ningún vehículo con esa placa.")

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
    print("Estado del vehículo actualizado correctamente.")

def actualizarPolizaVehiculo(connection):
    print("\n--- ACTUALIZAR POLIZA ---")
    placa = input("Digite la placa del vehículo: ")

    nuevaFechaCompraSeguro = input("\nDigite su fecha del nuevo seguro (DD/MM/AAAA): ")
    nuevaProveedorSeguro = input("\nDigite el nombre del nuevo proveedor del seguro: ")
    nuevaFechaCompraSegObligatorio = input("\nDigite su fecha del nuevo seguro obligatorio (DD/MM/AAAA): ")
    nuevaProveedorSegObligatorio = input("Digite el nombre del nuevo proveedor del seguro obligatorio: ")

    formatoFechas = "%d/%m/%Y"

    try:
        with connection:  # This ensures atomic transaction management
            cursor = connection.cursor()

            # Get current data
            cursor.execute("SELECT fechaCompraSeguro, fechaCompraSegObligatorio FROM vehiculos WHERE placa=?", (placa,))
            row = cursor.fetchone()
            if not row:
                print("\n❌ Vehículo no encontrado.")
                return
            
            fechaCompraSeguro = datetime.strptime(row[0], formatoFechas)
            fechaCompraSegObligatorio = datetime.strptime(row[1], formatoFechas)

            # Convert new input dates
            nuevaFechaCompraSeguro_dt = datetime.strptime(nuevaFechaCompraSeguro, formatoFechas)
            nuevaFechaCompraSegObligatorio_dt = datetime.strptime(nuevaFechaCompraSegObligatorio, formatoFechas)

            # Update if newer
            if nuevaFechaCompraSeguro_dt > fechaCompraSeguro:
                cursor.execute("""
                    UPDATE vehiculos 
                    SET fechaCompraSeguro=?, proveedorSeguro=? 
                    WHERE placa=?
                """, (nuevaFechaCompraSeguro, nuevaProveedorSeguro, placa))
                print("\n✅ Póliza de seguro actualizada exitosamente.")
            else:
                print("\n⚠️ La nueva fecha no puede ser anterior a la actual.")

            if nuevaFechaCompraSegObligatorio_dt > fechaCompraSegObligatorio:
                cursor.execute("""
                    UPDATE vehiculos 
                    SET fechaCompraSegObligatorio=?, proveedorSegObligatorio=? 
                    WHERE placa=?
                """, (nuevaFechaCompraSegObligatorio, nuevaProveedorSegObligatorio, placa))
                print("\n✅ Póliza de seguro obligatorio actualizada exitosamente.")
            else:
                print("\n⚠️ La nueva fecha del SOAT no puede ser anterior a la actual.")

            # `with connection:` auto-commits here safely

    except sqlite3.OperationalError as e:
        print(f"\n❌ Error de base de datos: {e}")
    except ValueError:
        print("\n❌ Formato incorrecto. Use (DD/MM/AAAA).")

def listaVeiculosActivos(connection):
    print("\n--- LISTA DE VEHICULOS ACTIVOS ---")  
    cursor = connection.cursor()
    cursor.execute("SELECT placa, marca, referencia, modelo, color FROM vehiculos WHERE activo=1")
    filas  = cursor.fetchall()
    
    if not filas:
        print("\n⚠️ No existen vehiculos registrados.")
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
    print("✅Tabla 'conductores' creada correctamente.")


def registrarConductor(connection):
    print("\n--- REGISTRO DE NUEVO CONDUCTOR ---")
    noId = input("Número de identificación: ")
    nombreCompleto = input("Nombre completo: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    correo = input("Correo electrónico: ")
    placaVehiculo = input("Placa del vehículo asignado: ")
    fechaIngreso = input("Fecha de ingreso (DD/MM/AAAA o vacío si no aplica): ")
    fechaRetiro = input("Fecha de retiro (DD/MM/AAAA o vacío si no aplica): ")
    indicadorContratado = input("Estado (1=Activo / 2=Inactivo / 3=Despedido): ")
    turno = input("Turno (1=24 horas / 2=12 horas): ")
    valorTurno = input("Valor del turno: ")
    valorAhorro = input("Valor ahorro mensual: ")
    valorAdeuda = input("Valor adeudado: ")
    totalNoDevuelto = input("Total ahorrado no devuelto: ")

    datos = (noId, nombreCompleto, direccion, telefono, correo, placaVehiculo,
             fechaIngreso, fechaRetiro, indicadorContratado, turno, valorTurno,
             valorAhorro, valorAdeuda, totalNoDevuelto)

    try:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO conductores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', datos)
        connection.commit()
        print("✅ Conductor registrado correctamente.")
    except Error as e:
        print("❌ Error al registrar conductor:", e)


def actualizarConductor(connection):
    print("\n--- ACTUALIZAR INFORMACIÓN DE CONDUCTOR ---")
    noId = input("Número de identificación del conductor: ")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noId,))
    fila = cursor.fetchone()

    # Si no se encuentra el conductor, avisar y salir
    if not fila:
        print("⚠️ No se encontró el conductor.")
        return

    # Mostrar los datos actuales para poder validar que se quiere actualizar
    print(f"\nDatos actuales del conductor {fila[1]}:")
    print(f"Dirección actual: {fila[2]}")
    print(f"Teléfono actual: {fila[3]}")
    print(f"Correo actual: {fila[4]}")
    print(f"Fecha ingreso actual: {fila[6]}")
    print(f"Fecha retiro actual: {fila[7]}")
    print(f"Valor adeudado actual: {fila[12]}")
    print(f"Total ahorrado no devuelto actual: {fila[13]}\n")

    # Pedir nuevos valores, permitiendo dejar en blanco paa lo que no se quiere cambiar
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
        print("❌ Error al actualizar:", e)

def consultarConductor(connection):
    print("\n--- CONSULTAR CONDUCTOR ---")
    noId = input("Número de identificación del conductor: ")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noId,))
    fila = cursor.fetchone()

    if not fila:
        print("❌ No se encontró información del conductor.")
        return

    estado = { '1': 'Activo', '2': 'Inactivo', '3': 'Despedido' }.get(str(fila[8]), 'Desconocido')
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS mantenimientos (
                        numeroOrden TEXT PRIMARY KEY,
                        placaVehiculo TEXT NOT NULL,
                        nitProveedor TEXT NOT NULL,
                        nombreProveedor TEXT NOT NULL,
                        descripcionServicio TEXT,
                        valorFacturado REAL,
                        fechaServicio TEXT,
                        FOREIGN KEY (placaVehiculo) REFERENCES vehiculos(placa)
                    )''')
    connection.commit()

def registrarMantenimiento(connection):
    print("\n--- REGISTRAR MANTENIMIENTO ---")
    datos = (
        input("Número de orden: "),
        input("Placa del vehículo: "),
        input("NIT proveedor: "),
        input("Nombre proveedor: "),
        input("Descripción servicio: "),
        float(input("Valor facturado: ")),
        input("Fecha del servicio (DD/MM/AAAA): ")
    )
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO mantenimientos VALUES (?,?,?,?,?,?,?)", datos)
        connection.commit()
        print("Mantenimiento registrado correctamente.")
    except Error as e:
        print("Error al registrar mantenimiento:", e)

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
        print("No se encontró el vehículo.")
        return

    # Consultar conductor asignado
    cursor.execute("SELECT nombreCompleto, telefono, correoElectronico FROM conductores WHERE placaVehiculo=?", (placa,))
    conductor = cursor.fetchone()

    # Consultar mantenimientos
    cursor.execute("SELECT fechaServicio, descripcionServicio, valorFacturado FROM mantenimientos WHERE placaVehiculo=?", (placa,))
    mantenimientos = cursor.fetchall()

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

    c.drawString(50, 500, "Mantenimientos recientes:")
    y = 480
    for m in mantenimientos:
        c.drawString(60, y, f"{m[0]} - {m[1]} (${m[2]})")
        y -= 20

    c.save()
    print(f"Ficha PDF generada: {archivo}")

# ------------------------------------------------------------
# MENÚS
# ------------------------------------------------------------

def menuVehiculos(connection):
    while True:
        print("\n=== MENÚ VEHÍCULOS ===")
        print("1. Registrar vehículo")
        print("2. Consultar vehículo")
        print("3. Actualizar estado")
        print("4. Actualizar Polizas")
        print("5. Lista de Vehiculos activos")
        print("6. Generar ficha PDF")
        print("7. Volver al menú principal")

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
            generarFichaVehiculoPDF(connection)
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")

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
            print("Opción no válida.")

def menuMantenimientos(connection):
    while True:
        print("\n=== MENÚ MANTENIMIENTOS ===")
        print("1. Registrar mantenimiento")
        print("2. Volver al menú principal")
        opcion = input("Seleccione: ")
        if opcion == "1":
            registrarMantenimiento(connection)
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")

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
        print("4. Salir")

        opcion = input("Seleccione: ")
        if opcion == "1":
            menuVehiculos(connection)
        elif opcion == "2":
            menuConductores(connection)
        elif opcion == "3":
            menuMantenimientos(connection)
        elif opcion == "4":
            print("Saliendo...")
            connection.close()
            break
        else:
            print("Opción no válida.")

# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

if __name__ == "__main__":
    menuPrincipal()
