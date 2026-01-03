from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QLayout, QFormLayout, QVBoxLayout
from servicios.vehiculo_servicios import listaVehiculosActivos
from ui.base_window import BaseWindow
from PyQt5.QtWidgets import QListWidget

class ListaActivosWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vehículos Activos")

        layout = QVBoxLayout()
        layout.setSpacing(12)

        titulo = QLabel("📋 Vehículos Activos")
        titulo.setObjectName("titulo")

        btn = QPushButton("Consultar")
        btn.clicked.connect(self.consultar)

        self.resultado = QListWidget()

        layout.addWidget(titulo)
        layout.addWidget(btn)
        layout.addWidget(self.resultado)

        self.setLayout(layout)
    
    def consultar(self):
        try:
            lista = listaVehiculosActivos()
            etiquetas = ["Placa", "Marca", "Referencia", "Modelo", "Color"]
            
            self.resultado.clear()
            
            for vehiculo in lista:
                for etiqueta, valor in zip(etiquetas, vehiculo):
                    self.resultado.addItem(f"{etiqueta}: {valor}")
                
            self.resultado.addItem("🚗 VEHÍCULO")
            self.resultado.addItem("-------------------------")

                
        except Exception as e:
            self.mostrar_error(str(e))