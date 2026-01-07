from PyQt5.QtWidgets import QFormLayout, QPushButton, QLabel, QLineEdit
from servicios.conductor_servicios import actualizarConductor
from ui.base_window import BaseWindow

class ActualizarConductorWindow(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actualizar Conductores")
        
        layout = QFormLayout()
        layout.setSpacing(14)
        
        titulo = QLabel("♻️ Actualizar Conductores")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)
        
        self.cedula = QLineEdit()
        layout.addRow("Cedula:", self.cedula)
              
        self.datos = {}
        for dato in [
            "nombreCompleto","direccion",
            "telefono", "correoElectronico", "placaVehiculo", 
            "fechaIngreso", "fechaRetiro", "indicadorContratado",
            "turno", "valorTurno", "valorAhorro", "valorAdeuda", 
            "totalAhorradoNoDevuelto"
        ]:
            self.datos[dato] = QLineEdit()
            layout.addRow(dato.replace("_", " ").title(), self.datos[dato])
            
        
        btn = QPushButton("Actualizar")
        btn.setObjectName("actualizar")
        btn.clicked.connect(self.actualizar)
        layout.addRow(btn)
        
        self.setLayout(layout)
        
        
    def actualizar(self):
        try:
            cedula = self.cedula.text().strip()
            if not cedula:
                raise ValueError("Debe ingresar la cédula")

            datos = {}
            for campo, input_ in self.datos.items():
                valor = input_.text().strip()
                if valor:
                    datos[campo] = valor   # ✅ solo valores reales

            actualizarConductor(cedula, datos)
            self.mostrar_ok("Conductor actualizado correctamente")
            self.close()

        except Exception as e:
            self.mostrar_error(str(e))
