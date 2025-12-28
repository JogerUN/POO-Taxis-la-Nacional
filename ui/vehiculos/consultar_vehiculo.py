from PyQt5.QtWidgets import QLabel, QVBoxLayout,QListWidget, QPushButton, QFormLayout, QLineEdit
from servicios.vehiculo_servicios import consultarVehiculo
from ui.base_window import BaseWindow

class ConsultarVehiculoWindow(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consultar Vehículo")

        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.placa = QLineEdit()
        self.resultado = QListWidget()
        self.resultado.setStyleSheet("""
        QListWidget {
            background-color: #2b2b3c;
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        """)

        
        form.addRow(QLabel("Placa:"), self.placa)
        
        btn = QPushButton("Consultar")
        btn.clicked.connect(self.consultar)
        
        layout.addLayout(form)
        layout.addWidget(btn)
        layout.addWidget(self.resultado) 
        
        self.setLayout(layout)       
        
    def consultar(self):
        try:
            vehiculo = consultarVehiculo(self.placa.text())
            etiquetas = [
                "Placa", "Marca", "Referencia", "Modelo", "Número chasis",
                "Número motor", "Color", "Concesionario", "Fecha compra",
                "Garantía (meses)", "Fecha póliza", "Proveedor póliza",
                "Fecha SOAT", "Proveedor SOAT", "Activo"
            ]
            
            self.resultado.clear()
            
            for etiqueta, valor in zip(etiquetas, vehiculo.como_tupla()):
                self.resultado.addItem(f"{etiqueta}: {valor}")
                self.resultado.addItem("------------------------------")
                
        except Exception as e:
            self.mostrar_error(str(e))