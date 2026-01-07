from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.base_window import BaseWindow
from servicios.conductor_servicios import registrarConductor

class RegistrarConductorWindow(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Conductor")
        
        layout = QFormLayout()
        layout.setSpacing(14)
        
        titulo = QLabel("➕ Registrar Nuevo Conductor")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)
        
        self.campos = {}
        for campo in [
            "noIdentificacion", "nombreCompleto","direccion",
            "telefono", "correoElectronico", "placaVehiculo", 
            "fechaIngreso", "fechaRetiro", "indicadorContratado",
            "turno", "valorTurno", "valorAhorro", "valorAdeuda", 
            "totalAhorradoNoDevuelto"
        ]:
            self.campos[campo] = QLineEdit()
            layout.addRow(campo.replace("_", " ").title(), self.campos[campo])
        
        btn = QPushButton("💾 Guardar Conductor")
        btn.clicked.connect(self.guardar)
        layout.addRow(btn)
        
        self.setLayout(layout)
        
    def guardar(self):
        try:
            datos = {k: v.text() for k, v in self.campos.items()}
            registrarConductor(datos)
            self.mostrar_ok("Conductor registrado correctamente")
            self.close()
        except Exception as e:
            self.mostrar_error(str(e))