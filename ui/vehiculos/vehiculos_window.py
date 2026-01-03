from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.vehiculos.registrar_vehiculo import RegistrarVehiculoWindow 
from ui.vehiculos.consultar_vehiculo import ConsultarVehiculoWindow 
from ui.vehiculos.actualizar_vehiculo import ActualizarEstadoVehiculoWindow 
from ui.vehiculos.lista_activos import ListaActivosWindow 
from ui.vehiculos.actualizar_seguros import ActualizarPolizaVehiculoWindow
from ui.base_window import BaseWindow

class VehiculosWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo Vehículos")
        self.setFixedSize(840, 760)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(80, 60, 80, 60)

        titulo = QLabel("🚗 Módulo Vehículos")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        layout.addWidget(titulo)

        botones = [
            ("➕ Registrar Vehículo", self.registrar),
            ("🔍 Consultar Vehículo", self.consultar),
            ("♻️ Actualizar Estado", self.actualizar),
            ("🛡️ Actualizar Pólizas", self.actualizar_seguros),
            ("📋 Vehículos Activos", self.lista_activos),
            ("⬅️ Volver", self.close)
        ]

        for texto, accion in botones:
            btn = QPushButton(texto)
            btn.clicked.connect(accion)
            layout.addWidget(btn)

        self.setLayout(layout)

    def registrar(self):
        self.r = RegistrarVehiculoWindow()
        self.r.show()

    def consultar(self):
        self.r = ConsultarVehiculoWindow()
        self.r.show()

    def actualizar(self):
        self.r = ActualizarEstadoVehiculoWindow()
        self.r.show()

    def actualizar_seguros(self):
        self.r = ActualizarPolizaVehiculoWindow()
        self.r.show()

    def lista_activos(self):
        self.r = ListaActivosWindow()
        self.r.show()
