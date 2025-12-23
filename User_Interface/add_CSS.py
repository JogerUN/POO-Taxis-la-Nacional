import sys # System-specific parameters and funtions
 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLineEdit, QPushButton)
from PyQt5.QtWidgets import QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() #Calls the Parenth constructor
        self.button1 = QPushButton("Button 1", self)
        self.button2 = QPushButton("Button 2", self)
        self.button3 = QPushButton("Button 3", self)
        self.initUI()
            
    def initUI(self): # self referend to our Window object 
        central_widget = QWidget() # Defining as a regular widget / Calling the constructor
        self.setCentralWidget(central_widget)
                
        hbox = QHBoxLayout()
        
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        
        central_widget.setLayout(hbox)
        
        self.button1.setObjectName("button1")
        self.button2.setObjectName("button2")
        self.button3.setObjectName("button3")
        
        
        
        self.setStyleSheet("""
                QPushButton{ 
                    font-size: 40px;
                    font-family: Arial;
                    padding: 15px 75px;
                    margin: 25px;
                    border: 3px solid;
                    border-radius: 15px; 
                }
                QPushButton#button1{
                    background-color: hsl(0, 100%, 50%);
                }
                QPushButton#button2{
                    background-color: green;
                }
                QPushButton#button3{
                    background-color: blue;
                }
                QPushButton#button1:hover{
                    background-color: hsl(0, 100%, 70%);
                }
                QPushButton#button2:hover{
                    background-color: hsl(120, 100%, 70%);
                }
                QPushButton#button3:hover{
                    background-color: hsl(200, 100%, 70%);
                }          
        """)
        
def main( ):
    app = QApplication(sys.argv) # Create an instance of QApplication
    window = MainWindow()
    window.show() # Show the window
    sys.exit(app.exec_())
    
    
if __name__ == '__main__': #
    main()