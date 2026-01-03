from PyQt5.QtWidgets import QFormLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from ui.base_window import BaseWindow

class ActualizarConductorWindow(BaseWindow):
    
    def __Init__(self):
        super().__init__()
        self.setWindowTitle("Actualizar Conductores")
        
        layout = QFormLayout()
        layout.setSpacing(14)
        
        titulo = QLabel("Actualizar Conductores")
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
        
        actualizar_button = QPushButton("Actualizar")
        actualizar_button.setObjectName("actualizar")
        layout.addRow(actualizar_button)
        
        self.setLayout(layout)
        pass