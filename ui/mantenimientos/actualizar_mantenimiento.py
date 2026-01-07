from ui.base_window import BaseWindow
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QFormLayout, QLineEdit
from servicios.mantenimiento_servicios import actualizarMantenimiento

class ActualizarMantenimientoWindow(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actualizar Mantenimiento")
        
        layout =QFormLayout()
        layout.setSpacing(12)
        
        titulo = QLabel("♻️ Actualizar Mantenimiento")
        titulo.setObjectName("titulo")
        layout.addRow(titulo)
        
        self.num_order = QLineEdit()
        layout.addRow("Número de Orden:", self.num_order)
        
        # ⚠️ keys técnicas (NO labels)        
        self.datos = {}
        for dato in [
            "placaVehiculo",
            "nitProveedor",
            "nombreProveedor",
            "descripcionServicio",
            "valorFacturado"
            "fechaServicio"
        ]:
            self.datos[dato] = QLineEdit()
            layout.addRow(dato.replace("_", " "), self.datos[dato])
    
    
        btn = QPushButton("Actualizar")
        btn.setObjectName("actualizar")
        btn.clicked.connect(self.actualizar)
        layout.addRow(btn)
                
        self.setLayout(layout)
    
    def actualizar(self):
        try:
            num_order = self.num_order.text().strip()
            if not num_order:
                raise ValueError("El número de orden es obligatorio")
            
            datos = {}
            
            for campo, input in self.datos.items():
                valor = input.text().strip()
                if valor:
                    if campo in ["valorFacturado"]:
                        valor = float(valor)
                    datos[campo] = valor   # ✅ solo valores reales      
            
            actualizarMantenimiento(num_order, datos)
            self.mostrar_ok("Mantenimiento actualizado correctamente")
            self.close()
            
        except Exception as e:
            self.mostrar_error(str(e))