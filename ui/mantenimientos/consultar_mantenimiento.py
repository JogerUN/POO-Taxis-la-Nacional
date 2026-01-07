from ui.base_window import BaseWindow
from PyQt5.QtWidgets import QLabel, QVBoxLayout,QListWidget, QPushButton, QFormLayout, QLineEdit
from servicios.mantenimiento_servicios import consultarMantenimiento


class ConsultarMantenimientoWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consultar Mantenimiento")
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        titulo = QLabel("🔍 Consulta de Mantenimiento")
        titulo.setObjectName("titulo")
        
        form = QFormLayout()
        self.num_orden = QLineEdit()
        form.addRow("Número de Orden:", self.num_orden)
        
        btn = QPushButton("Consultar")
        btn.clicked.connect(self.consultar)
        
        self.resultado = QListWidget()
        
        layout.addWidget(titulo)
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.resultado)
        
        self.setLayout(layout)
        
    def consultar(self):
        
        try:
            mantenimiento = consultarMantenimiento(self.num_orden.text())
            
            etiquetas = [
                "Número de Orden", "Nit. Proveedor", "Nombre Proveedor", "Descripción del servicio",
                "Valor facturado", "Fecha del servicio"
            ]
            
            self.resultado.clear()
            
            for etiqueta, valor in zip(etiquetas, mantenimiento.como_tupla()):
                self.resultado.addItem(f"{etiqueta}: {valor}")
                self.resultado.addItem("------------------------------")
                
        except Exception as e:
            self.mostrar_error(str(e))