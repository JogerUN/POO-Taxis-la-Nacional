from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.base_window import BaseWindow
from servicios.vehiculo_servicios import registrarVehiculo


class RegistrarVehiculoWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("➕ Registrar Vehículo")
        self.setStyleSheet(self.estilos())

        layout = QFormLayout()
        layout.setSpacing(12)

        titulo = QLabel("Registro de Vehículo")
        titulo.setAlignment(Qt.AlignCenter)
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
            self.campos[campo].setPlaceholderText(campo.replace("_", " ").title())
            layout.addRow(campo.replace("_", " ").title(), self.campos[campo])

        btn = QPushButton("💾 Guardar Vehículo")
        btn.clicked.connect(self.guardar)
        layout.addRow(btn)

        self.setLayout(layout)

    def estilos(self):
        return """
        QWidget { background-color: #1e1e2f; color: white; }
        QLabel#titulo { font-size: 18px; font-weight: bold; }
        QLineEdit {
            padding: 8px;
            border-radius: 6px;
            background-color: #2b2b3c;
            color: white;
        }
        QPushButton {
            background-color: #2d89ef;
            padding: 10px;
            border-radius: 8px;
        }
        """

    def guardar(self):
        try:
            datos = {k: v.text() for k, v in self.campos.items()}
            registrarVehiculo(datos)
            self.mostrar_ok("Vehículo registrado correctamente")
            self.close()
        except Exception as e:
            self.mostrar_error(str(e))
