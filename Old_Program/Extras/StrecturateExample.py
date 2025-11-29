import sqlite3
from sqlite3 import Error  # Library

# Connection Method
def conexionDB():
    try:
        # We just built a connection to work with our DataBase
        con = sqlite3.connect('BDEjemplo.db')
        return con
    except Error as e:
        print("Database connection failed", e)

# Close Connection Method
def cerrarDB(con): #We need "con" to know which file we're referent
    con.close()


# Build Table Method
def crearTablaVehiculos(con):
    cursorObj = con.cursor()
    cad = ''' CREATE TABLE IF NOT EXISTS vehiculos(
                                    placa text NOT NULL,
                                    marca text NOT NULL,
                                    referencia text NOT NULL,
                                    modelo integer NOT NULL,
                                    numeroChasis text NOT NULL,
                                    numeroMotor text NOT NULL,
                                    color text NOT NULL,
                                    concesionario text NOT NULL,
                                    fechaCompraVehiculo date NOT NULL,
                                    tiempoGarantia integer NOT NULL,
                                    fechaCompraSegObliga date NOT NULL,
                                    proveedorDegOpbli text NOT NULL,
                                    Activo integer NOT NULL,
                                    PRIMARY KEY(placa))'''
    cursorObj.execute(cad)
    con.commit()


# Second Table
def crearTablaVehiculos1(con):
    cursorObj = con.cursor()
    cursorObj.execute(''' CREATE TABLE IF NOT EXISTS vehiculos(
                                    placa text NOT NULL,
                                    marca text NOT NULL,
                                    referencia text NOT NULL,
                                    modelo integer NOT NULL,
                                    numeroChasis text NOT NULL,
                                    numeroMotor text NOT NULL,
                                    color text NOT NULL,
                                    concesionario text NOT NULL,
                                    fechaCompraVehiculo date NOT NULL,
                                    tiempoGarantia integer NOT NULL,
                                    fechaCompraSegObliga date NOT NULL,
                                    proveedorDegOpbli text NOT NULL,
                                    Activo integer NOT NULL,
                                    PRIMARY KEY(placa))''')
    con.commit()


# Build Insert Data
def insertarVehiculos(con):
    cursorObj = con.cursor()
    cad = '''INSERT INTO vehiculos VALUES("LSV252",
                                        "RENAULT",
                                        "SYMBOL",
                                        2014,
                                        "123asd",
                                        "456lki",
                                        "BLANCO",
                                        "Los Coches",
                                        "12/02/2013",
                                        36,
                                        "12/09/2013",
                                        "Seguros del Estado",
                                        1)
    '''
    cursorObj.execute(cad)
    con.commit()


# Maintenance Vehicle
def crearTablaMantenimientoVehiculo(con):
    cursorObj = con.cursor()
    cursorObj.execute(''' CREATE TABLE IF NOT EXISTS mantenimientoVehiculo(
                                    numeroOrden integer NOT NULL,
                                    placaVehiculo text NOT NULL,
                                    nit text NOT NULL,
                                    nombreProveedor text NOT NULL,
                                    descripcionServicio text NOT NULL,  
                                    valorFacturado integer NOT NULL,
                                    fechaServicio date NOT NULL,
                                    PRIMARY KEY(numeroOrden))''')
    con.commit()


# Insert Maintenance Vehicle data
def leerInformacionMantenimiento():
    numeroOrden_inser = input("Order Number: ")
    placaVehiculo_inser = input("Plate: ")
    nit_inser = input("NIT: ")
    nombreProveedor_inser = input("Supplier: ")
    descripcionServicio_inser = input("Type of service: ")
    valorFacturado_inser = input("Invoced Price: ")
    fechaServicio_inser = "12/10/2025"
    mantenimiento = (numeroOrden_inser,
                     placaVehiculo_inser,
                     nit_inser,
                     nombreProveedor_inser,
                     descripcionServicio_inser,
                     valorFacturado_inser,
                     fechaServicio_inser)
    print("Manthenice Tuple: ", mantenimiento, type(mantenimiento))
    return mantenimiento


def crearMantenimiento(con, mant):
    cursorObj = con.cursor()
    cursorObj.execute(''' INSERT INTO mantenimientoVehiculo
                        VALUES (?,?,?,?,?,?,?)''', mant)
    con.commit()


