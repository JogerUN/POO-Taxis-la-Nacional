from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
class MantenimientosWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo Vehículos")

        layout = QVBoxLayout()

        btn_registrar = QPushButton("Registrar Vehículo")
        btn_consultar = QPushButton("Consultar Vehículo")
        btn_actualizar = QPushButton("Actualizar Vehículo")
        btn_salir = QPushButton("Volver")

        btn_registrar.clicked.connect(self.registrar)

        layout.addWidget(btn_registrar)
        layout.addWidget(btn_consultar)
        layout.addWidget(btn_actualizar)
        layout.addWidget(btn_salir)

        self.setLayout(layout)

    def registrar(self):
        self.r = RegistrarVehiculoWindow()
        self.r.show()
