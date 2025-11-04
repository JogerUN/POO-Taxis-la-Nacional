# Libraries Required 
import sqlite3
from sqlite3 import Error 

# Conenection Method 
def conexionDB():
    try: 
        connection = sqlite3.connect('La_Nacional_de_Taxis_DB.db')
        return connection
    except Error as error:
        print("DataBase connection failed ❌: ", error)
        
# Close connection
def cerrarDB(connection):
    connection.close()

# [1] Vehicles Module
def crearTablaVehiculos(connection):
    cursorObj = connection.cursor()
    cad='''CREATE TABLE IF NOT EXISTS vehiculos(
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
                proveedorSegObli text NOT NULL,
                Activo integer NOT NULL,
                PRIMARY KEY(placa)
            ) '''
    cursorObj.execute(cad)
    connection.commit()
    print("Tabla creada exitosamente ✅")
    
def insertarVehiculos(connection):
    #Info. of Vehicule given for user
    placa_insert=input("Numero de Placa: ")
    marca_insert=input("Marca del vehiculo: ")
    referencia_insert=input("Referencia del vehiculo: ")
    modelo_insert=input("Modelo del vehiculo: ")
    numeroChasis_insert=input("Numero del Chasis: ")
    numeroMotor_insert=input("Numero del Motor: ")
    color_insert=input("Color del vehiculo: ")
    concesionario_insert=input("Concesionario de compra: ")                                    
    fechaCompraVehiculo_insert=input("Fecha de compra del vehiculo (DD/MM/AAAA): ")
    tiempoGarantia_insert=input("Tiempo de garantia en meses: ")
    fechaCompraSegObliga_insert=input("Fechas de compra del seguro (DD/MM/AAAA): ")
    proveedorDegOpbli_insert=input("Proovedor del seguro: ")
    Activo_insert=input("Esta activo (Si=1 / No=2:) ")
    
    info_vehiculo = (placa_insert,
                marca_insert,
                referencia_insert,
                modelo_insert,
                numeroChasis_insert,
                numeroMotor_insert,
                color_insert,
                concesionario_insert,
                fechaCompraVehiculo_insert,
                tiempoGarantia_insert,
                fechaCompraSegObliga_insert,
                proveedorDegOpbli_insert,
                Activo_insert)
    
    print("Informacion del vehiculo registrada: ", info_vehiculo) 
    
    cursorOjb=connection.cursor()
    # Avoid craches by same value in Numero de Placa
    try:
        cursorOjb.execute(''' INSERT INTO vehiculos VALUES 
                      (?,?,?,?,?,?,?,?,?,?,?,?,?)''',info_vehiculo)
        connection.commit()
        print("Vehiculo registrado exitosamente. ✅")
    except Error as e:
        print("Error al insertar informacion: ",e)
        

#Consult vehicule info. by Numero de Palca
def consultarInfoVehiculo(connection):
    placa=input("Numero de Placa: ")
    cursorOjb=connection.cursor()
    #Avoid SQL Injection
    cursorOjb.execute('SELECT * FROM vehiculos WHERE placa=?', (placa,))
    filas=cursorOjb.fetchall()
    
    if not filas:
        print(f"No se encontro informcaion para la placa: {placa}.")
        return
    
    print(f"La informacion de vehiculo deL vehivulo {placa} es: ")
    for row in filas:
        print(f'''
        Marca: {row[1]}
        Referencia: {row[2]}
        Modelo: {row[3]}
        N. Chasis: {row[4]}
        N. Motor: {row[5]}
        Color: {row[6]}
        Concesionario: {row[7]}
        Fecha de compra: {row[8]}
        Garantia (meses) {row[9]}
        Fecha de compra del seguro: {row[10]}
        Proveedor Seguro: {row[11]}
        Estado activo: {"Si" if row[12]==1 else "No"}
        ''')
        
    #Building a MENU
    def menu(connection):
        salirprincipal = False #Flag
        while not salirprincipal:
            opcPrincipal = input('''
                    MENU PRINCIPAL TAXIS LA NACIONAL

                    1- Menu de gestion de Vehiculos
                    2- Menu de gestion de Conductores
                    3- Menu de gestion de Mantenimiento
                    4- Ficha de Vehiculo
                    5- Salir

                    Seleccione una opcion: >>> ''')
            
            if (opcPrincipal =='1'):
                    salirConductores=False
                    while not salirConductores:
                    
                    optionVehicules = input(''' 
                    MENU DE GESTION DEL VEHICULO
                    
                    1- Crear un nuevo vehiculo
                    2- Consultar informacion de un vehiculo
                    3- Actualizar poliza de sangre
                    4- Actualizacion del estado de Vehiculo (Activo / Inactivo)
                    5- Lista de Vehiculos activos
                    6- Eliminar un Vehiculo
                    7- Regresar al menu principal
                            
                
                    Seleccione una opciom: >>>''')
                    
            elif (optionVehiculo =='2'):
                opcPrincipal  = True
            elif (opcPrincipal =='3'):
                opcPrincipal  = True
            elif (opcPrincipal =='4'):
                opcPrincipal  = True
            elif (opcPrincipal =='5'):
                opcPrincipal  = True 
                        
                        

                       
                                       
def main():
    myConnection = conexionDB()
    miVehiculo= insertarVehiculos()
    creartablaVehiculos(myConnection)
    consultarInfoVehiculo(myConnection)
main()
