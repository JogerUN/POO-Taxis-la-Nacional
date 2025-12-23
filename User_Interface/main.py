import sys  # System-specific parameters and functions

# ============================ PyQt5 Imports ============================
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QCheckBox, QRadioButton, QButtonGroup
)

from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt  # Used for alignment flags


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Calls the Parent constructor (QMainWindow)

        # ===================== Window Base Configuration =====================
        self.setWindowTitle("SISTEMA DE GESTIÓN - TAXIS LA NACIONAL")
        self.setGeometry(500, 150, 1000, 800)  # Set the window size and position
        self.setWindowIcon(QIcon("User_Interface/images/UNAL.png"))

        # ===================== Widgets Declaration =====================
        # Declaring widgets here makes them accessible in all methods
        self.button = QPushButton("Click ME!", self)
        self.label = QLabel("Hello", self)
        self.checkbox = QCheckBox("Do you like food?", self)

        # ======================================= Radio Buttons ================================================
        self.radio1 = QRadioButton("Visa", self)
        self.radio2 = QRadioButton("Mastercard", self)
        self.radio3 = QRadioButton("Gift Card", self)
        self.radio4 = QRadioButton("In-Store", self)
        self.radio5 = QRadioButton("Online", self)

        self.button_group1 = QButtonGroup(self)
        self.button_group2 = QButtonGroup(self)

        # ===================== UI Construction =====================
        self.build_central_widget()
        self.build_header()
        self.build_image()
        self.build_checkbox()
        self.initUI()  # Final UI setup (signals, positions, styles)

    # '''Everything realted with the User Interface shoud be in this function, clean code'''
    def build_central_widget(self):
        """
        Builds the central widget and grid layout.
        This is the main container for layout-based widgets.
        """

        central_widget = QWidget()  # Defining as a regular widget / Calling the constructor
        self.setCentralWidget(central_widget)

        # ===================== Grid Labels =====================
        label1 = QLabel("#1")
        label2 = QLabel("#2")
        label3 = QLabel("#3")
        label4 = QLabel("#4")
        label5 = QLabel("#5")
        label6 = QLabel("#6")

        label1.setStyleSheet("background-color: green;")
        label2.setStyleSheet("background-color: green;")
        label3.setStyleSheet("background-color: white;")
        label4.setStyleSheet("background-color: white;")
        label5.setStyleSheet("background-color: green;")
        label6.setStyleSheet("background-color: green;")

        grid = QGridLayout()

        '''vbox = QVBoxLayout()'''  # Calling the constructor (example)
        '''hbox = QHBoxLayout()'''  # Horizontal layout example
        '''grid = QGridLayout() We've got to specify where [row][column]'''

        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 0, 1)
        grid.addWidget(label3, 1, 0)
        grid.addWidget(label4, 1, 1)
        grid.addWidget(label5, 2, 1)
        grid.addWidget(label6, 2, 0)

        central_widget.setLayout(grid)
        # '''Setting the Layout within the central_widget'''

    def build_header(self):
        """
        Creates the main title label (header).
        """

        label = QLabel("Bienvenido al Sistema de Gestión de Taxis La Nacional", self)
        label.setFont(QFont("TimeNewRoman", 25))
        label.setGeometry(0, 0, 1000, 100)  # (x, y, width, height)

        label.setStyleSheet(
            "color: #40e32d;"
            "background-color: #090a09;"
            "font-weight: bold;"
            "font-style: italic;"
            "text-decoration: underline;"
        )

        # label.setAlignment(Qt.AlignTop)        # Vertically Top
        # label.setAlignment(Qt.AlignBottom)     # Vertically Bottom
        # label.setAlignment(Qt.AlignVCenter)    # Vertically Center
        # label.setAlignment(Qt.AlignRight)      # Horizontally Right
        # label.setAlignment(Qt.AlignLeft)       # Horizontally Left
        label.setAlignment(Qt.AlignCenter)       # Center Center

    def build_image(self):
        """
        Loads and centers an image inside the window.
        """

        pixmap = QPixmap("User_Interface/images/UNAL.png")  # The Object
        image = QLabel(self)

        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)
        image.setScaledContents(True)

        image.setGeometry(
            (self.width() - 600) // 2,
            200,
            600,
            400
        )  # How to move the image to the middle of the window

    # ========================================= Checkbox =============================================
    def build_checkbox(self):
        """
        Configures the checkbox and connects its signal.
        """

        self.checkbox.setGeometry(20, 120, 400, 50)
        self.checkbox.setStyleSheet(
            "font-size: 30px;"
            "font-family: Arial;"
        )

        # self.checkbox.setChecked(False)  # Just if we want the checkbox already checked
        self.checkbox.stateChanged.connect(self.checkbox_changed)

    def checkbox_changed(self, state):
        """
        Triggered when the checkbox state changes.
        """

        if state == Qt.Checked:
            print("You like food")
        else:
            print("You DON'T like food")

    def initUI(self):
        """
        Final UI setup:
        - Radio buttons positioning
        - Button groups
        - Signals & slots
        """

        # ===================== Radio Buttons Geometry =====================
        self.radio1.setGeometry(0, 200, 300, 50)
        self.radio2.setGeometry(0, 250, 300, 50)
        self.radio3.setGeometry(0, 300, 300, 50)
        self.radio4.setGeometry(0, 350, 300, 50)
        self.radio5.setGeometry(0, 400, 300, 50)

        self.setStyleSheet(
            "QRadioButton {"
            "font-size: 40px;"
            "font-family: Arial;"
            "padding: 10px;"
            "}"
        )

        # Grouping Options Buttons by Groups
        self.button_group1.addButton(self.radio1)
        self.button_group1.addButton(self.radio2)
        self.button_group1.addButton(self.radio3)

        self.button_group2.addButton(self.radio4)
        self.button_group2.addButton(self.radio5)

        # Connecting radio buttons to the same slot
        for radio in [self.radio1, self.radio2, self.radio3, self.radio4, self.radio5]:
            radio.toggled.connect(self.radio_button_changed)

        # ===================== Button =====================
        self.button.setGeometry(350, 600, 300, 100)
        self.button.setStyleSheet("font-size: 50px;")
        self.button.clicked.connect(self.on_click)  # button + signal + connected + slot

    def radio_button_changed(self):
        """
        Triggered when any radio button changes state.
        """

        radio_button = self.sender()
        if radio_button.isChecked():
            print(f"{radio_button.text()} is selected")

    def on_click(self):
        """
        Triggered when the button is clicked.
        """

        self.label.setText("GoodBye")
        # self.button.setDisabled(True)  # Allowing just one click


def main():
    app = QApplication(sys.argv)  # Create an instance of QApplication
    window = MainWindow()
    window.show()  # Show the window
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
