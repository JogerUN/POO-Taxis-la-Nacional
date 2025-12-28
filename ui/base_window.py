from PyQt5.QtWidgets import QMessageBox, QWidget

class BaseWindow(QWidget):
    from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class BaseWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet(self.estilos())
        self.setFixedWidth(520)

    def estilos(self):
        return """
        QWidget {
            background-color: #1e1e2f;
            font-family: Arial;
            font-size: 13px;
            color: #ffffff;
        }

        QLabel {
            color: #ffffff;
        }

        QLabel#titulo {
            font-size: 20px;
            font-weight: bold;
            padding-bottom: 10px;
        }

        QLineEdit {
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #444;
            background-color: #2b2b3c;
            color: white;
        }

        QPushButton {
            background-color: #2d89ef;
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #1b5fa7;
        }

        QListWidget {
            background-color: #2b2b3c;
            border-radius: 6px;
            padding: 6px;
        }
        """

    def mostrar_ok(self, mensaje):
        QMessageBox.information(self, "Éxito", mensaje)

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)
