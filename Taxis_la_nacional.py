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
def inputObligatorio(entrada):
    while True:
        #metodo .strip() para eliminar espacios en blanco de los extremos de la cadena
        entrada = input(entrada).strip()
        if entrada == "":
            print("⚠️ Lo sentimos el campo no puede estar vacio, porfavor intente de nuevo.")
        else:
            return entrada
        
#Fuc. que permite egistrar nuevos vehiculos 
def registrarVehiculo(connection):
    print("\n--- REGISTRAR NUEVO VEHÍCULO ---")
    
    datos = (
        inputObligatorio("Placa: "), 
        inputObligatorio("Marca: "),
        inputObligatorio("Referencia: "),
        inputObligatorio("Modelo: "),
        inputObligatorio("Número de chasis: "),
        inputObligatorio("Número de motor: "),
        inputObligatorio("Color: "),
        inputObligatorio("Concesionario: "),
        inputObligatorio("Fecha de compra (DD/MM/AAAA): "),
        inputObligatorio("Garantía (meses): "),
        inputObligatorio("Fecha compra poliza de seguro (DD/MM/AAAA): "),
        inputObligatorio("Proveedor poliza de seguro: "),
        inputObligatorio("Fecha compra seguro obligatorio (DD/MM/AAAA): "),
        inputObligatorio("Proveedor seguro obligatorio: "),
        inputObligatorio("Activo (1=Sí / 2=No): ")
    )
    
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
    print("Tabla 'conductores' creada correctamente.")


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
        print("Conductor registrado correctamente.")
    except Error as e:
        print("Error al registrar conductor:", e)


def actualizarConductor(connection):
    print("\n--- ACTUALIZAR INFORMACIÓN DE CONDUCTOR ---")
    noId = input("Número de identificación del conductor: ")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noId,))
    fila = cursor.fetchone()

    # Si no se encuentra el conductor, avisar y salir
    if not fila:
        print("No se encontró el conductor.")
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
        print("Información actualizada correctamente.")
    except Error as e:
        print("Error al actualizar:", e)

