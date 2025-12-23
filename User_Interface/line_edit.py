import sys # System-specific parameters and funtions
 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() #Calls the Parenth constructor
        self.setGeometry(500, 150, 1000, 800) # Set the window size and position
        self.line_edit = QLineEdit(self)
        self.button = QPushButton("Submit", self)
        self.initUI()
        
    
    
    def initUI(self): # self referend to our Window object 
        self.line_edit.setGeometry(10, 10, 200, 50)    
        self.button.setGeometry(210, 10, 100, 50)
        self.line_edit.setStyleSheet("font-size: 25px;"
                                     "font-family: Arial")
    
        self.button.setStyleSheet("font-size: 25px;"
                                     "font-family: Arial")

        self.line_edit.setPlaceholderText("Write something M0th4r F4k*r")
        
        self.button.clicked.connect(self.submit)
   
    def submit(self):
        text = self.line_edit.text()
        
        
        print(f"You Clicked the Button \n {text}")
        
                
def main( ):
    app = QApplication(sys.argv) # Create an instance of QApplication
    window = MainWindow()
    window.show() # Show the window
    sys.exit(app.exec_())
    
    
if __name__ == '__main__': #
    main()