from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.base_window import BaseWindow
from servicios.vehiculo_servicios import registrarVehiculo


class RegistrarVehiculoWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Vehículo")

        layout = QFormLayout()
        layout.setSpacing(12)

        titulo = QLabel("➕ Registrar Nuevo Vehículo")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)

        self.campos = {}
        for campo in [
            "placa", "marca", "referencia", "modelo",
            "numero_chasis", "numero_motor", "color",
            "concesionario", "fecha_compra_vehiculo",
            "tiempo_garantia", "fecha_compra_poliza_seguro",
            "proveedor_poliza_seguro", "fecha_compra_segObligatorio",
            "proveedor_segObligatorio", "activo"
        ]:
            self.campos[campo] = QLineEdit()
            layout.addRow(campo.replace("_", " ").title(), self.campos[campo])

        btn = QPushButton("💾 Guardar Vehículo")
        btn.clicked.connect(self.guardar)
        layout.addRow(btn)

        self.setLayout(layout)


    def guardar(self):
        try:
            datos = {k: v.text() for k, v in self.campos.items()}
            registrarVehiculo(datos)
            self.mostrar_ok("Vehículo registrado correctamente")
            self.close()
        except Exception as e:
            self.mostrar_error(str(e))
