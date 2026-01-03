from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.conductores.registrar_conductor import RegistrarConductorWindow
from ui.conductores.consultar_conductor import ConsultarConductorWindow
from ui.conductores.actualizar_conductor import ActualizarConductorWindow
from ui.conductores.lista_conductores_activos import ListaCondutoresActivosWindow
from ui.base_window import BaseWindow

class ConductoresWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Módulo Conductores")
        self.setFixedSize(840, 760)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(80, 60, 80, 60) 
        
        titulo = QLabel("Módulo Conductores")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(titulo)
        
        botones = [
            ("➕ Registrar Conductor", self.registrar),
            ("🔍 Consultar Conductor", self.consultar),
            ("♻️ Actualizar Conductor", self.actualizar),
            ("📋 Lista de Conductores Activos", self.lista_activos),
            ("⬅️ Volver", self.close)    
        ]
        
        for texto, action in botones:
            btn = QPushButton(texto)
            btn.clicked.connect(action)
            layout.addWidget(btn)
            
        self.setLayout(layout)

    def registrar(self):
        self.r = RegistrarConductorWindow
        self.r.show()

    def consultar(self):
        self.r = ConsultarConductorWindow
        self.r.show()
    
    def actualizar(self):
        self.r = ActualizarConductorWindow
        self.r.show()
        
    def lista_activos(self):
        self.r = ListaCondutoresActivosWindow
        self.r.show()