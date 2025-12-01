# =============================================================
# REPOSITORIO DE VEHÍCULOS (CRUD) Create Read Update Delete
# Encargado de comunicación con la base de datos exclusivamente.
# =============================================================
import sqlite3
from modulos.vehiculo import Vehiculo


class RepositorioVehiculo:
    
    def __init__(self, connection):
        """
        Recibe una conexión activa a SQLite.
        Crea la tabla si no existe.
        """
        self.connection = connection
        self.crear_tabla()
    
    # =========================================================
    # CREAR TABLA
    # =========================================================
    def crear_tabla(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehiculos(
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
            )
        ''')
        self.connection.commit()

    # =========================================================
    # Convertir fila SQL → objeto Vehiculo
    # =========================================================
    def infVehiculo_a_objeto(self, fila):
        """
        Convierte una tupla SQL a objeto Vehiculo.
        Si la fila es None → retorna None.
        """
        if fila is None:
            return None
        
        return Vehiculo(
            placa=fila[0],
            marca=fila[1],
            referencia=fila[2],
            modelo=fila[3],
            numero_chasis=fila[4],
            numero_motor=fila[5],
            color=fila[6],
            concesionario=fila[7],
            fecha_compra_vehiculo=fila[8],
            tiempo_garantia=fila[9],
            fecha_compra_poliza_seguro=fila[10],
            proveedor_poliza_seguro=fila[11],
            fecha_compra_segObligatorio=fila[12],
            proveedor_segObligatorio=fila[13],
            activo=fila[14]
        )

    # =========================================================
    # GUARDAR VEHICULO
    # =========================================================
    def guardar(self, vehiculo: Vehiculo):
        """
        Inserta un vehículo en la BD.
        Lanza errores si la placa ya existe.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO vehiculos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                vehiculo.infVehiculo()
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise Exception("Vehículo ya registrado (placa duplicada).")
        except Exception as e:
            raise Exception(f"Error al guardar vehículo: {e}")

    # =========================================================
    # BUSCAR POR PLACA
    # =========================================================
    def buscar_por_placa(self, placa: str):
        """
        Busca un vehículo por su placa y retorna un objeto Vehiculo.
        Si no existe, retorna None.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM vehiculos WHERE placa = ?",
            (placa.upper(),)
        )
        fila = cursor.fetchone()
        return self.infVehiculo_a_objeto(fila)

    # =========================================================
    # ACTUALIZAR ESTADO (1/2)
    # =========================================================
    def actualizar_estado(self, placa: str, nuevo_estado: int):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE vehiculos SET activo=? WHERE placa=?",
            (nuevo_estado, placa.upper())
        )
        self.connection.commit()

    # =========================================================
    # ACTUALIZAR POLIZAS
    # =========================================================
    def actualizar_poliza(self, vehiculo: Vehiculo):
        """
        Actualiza pólizas en base al objeto Vehiculo recibido.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE vehiculos SET 
                fechaCompraPolizaSeguro=?, 
                proveedorPolizaSeguro=?, 
                fechaCompraSegObligatorio=?, 
                proveedorSegObligatorio=?
            WHERE placa=?
        ''',
        (
            vehiculo._fecha_compra_poliza_seguro,
            vehiculo._proveedor_poliza_seguro,
            vehiculo._fecha_compra_segObligatorio,
            vehiculo._proveedor_segObligatorio,
            vehiculo._placa
        ))
        self.connection.commit()

    # =========================================================
    # LISTA DE VEHÍCULOS ACTIVOS
    # =========================================================
    def lista_activos(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT placa, marca, referencia, modelo, color
            FROM vehiculos
            WHERE activo = 1
        ''')
        return cursor.fetchall()
     