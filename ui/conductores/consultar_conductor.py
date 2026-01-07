from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout, QListWidget
from servicios.conductor_servicios  import consultarConductor
from ui.base_window import BaseWindow

class ConsultarConductorWindow(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Conductor")
        
        layout = QVBoxLayout()
        layout.setSpacing(12)

        titulo =QLabel("🔍 Consulta de Conductor")
        titulo.setObjectName("titulo")
        
        form = QFormLayout()
        self.cedula = QLineEdit()
        form.addRow("Cédula:", self.cedula)
                
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
            conductor = consultarConductor(self.cedula.text())
            etiquetas =[
                "Cedula", "Nombre Completo", "Dirreccion" , "Telefono",
                "Correo Electronico", "Fecha Ingreso", "Fecha Retiro",
                "Estado del conductor", "Turno", "Valor Turno", "Valor AHorro", 
                "Valor deuda", "Valor ahorra"  , "Total Ahorrado No Devuelto" 
            ]
            self.resultado.clear()
                
            for etiqueta, valor in zip(etiquetas, conductor.como_tupla()):
                self.resultado.addItem(f"{etiqueta}: {valor}")
                self.resultado.addItem("------------------------------")
                
        except Exception as e:
            self.mostrar_error(str(e))