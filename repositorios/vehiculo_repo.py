import sqlite3
from datetime import datetime

#Conexion con mi objeto
from modulos.vehiculo import Vehiculo

# ============================================================
#           REPOSITORIO DE VEHÍCULOS (CRUD)
# ============================================================

class RepositorioVehiculo:
    
    def __init__(self, connection):
        self.connection = connection
        self.crear_tabla()
    
    # =================
    #   CREAR TABLA
    # =================

    def crear_tabla(self):
        cursor = self.connection.cursor()
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
        self.connection.commit()
    
    # ============================================================
    # Convertir fila SQL → objeto Vehiculo
    # ============================================================
    
    def infVehiculo_a_objecto(self, infVehiculo):
        if infVehiculo is None:
            return None
        return Vehiculo(
            placa = infVehiculo[0],
            marca = infVehiculo[1],
            referencia = infVehiculo[2],
            modelo = infVehiculo[3],
            numero_chasis = infVehiculo[4],
            numero_motor = infVehiculo[5],
            color = infVehiculo[6],
            concesionario = infVehiculo[7],
            fecha_compra_vehiculo = infVehiculo[8],
            tiempo_garantia = infVehiculo[9],
            fecha_compra_poliza_seguro = infVehiculo[10],
            proveedor_poliza_seguro = infVehiculo[11],
            fecha_compra_segObligatorio = infVehiculo[12],
            proveedor_segObligatorio = infVehiculo[13],
            activo = infVehiculo[14]
        )
        
    # ============================================================
    # Guardar vehículo en BD (reemplaza registrarVehiculo)
    # ============================================================
    
    def guardar(self, vehiculo):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''INSERT INTO vehiculos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                           ''', vehiculo.infVehiculo())
            self.connection.commit()
            print("✅ Vehículo registrado correctamente.")
        except sqlite3.IntegrityError:
            print(f"❌ Error el vehiculo ya se encuntra registrado: ")
        except Exception as e:
            print(f"❌ Error al registrar el vehiculo: ", e) 
        
    # ============================================================
    # Buscar vehículo por placa (reemplaza consultarVehiculo)
    # ============================================================ 
    
    def buscar_por_placa(self, placa):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM vehiculos WHERE placa=?", (placa.upper(),))
        infVehiculo = cursor.fetchone()
        return self.infVehiculo_a_objecto(infVehiculo)

    # ============================================================
    # Actualizar estado (Activo=1 / Inactivo=2)
    # ============================================================
    
    def actualizar_estado(self, placa, nuevo_estado):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE vehiculos SET activo=? WHERE placa=?", (nuevo_estado, placa.upper()))
        self.connection.commit()
        print("✅ Estado del vehículo actualizado correctamente.")
        
    # ============================================================
    # Actualizar pólizas (reemplaza actualizarPolizaVehiculo)
    # ============================================================
    
    def actualizar_poliza(self, vehiculo):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE vehiculos
                       SET 
                       fechaCompraPolizaSeguro=?, 
                       proveedorPolizaSeguro=?, 
                       fechaCompraSegObligatorio=?, 
                       proveedorSegObligatorio=?
                       WHERE placa=?''', 
                       (vehiculo._fecha_compra_poliza_seguro,
                        vehiculo._proveedor_poliza_seguro,
                        vehiculo._fecha_compra_segObligatorio,
                        vehiculo._proveedor_segObligatorio,
                        vehiculo._placa))
        self.connection.commit()
        print("✅ Póliza de seguro obligatorio actualizada exitosamente.")

    # ============================================================
    # Listar vehículos activos (reemplaza listaVeiculosActivos)
    # ============================================================
    
    def lista_activos(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT placa, marca, referencia, modelo, 
                       color FROM vehiculos WHERE activo=1''')
        return cursor.fetchall()        