from ui.base_window import BaseWindow
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPushButton, QLabel
from servicios.mantenimiento_servicios import registrarMantenimiento

class RegistrarMantenimientoWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Mantenimiento")
        
        layout = QFormLayout()
        layout.setSpacing(12)
        
        titulo = QLabel("➕ Registrar Nuevo Mantenimiento")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)
        
        self.campos = {}
        for campo in {
            "numeroOrden", "placaVehiculo", "nitProveedor", "nombreProveedor", 
            "descripcionServicio", "valorFacturado", "fechaServicio"
        }:
            self.campos[campo] = QLineEdit()
            layout.addRow(f"{campo.capitalize()}: ", self.campos[campo])
            
        btn = QPushButton("💾 Guardar Mantenimiento")
        btn.clicked.connect(self.guardar)
        layout.addRow(btn)
        
        self.setLayout(layout)
        
    def guardar(self):
        try:
            datos = {k: v.text() for k, v in self.campos.items()}
            registrarMantenimiento(datos)
            self.mostrar_ok("Mantenimiento registrado correctamente")
            self.close()
        except Exception as e:
            self.mostrar_error(str(e))