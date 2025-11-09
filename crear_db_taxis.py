import sqlite3

def crear_base_datos():
    connection = sqlite3.connect("taxis_la_nacional.db")
    cursor = connection.cursor()

    # ----------------------------------------------------------
    # Crear tabla VEHICULOS
    # ----------------------------------------------------------
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

    # ----------------------------------------------------------
    # Crear tabla CONDUCTORES
    # ----------------------------------------------------------
    cursor.execute('''CREATE TABLE IF NOT EXISTS conductores(
                        noIdentificacion TEXT PRIMARY KEY,
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
                        FOREIGN KEY (placaVehiculo) REFERENCES vehiculos(placa)
                    )''')

    # ----------------------------------------------------------
    # Crear tabla MANTENIMIENTOS
    # ----------------------------------------------------------
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

    # ----------------------------------------------------------
    # Insertar datos en VEHICULOS
    # ----------------------------------------------------------
    vehiculos = [
        ("TLA001","Toyota","Corolla XEI",2020,"CH001TLA001","MT001TLA001","Blanco","Toyota Andino","12/01/2020",36,"10/01/2024","Sura","12/01/2024","AXA Colpatria",1),
        ("TLA002","Chevrolet","Onix LTZ",2021,"CH002TLA002","MT002TLA002","Gris","Chevrolet Caribe","25/02/2021",48,"05/03/2024","Seguros Bolívar","10/03/2024","Sura",1),
        ("TLA003","Kia","Rio Sedan",2019,"CH003TLA003","MT003TLA003","Rojo","Kia Motors Norte","15/03/2019",36,"20/03/2023","AXA Colpatria","25/03/2023","Sura",2),
        ("TLA004","Nissan","Versa Sense",2022,"CH004TLA004","MT004TLA004","Azul","Nissan Centro","03/05/2022",60,"15/05/2024","Mapfre","20/05/2024","AXA Colpatria",1),
        ("TLA005","Hyundai","Accent Vision",2020,"CH005TLA005","MT005TLA005","Negro","Hyundai Motorland","10/07/2020",48,"12/07/2024","Sura","15/07/2024","Seguros Bolívar",1),
        ("TLA006","Renault","Logan Life",2018,"CH006TLA006","MT006TLA006","Amarillo","Renault La Sabana","09/09/2018",36,"10/09/2023","AXA Colpatria","12/09/2023","Mapfre",2),
        ("TLA007","Mazda","3 Touring",2021,"CH007TLA007","MT007TLA007","Plata","Mazda MotorCity","14/10/2021",48,"20/10/2024","Seguros Bolívar","22/10/2024","Sura",1),
        ("TLA008","Suzuki","Swift GLX",2019,"CH008TLA008","MT008TLA008","Blanco","Suzuki Andes","18/11/2019",36,"22/11/2023","Mapfre","25/11/2023","AXA Colpatria",2),
        ("TLA009","Volkswagen","Voyage Trend",2020,"CH009TLA009","MT009TLA009","Gris","VW Autonorte","05/01/2020",48,"07/01/2024","Sura","10/01/2024","Seguros Bolívar",1),
        ("TLA010","Ford","Fiesta SE",2018,"CH010TLA010","MT010TLA010","Rojo","Ford Motorland","25/02/2018",36,"28/02/2023","Mapfre","03/03/2023","AXA Colpatria",2),
        ("TLA011","Toyota","Yaris Sedan",2023,"CH011TLA011","MT011TLA011","Blanco","Toyota Andino","10/04/2023",60,"15/04/2024","Sura","20/04/2024","Seguros Bolívar",1),
        ("TLA012","Chevrolet","Spark GT",2019,"CH012TLA012","MT012TLA012","Amarillo","Chevrolet Caribe","15/05/2019",36,"18/05/2023","AXA Colpatria","21/05/2023","Sura",2),
        ("TLA013","Kia","Picanto Ion",2020,"CH013TLA013","MT013TLA013","Plata","Kia Motors Norte","12/06/2020",48,"15/06/2024","Seguros Bolívar","18/06/2024","AXA Colpatria",1),
        ("TLA014","Hyundai","Elantra GLS",2021,"CH014TLA014","MT014TLA014","Azul","Hyundai Motorland","08/07/2021",48,"10/07/2024","Sura","12/07/2024","Mapfre",1),
        ("TLA015","Renault","Sandero Stepway",2019,"CH015TLA015","MT015TLA015","Gris","Renault La Sabana","22/08/2019",36,"25/08/2023","Mapfre","28/08/2023","AXA Colpatria",2),
        ("RKK118","KIA","CERATO",2012,"N","1","GRIS","NO TIENE","9/11/2025",36,"9/12/2025","SDK","09/11/2025","MIT",2)
    ]

    cursor.executemany("INSERT OR IGNORE INTO vehiculos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", vehiculos)
   
    # ----------------------------------------------------------
    # Insertar datos en CONDUCTORES
    # ----------------------------------------------------------
    conductores = [
        ("12345678","Pepito Perez","Crra 80 No 25h-44","3228765403","pep_per@gmail.com","TLA001","20/01/2020","","1","1","100000","30000","0","0"),
        ("1012356789","Carlos Gómez","Calle 10 No12-34","104567890","carlosg@gmail.com","TLA002","28/02/2021","","1","2","50000","20000","0","10000"),
        ("1010010001","Carlos Ramírez","Cra 12 #45-23","3105678912","carlos.ramirez@email.com","TLA001","15/03/2018","10/06/2020","3","1","95000","50000","0","0"),
        ("1010010002","María Gómez","Cl 8 #21-45","3124589621","maria.gomez@email.com","TLA002","22/07/2019","","1","2","80000","60000","20000","10000"),
        ("1010010003","Jorge Martínez","Av 68 #90-12","3015698741","jorge.martinez@email.com","TLA002","10/02/2020","","1","2","80000","55000","0","0"),
        ("1010010004","Sandra López","Cl 45 #22-19","3204785120","sandra.lopez@email.com","TLA003","25/11/2021","","1","1","92000","60000","0","5000"),
        ("1010010005","Ricardo Pérez","Cra 80 #30-60","3115879623","ricardo.perez@email.com","TLA004","18/06/2018","12/12/2020","3","1","97000","48000","0","0"),
        ("1010010006","Luisa Fernández","Cl 100 #25-33","3136985214","luisa.fernandez@email.com","TLA005","01/09/2019","","1","2","85000","62000","10000","3000"),
        ("1010010007","Andrés Castillo","Cra 50 #77-12","3147896520","andres.castillo@email.com","TLA005","05/01/2022","","1","2","85000","58000","0","0"),
        ("1010010008","Diana Morales","Cl 40 #19-56","3004561237","diana.morales@email.com","TLA006","14/05/2023","","1","1","90000","54000","0","0"),
        ("1010010009","Felipe Torres","Av Suba #130-21","3206987412","felipe.torres@email.com","TLA007","09/08/2020","20/12/2021","3","1","93000","49000","0","0"),
        ("1010010010","Laura Sánchez","Cl 33 #10-44","3125968740","laura.sanchez@email.com","TLA008","17/03/2021","","1","2","81000","55000","15000","5000"),
        ("1010010011","Pedro Jiménez","Cra 90 #55-20","3156897452","pedro.jimenez@email.com","TLA008","12/02/2024","","1","2","81000","57000","0","0"),
        ("1010010012","Camila Herrera","Cl 15 #66-32","3197845623","camila.herrera@email.com","TLA009","03/01/2025","","1","1","88000","53000","0","0"),
        ("1010010013","Santiago Ruiz","Cra 22 #11-30","3104579823","santiago.ruiz@email.com","TLA010","11/07/2022","","1","1","92000","59000","0","0"),
        ("1010010014","Natalia Torres","Cl 77 #50-12","3148761235","natalia.torres@email.com","TLA011","09/09/2018","10/10/2020","3","1","91000","56000","0","0"),
        ("1010010015","Diego Mendoza","Av Caracas #120-45","3126987451","diego.mendoza@email.com","TLA012","19/11/2019","","1","1","94000","62000","0","0"),
        ("1010010016","Valentina Rojas","Cl 88 #33-21","3207896542","valentina.rojas@email.com","TLA013","02/06/2020","","1","2","87000","53000","0","0"),
        ("1010010017","David García","Cra 15 #18-90","3112369874","david.garcia@email.com","TLA013","15/09/2022","","1","2","87000","55000","0","0"),
        ("1010010018","Paula Restrepo","Cl 99 #70-55","3006549872","paula.restrepo@email.com","TLA014","07/04/2023","","1","1","89000","56000","0","0"),
        ("1010010019","Sebastián López","Cra 33 #11-15","3104589632","sebastian.lopez@email.com","TLA015","20/02/2018","10/01/2020","3","1","95000","50000","0","0"),
        ("1010010020","Ana María Castro","Cl 23 #45-78","3124587961","ana.castro@email.com","TLA015","12/06/2021","","1","2","82000","52000","0","0")
    ]

    cursor.executemany("INSERT OR IGNORE INTO conductores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", conductores)

    # ----------------------------------------------------------
    # Insertar datos de prueba en MANTENIMIENTOS
    # ----------------------------------------------------------
    mantenimientos = [
        ("MT001","TLA001","900123456","Taller Toyota Andino","Cambio de aceite y filtros",250000,"12/03/2024"),
        ("MT002","TLA002","901234567","Chevrolet Caribe Service","Revisión de frenos y alineación",180000,"15/04/2024"),
        ("MT003","TLA003","902345678","Kia Motors Norte","Cambio de pastillas de freno",220000,"20/05/2024"),
        ("MT004","TLA004","903456789","Nissan Centro","Cambio de llantas delanteras",400000,"25/06/2024"),
        ("MT005","TLA005","904567890","Hyundai Motorland","Cambio de batería",300000,"05/07/2024")
    ]
    cursor.executemany('''INSERT OR IGNORE INTO mantenimientos VALUES (?,?,?,?,?,?,?)''', mantenimientos)

    # ----------------------------------------------------------
    connection.commit()
    connection.close()
    print("✅ Base de datos 'taxis_la_nacional.db' creada exitosamente con tablas y datos de prueba.")

if __name__ == "__main__":
    crear_base_datos()

