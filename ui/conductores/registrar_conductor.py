from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.base_window import BaseWindow

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
            self.compos[campo] = QLineEdit()
            layout.addRow(campo.replace("_", " ").title(), self.compos[campo])
            pass