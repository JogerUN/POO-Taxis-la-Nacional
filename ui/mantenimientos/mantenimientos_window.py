from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.mantenimientos.registrar_mantenimiento import RegistrarMantenimientoWindow
from ui.mantenimientos.consultar_mantenimiento import ConsultarMantenimientoWindow
from ui.mantenimientos.actualizar_mantenimiento import ActualizarMantenimientoWindow
from ui.mantenimientos.borrar_mantenimiento import BorrarMantenimientoWindow
from ui.base_window import BaseWindow

class MantenimientosWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo Mantenimientos")
        self.setFixedSize(840, 760)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(80, 60, 80, 60)
        
        titulo = QLabel("🛠️ Módulo Mantenimientos")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)

        layout.addWidget(titulo)
        
        botones = [
            ("➕ Registrar Mantenimiento", self.registrar),
            ("🔍 Consultar Mantenimiento", self.consultar),
            ("♻️ Actualizar Mantenimiento", self.actualizar),
            ("🗑️ Borrar Mantenimiento" , self.borrar),
            ("⬅️ Volver", self.close)
        ]        
        
        for texto, accion in botones:
            btn = QPushButton(texto)
            btn.clicked.connect(accion)
            layout.addWidget(btn)

        self.setLayout(layout)

    def registrar(self):
        self.r = RegistrarMantenimientoWindow()
        self.r.show()
        
    def consultar(self):
        self.r = ConsultarMantenimientoWindow()
        self.r.show()
        
    def actualizar(self):
        self.r = ActualizarMantenimientoWindow()
        self.r.show()   
        
    def borrar(self):
        self.r = BorrarMantenimientoWindow()
        self.r.show()
        
        
