from PyQt5.QtWidgets import QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from ui.base_window import BaseWindow

class ListaCondutoresActivosWindow(BaseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Conductores Activos")
        
        pass