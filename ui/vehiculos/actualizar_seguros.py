from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QFormLayout
from servicios.vehiculo_servicios import actualizarPolizaVehiculo
from ui.base_window import BaseWindow

class ActualizarPolizaVehiculoWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actualizar Pólizas")

        layout = QFormLayout()
        layout.setSpacing(12)

        titulo = QLabel("🛡️ Actualizar Pólizas del Vehículo")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)

        self.placa = QLineEdit()
        layout.addRow("Placa:", self.placa)

        self.campos = {}
        for campo, label in {
            "fecha_compra_poliza_seguro": "Fecha Póliza (DD/MM/AAAA)",
            "proveedor_poliza_seguro": "Proveedor Póliza",
            "fecha_compra_segObligatorio": "Fecha SOAT (DD/MM/AAAA)",
            "proveedor_segObligatorio": "Proveedor SOAT"
        }.items():
            self.campos[campo] = QLineEdit()
            layout.addRow(label, self.campos[campo])

        btn = QPushButton("Actualizar Pólizas")
        btn.clicked.connect(self.actualizar)
        layout.addRow(btn)

        self.setLayout(layout)

    def actualizar(self):
        try:
            datos = {k: v.text() for k, v in self.campos.items()}
            actualizarPolizaVehiculo(self.placa.text(), datos)
            self.mostrar_ok("Pólizas actualizadas correctamente")
            self.close()
        except Exception as e:
            self.mostrar_error(str(e))
