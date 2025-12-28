from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.vehiculos.registrar_vehiculo import RegistrarVehiculoWindow
from ui.vehiculos.consultar_vehiculo import ConsultarVehiculoWindow
from ui.vehiculos.actualizar_vehiculo import ActualizarEstadoVehiculoWindow
from ui.vehiculos.lista_activos import ListaActivosWindow
from ui.vehiculos.actualizar_seguros import ActualizarPolizaVehiculoWindow


class VehiculosWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 Módulo Vehículos")
        self.setFixedSize(420, 420)
        self.setStyleSheet(self.estilos())

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        titulo = QLabel("Gestión de Vehículos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo")

        btn_registrar = QPushButton("➕ Registrar Vehículo")
        btn_consultar = QPushButton("🔍 Consultar Vehículo")
        btn_actualizar = QPushButton("♻️ Actualizar Estado")
        btn_actualizar_seguros = QPushButton("🛡️ Actualizar Pólizas")
        btn_lista_activos = QPushButton("📋 Vehículos Activos")
        btn_salir = QPushButton("⬅️ Volver")

        btn_registrar.clicked.connect(self.registrar)
        btn_consultar.clicked.connect(self.consultar)
        btn_actualizar.clicked.connect(self.actualizar)
        btn_actualizar_seguros.clicked.connect(self.actualizar_seguros)
        btn_lista_activos.clicked.connect(self.lista_activos)
        btn_salir.clicked.connect(self.close)

        layout.addWidget(titulo)
        layout.addSpacing(20)

        for btn in [
            btn_registrar, btn_consultar, btn_actualizar,
            btn_actualizar_seguros, btn_lista_activos
        ]:
            layout.addWidget(btn)

        layout.addSpacing(20)
        layout.addWidget(btn_salir)

        self.setLayout(layout)

    def estilos(self):
        return """
        QWidget {
            background-color: #1e1e2f;
            font-family: Arial;
        }

        QLabel#titulo {
            font-size: 22px;
            font-weight: bold;
            color: white;
        }

        QPushButton {
            background-color: #2d89ef;
            color: white;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #1b5fa7;
        }
        """

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
