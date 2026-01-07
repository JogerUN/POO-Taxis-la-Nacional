from ui.base_window import BaseWindow
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QFormLayout, QLineEdit
from servicios.mantenimiento_servicios import borrarMantenimiento

class BorrarMantenimientoWindow(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Borrar Mantenimiento")
        
        layout = QFormLayout()
        layout.setSpacing(12)
        
        titulo = QLabel("🗑️ Borrar Mantenimiento")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)
        
        self.num_order = QLineEdit()
        layout.addRow("Número de Orden:", self.num_order)
        
        btn =  QPushButton("Borrar")
        btn.setObjectName("btn")
        btn.clicked.connect(self.borrar)
        
        layout.addRow(btn)
        
        self.setLayout(layout)
        
    def borrar(self):
        try:
            num_order = self.num_order.text().strip()
            borrarMantenimiento(num_order)
            self.mostrar_ok("Mantenimiento borrado correctamente")
            self.close()
        except Exception as e:
            self.mostrar_error(str(e))