def crearMantenimiento1(con):
    numeroOrden_inser = input("Order Number: ")
    placaVehiculo_inser = input("Plate: ")
    nit_inser = input("NIT: ")
    nombreProveedor_inser = input("Supplier: ")
    descripcionServicio_inser = input("Type of service: ")
    valorFacturado_inser = input("Invoced Price: ")
    fechaServicio_inser = "12/10/2025"
    mantenimiento = (numeroOrden_inser,
                     placaVehiculo_inser,
                     nit_inser,
                     nombreProveedor_inser,
                     descripcionServicio_inser,
                     valorFacturado_inser,
                     fechaServicio_inser)
    print("Manthenice Tuple: ", mantenimiento, type(mantenimiento))
    cursorObj = con.cursor()
    cursorObj.execute(''' INSERT INTO mantenimientoVehiculo
                        VALUES (?,?,?,?,?,?,?)''', mantenimiento)
    con.commit()


# UPDATE + WHERE
def actualizarMantenimientoRealizado(con):
    numeroOrden_inser = input("Order Number: ")
    placaVehiculo_inser = input("Plate: ")
    valorFacturado_inser = input("Invoced Price: ")

    cursorObj = con.cursor()
    cad = 'UPDATE mantenimientoVehiculo SET placaVehiculo="' + placaVehiculo_inser + '", valorFacturado=' + valorFacturado_inser + ' WHERE numeroOrden=' + numeroOrden_inser
    print("The chain to execute is: ", cad)
    cursorObj.execute(cad)
    con.commit()


# SELECT + WHERE
def consultarMantenimientoRealizado(con):
    cursorObj = con.cursor()
    numeroOrden = input('Order number: ')
    cad = 'SELECT numeroOrden, placaVehiculo, nit, nombreProveedor, valorFacturado, fechaServicio FROM mantenimientoVehiculo WHERE numeroOrden=' + numeroOrden
    print('The Chain to execute is: ', cad)
    cursorObj.execute(cad)

    filas = cursorObj.fetchall()
    print("The type of data in the rows is: ", type(filas))
    for row in filas:
        numeroOrden_inser = row[0]
        placaVehiculo_inser = row[1]
        nombreProveedor_inser = row[3]
        print('Num of Order: ', numeroOrden_inser, 'Plate: ', placaVehiculo_inser, 'Supplier: ', nombreProveedor_inser)
    con.commit()


# All rows in one line
def consultarMantenimientoRealizado1(con):
    numeroOrden = input('Order number: ')
    cursorObj = con.cursor()
    cad = 'SELECT * FROM mantenimientoVehiculo WHERE numeroOrden=' + numeroOrden
    print('The Chain to execute is: ', cad)
    cursorObj.execute(cad)

    filas = cursorObj.fetchall()
    print("The type of data in the rows is: ", type(filas))
    for row in filas:
        numeroOrden_inser = row[0]
        placaVehiculo_inser = row[1]
        nombreProveedor_inser = row[3]
        print('Num of Order: ', numeroOrden_inser, 'Plate: ', placaVehiculo_inser, 'Supplier: ', nombreProveedor_inser)


# Sum rows
def consultarMantenimientoRealizado2(con):
    cursorObj = con.cursor()
    cad = 'SELECT sum(valorFacturado) FROM mantenimientoVehiculo'
    print('The Chain to execute is: ', cad)
    cursorObj.execute(cad)
    filas = cursorObj.fetchall()
    print("The type of data in the rows is: ", type(filas))
    for row in filas:
        totalFacturado = row[0]
        print('Total Invoice: ', totalFacturado)
    con.commit()


