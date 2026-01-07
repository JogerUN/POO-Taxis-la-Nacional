from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QListWidget
from servicios.conductor_servicios import listaConductoresActivos
from ui.base_window import BaseWindow


class ListaConductoresActivosWindow(BaseWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Conductores Activos")

        layout = QVBoxLayout()
        layout.setSpacing(12)

        titulo = QLabel("📋 Conductores Activos")
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
            lista = listaConductoresActivos()

            etiquetas = ["Cédula", "Nombre", "Placa"]

            self.resultado.clear()

            for conductor in lista:
                self.resultado.addItem("🚗 CONDUCTOR")
                self.resultado.addItem("-------------------------")

                for etiqueta, valor in zip(etiquetas, conductor):
                    self.resultado.addItem(f"{etiqueta}: {valor}")

        except Exception as e:
            self.mostrar_error(str(e))