def consultarConductor(connection):
    print("\n--- CONSULTAR CONDUCTOR ---")
    noId = input("Número de identificación del conductor: ")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM conductores WHERE noIdentificacion=?", (noId,))
    fila = cursor.fetchone()

    if not fila:
        print("No se encontró información del conductor.")
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
                        numeroOrden TEXT PRIMARY KEY NOT NULL,
                        placaVehiculo TEXT NOT NULL,
                        nitProveedor TEXT NOT NULL,
                        nombreProveedor TEXT NOT NULL,
                        descripcionServicio TEXT NOT NULL,
                        valorFacturado REAL NOT NULL,
                        fechaServicio TEXT NOT NULL,
                        FOREIGN KEY (placaVehiculo) REFERENCES vehiculos(placa)
                    )''')
    connection.commit()

def LeerInformacionMantenimiento():
        numeroDeOrden=input("Numero de Orden: ")
        placaVehiculo=input("Placa: ")
        nit=input("Nit: ")
        nombreProveedor=input("Proveedor: ")
        descripcionServicio=input("Servicio Prestado: ")
        valorFacturado=input("Valor Facturado: ")
        from datetime import datetime    #Importar datatime para poder utilizar fechas
        fecha=True
        while fecha==True:
                    fechaServicio =input("Fecha de Servecio en formato dd/mm/aaaa: ")
                    try:
                        fecha= datetime.strptime(fechaServicio, "%d/%m/%Y").date()    #Convertir la cadena string en un objeto datetime
                        fecha_base = fecha.strftime("%Y-%m-%d")    #Convertir objeto datetime en una cadena legible
                        break
                    except ValueError:
                        print("Fecha invalida,  ingrese de nuevo la fecha ")
        mantenimiento=(numeroDeOrden, placaVehiculo, nit, nombreProveedor, descripcionServicio, valorFacturado, fecha_base)    #Variale utilizada para formar una tupla con los datos ingresados
        return mantenimiento    #Devolver la variable para poder ser utilizada en otros metodos

def CrearMantenimiento(connection,mant):
    try:
        cursorObj=connection.cursor()
        cursorObj.execute('''INSERT INTO mantenimientos (numeroOrden, placaVehiculo, nitProveedor, nombreProveedor, descripcionServicio, valorFacturado, fechaServicio) Values(?,?,?,?,?,?,?)''',mant)
        connection.commit()
        print("Se creo correctamente el mantenimiento ")
    except sqlite3.IntegrityError as error:    #Excepciòn de error de integridad para evitar que hallan campos vacios o numeros de orden repetidos
        if "UNIQUE constraint failed" in str(error):
            print("Numero de orden repetido")
        else:
            print("No se aceptan campos vacios, por favor ingresar de nuevo los datos " )

def ActualizarMantenimientoRealizado(connection):
    try:
        cursorObj=connection.cursor()
        numeroDeOrden=input("Numero de Orden: ")
        cursorObj.execute("SELECT 1 FROM mantenimientos WHERE numeroOrden="+numeroDeOrden)
        if cursorObj.fetchone() is None:    #Obtener una sola fila del resultado de la consulta para que si no encuentra nada imprima un mensaje de error
                print("No se encontro Mantenimiento, Numero de orden inexistente")
                return    #Si encuentra alo devuelve el valor, si no encuentra nada devuelve None
        placaVehiculo=input("Placa: ")
        nit=input("Nit: ")
        nombreProveedor=input("Nombre del Proveedor")
        descripcionServicio=input("Descripciòn del Servicio Prestado: ")
        valorFacturado=input("Valor Facturado: ")
        from datetime import datetime
        fecha=True    #Valor booleano para poder crear un bucle while hasta que la fecha sea ingresada correctamente
        while fecha==True:
                    fechaServicio =input("Fecha de Servecio en formato dd/mm/aaaa: ")
                    try:
                        fecha= datetime.strptime(fechaServicio, "%d/%m/%Y").date()
                        fecha_base = fecha.strftime("%Y-%m-%d")
                        break    #Salir del bulce si el usuario ingresa de forma correcta la fecha
                    except ValueError:    #Captura el error si la fecha esta en un formato invalido
                        print("Fecha invalida,  ingrese de nuevo la fecha ")
        #Si alguno de los campos esta vacio imprimira un mensaje de error, el operador not invierte el valor logico y strip elimina los espacios al inicio y al final de la cadena
        if (not placaVehiculo.strip() or not nit.strip() or not nombreProveedor.strip() or
            not descripcionServicio.strip() or not valorFacturado.strip() or not fechaServicio.strip()):
            print("No se aceptan campos vacíos. Por favor ingrese de nuevo los datos.")
            return
        cad = ( "UPDATE mantenimientos SET "
                        "placaVehiculo='" + placaVehiculo + "', "
                        "nitProveedor='" + nit + "', "
                        "nombreProveedor='" + nombreProveedor + "', "
                        "descripcionServicio='" + descripcionServicio + "', "
                        "valorFacturado='" + valorFacturado + "', "
                        "fechaServicio='" + fechaServicio + "' "
                        "WHERE numeroDeOrden='" + numeroDeOrden + "'")
        cursorObj.execute(cad)
        connection.commit()
        print("Se actualizo correctamente el Mantenimiento con el Numero de Orden:  ",numeroDeOrden)
    except sqlite3.OperationalError as error:    #Atrapa el error de integridad como "error"
            print("campos vacios o invalidos ")

def ConsultarMantenimientoRealizado(connection):
    try:
        cursorObj=connection.cursor()
        numeroDeOrden=input("Numero de Orden: ")
        cad='SELECT numeroOrden,  placaVehiculo, nitProveedor, nombreProveedor, descripcionServicio,  valorFacturado,fechaServicio FROM mantenimientos WHERE numeroOrden='+numeroDeOrden
        cursorObj.execute(cad)
        filas=cursorObj.fetchall()    #Recupera todos los datos de cad
        if not filas:    #Si filas esta vacio entonces saltara un mensaje de error
            print("Numero de orden inexistente")
            return
        else:
            for row in filas:    #Filas en las que se atrapan los datos obtenidos de forma ordenada y coherente con el numero de columnas de la tabla
                numeroDeOrden=row[0]
                placa=row[1]
                ni=row[2]
                proveedor=row[3]
                descripcion = row[4]
                valor = row[5]
                fecha = row[6]
                
                print("Numero de Orden: ",numeroDeOrden,
                      "\nPlaca: ",placa,
                      "\nProveedor: ",proveedor,
                      "\nNit: ",ni,
                      "\nDescripcion del servicio prestado: ",descripcion,
                      "\nValor facturado: ",valor,
                      "\nFecha del servicio: ",fecha)
    except sqlite3.OperationalError as error:    #Detectar si el campo esta vacio
            print("Campo vacio")
            
def BorrarMantenimiento(connection):
    try:
        cursorObj=connection.cursor()
        numeroDeOrden=input("Numero de Orden: ")
        cad='DELETE FROM mantenimientos WHERE  numeroOrden='+numeroDeOrden  
        cursorObj.execute(cad)
        if cursorObj.rowcount == 0:    #Saber cuantas columnas de la tabla fueron afectadsa en la ejecuciòn, si fueron 0 entonce marcara un mensaje de error
            print("Numero de orden inexistente, no se pudo eliminar nada")
        else:
            print("Se elimino el mantenimiento con el numero de orden: ",numeroDeOrden)
        connection.commit()
    except sqlite3.OperationalError as error:    #Detectar si el campo esta vacio
            print("Campo vacio")
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
    print(f"Ficha PDF generada: {archivo}")

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
    