# Last maintenance provided
def consultarMantenimientoRealizado3(con):
    cursorObj = con.cursor()
    cad = 'SELECT max(fechaServicio) FROM mantenimientoVehiculo'
    print('The Chain to execute is: ', cad)
    cursorObj.execute(cad)
    filas = cursorObj.fetchall()
    print("The type of data in the rows is: ", type(filas))
    for row in filas:
        fechaServicio_inser = row[0]
        print('Services Date: ', fechaServicio_inser)

    cad = 'SELECT * FROM mantenimientoVehiculo WHERE fechaServicio="' + fechaServicio_inser + '"'
    print('The Chain to execute is: ', cad)
    cursorObj.execute(cad)

    filas = cursorObj.fetchall()
    print("The type of data in the rows is: ", type(filas))
    for row in filas:
        numeroOrden_inser = row[0]
        placaVehiculo_inser = row[1]
        nombreProveedor_inser = row[3]
        fechaServicio_inser_M = row[6]
        print('Num of Order: ', numeroOrden_inser, 'Plate: ', placaVehiculo_inser, 'Supplier: ', nombreProveedor_inser)


# Delete something
def borrarMantenimineto(con):
    numeroOrden = input('Order number: ')
    cursorObj = con.cursor()
    cad = 'DELETE FROM mantenimientoVehiculo WHERE numeroOrden=' + numeroOrden
    print('Chain: ', cad)
    cursorObj.execute(cad)
    con.commit()
    
def borrarTablaVehiculos(con):
    cursorObj = con.cursor()
    cad='''DROP TABLE vehiculos'''
    print("Chain: ",cad)
    cursorObj.execute(cad)
    con.commit()

#Create a MENU
def menu(con):
    salirPrincipal=False #Flag
    while not salirPrincipal:
        opcPrincipal=input('''
                    MENU PRINCIPAL TAXIS LA NACIONAL

                    1- Menu de gestion de Vehiculos
                    2- Menu de gestion de Conductores
                    3- Menu de gestion de Mantenimiento
                    4- Ficha de Vehiculo
                    5- Salir

                    Seleccione una opcion: >>> ''')
        if (opcPrincipal == '1'):
            salirPrincipal=True
        elif (opcPrincipal == '2'):
            salirConductores=False
            while not salirConductores:
                opcConductores=input('''
                MENU DE ADMINISTRACION DE CONDUCTORES

                1- Crear un nuevo conductor
                2- Actualizar informacion conductor
                3- Consultar informacion de un conductor
                4- Regrezar al menu principal
                
                Seleccione una opcion: >>> ''')
                if (opcConductores=='1'):
                    salirConductores=True
                elif (opcConductores=='2'):
                    salirConductores=True
                elif (opcConductores=='3'):
                    salirConductores=True
                elif (opcConductores=='4'):
                    salirConductores=True
        elif (opcPrincipal == '3'):
            salirMantenimientos=False
            while not salirMantenimientos:
                opcMantenimientos=input('''
                    MENU DE MANTENIMIENTOS

                    1- Crear un mantenimiento
                    2- Consultar un mantenimiento realizado
                    3- Borrar un mantenimiento
                    4- Retornar al menu principal

                    Seleccione una opcion: >>> ''')
                if (opcMantenimientos =='1'):
                    miMantenimiento = leerInformacionMantenimiento()
                    crearMantenimiento(con, miMantenimiento)
                elif (opcMantenimientos =='2'):
                    consultarMantenimientoRealizado(con)
                elif (opcMantenimientos =='3'):
                    borrarMantenimineto(con)
                elif (opcMantenimientos =='4'):
                    salirMantenimientos=True 
                
        elif (opcPrincipal == '4'):
            salirPrincipal=True
        elif (opcPrincipal == '5'):
            salirPrincipal=True


def main():
    miCon = conexionDB()
    menu(miCon)
    # Uncomment what you need to test:
    # crearTablaVehiculos(miCon)
    # crearTablaVehiculos1(miCon)
    # crearTablaMantenimientoVehiculo(miCon)
    miMantenimiento = leerInformacionMantenimiento()
    crearMantenimiento(miCon, miMantenimiento)
    # crearMantenimiento1(miCon)
    # insertarVehiculos(miCon)
    # actualizarMantenimientoRealizado(miCon)
    consultarMantenimientoRealizado(miCon)
    # consultarMantenimientoRealizado1(miCon)
    # consultarMantenimientoRealizado2(miCon)
    # consultarMantenimientoRealizado3(miCon) 
    #borrarTablaVehiculos(miCon)
    borrarMantenimineto(miCon)
    
    cerrarDB(miCon)
    


main()
