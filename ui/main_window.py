from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from ui.vehiculos.vehiculos_window import VehiculosWindow
from ui.conductores.conductores_window import ConductoresWindow
from ui.mantenimientos.mantenimientos_window import MantenimientosWindow


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚕 Taxis La Nacional")
        self.setFixedSize(420, 380)   # Tamaño fijo (más elegante)
        self.setStyleSheet(self.estilos())

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        # 🟡 TÍTULO
        titulo = QLabel("Taxis La Nacional")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Sistema de Gestión")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setObjectName("subtitulo")

        # 🟡 BOTONES
        btn_vehiculos = QPushButton("🚗 Gestión de Vehículos")
        btn_conductores = QPushButton("👨‍✈️ Gestión de Conductores")
        btn_mantenimientos = QPushButton("🛠️ Mantenimientos")
        btn_salir = QPushButton("❌ Salir")

        btn_vehiculos.clicked.connect(self.abrir_vehiculos)
        btn_conductores.clicked.connect(self.abrir_conductores)
        btn_mantenimientos.clicked.connect(self.abrir_mantenimientos)
        btn_salir.clicked.connect(self.close)

        # 🟡 ESPACIADOR
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 🟡 ARMADO DEL LAYOUT
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addSpacing(20)

        layout.addWidget(btn_vehiculos)
        layout.addWidget(btn_conductores)
        layout.addWidget(btn_mantenimientos)

        layout.addItem(spacer)
        layout.addWidget(btn_salir)

        self.setLayout(layout)

    # ============================
    # MÉTODOS DE NAVEGACIÓN
    # ============================
    def abrir_vehiculos(self):
        self.v = VehiculosWindow()
        self.v.show()

    def abrir_conductores(self):
        self.c = ConductoresWindow()
        self.c.show()

    def abrir_mantenimientos(self):
        self.m = MantenimientosWindow()
        self.m.show()

    # ============================
    # ESTILOS CSS (QSS)
    # ============================
    def estilos(self):
        return """
        QWidget {
            background-color: #1e1e2f;
            font-family: Arial;
        }

        QLabel#titulo {
            font-size: 26px;
            font-weight: bold;
            color: #ffffff;
        }

        QLabel#subtitulo {
            font-size: 14px;
            color: #cfcfcf;
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

        QPushButton:pressed {
            background-color: #133d6b;
        }
        """
