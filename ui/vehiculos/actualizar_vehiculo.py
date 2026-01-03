from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QFormLayout, QLineEdit
from servicios.vehiculo_servicios import consultarVehiculo, actualizarEstado
from ui.base_window import BaseWindow

class ActualizarEstadoVehiculoWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actualizar Estado")

        layout = QFormLayout()
        layout.setSpacing(12)

        titulo = QLabel("♻️ Actualizar Estado del Vehículo")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)

        self.placa = QLineEdit()
        self.estado = QLineEdit()

        layout.addRow("Placa:", self.placa)
        layout.addRow("Estado (1=Activo / 2=Inactivo):", self.estado)

        btn = QPushButton("Actualizar Estado")
        btn.clicked.connect(self.actualizar)
        layout.addRow(btn)

        self.setLayout(layout)
        
    def actualizar(self):
        try:
            placa = self.placa.text()
            nuevo_estado = int(self.estado.text())
            actualizarEstado(placa, nuevo_estado)
            self.mostrar_ok("Estado del vehículo actualizado correctamente")
            self.close()
        except Exception as e:
            self.mostrar_error(str(e))