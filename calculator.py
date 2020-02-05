import sys, os, re
from PyQt5.QtWidgets import *   
from PyQt5.QtGui import QKeySequence, QIcon, QFont
from PyQt5 import QtCore

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'icon.png'))
        self.setWindowTitle("Calculator")

        self.main = main_widget()
        self.setCentralWidget(self.main) 
        self.main_menu = self.menuBar()

        self.CE_button = self.main_menu.addAction("CE")
        self.CE_button.triggered.connect(self.main.on_CE_pressed)
        self.CE_button.setShortcut("Backspace")

        self.C_button = self.main_menu.addAction("C")
        self.C_button.triggered.connect(self.main.on_C_pressed)
        
        
class main_widget(QWidget):
    def __init__(self):
        super().__init__()

        self.repeat_operator_list = ["+", "/", "*"]
        self.operator_list = ["+", "/", "*","-"]
        self.number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.button_info_list = [ [0,0,0] , [1,1,0] , [2,2,0] , [3,0,1] , [4,1,1] , [5,2,1] , [6,0,2] , [7,1,2], [8,2,2] , [9,0,3] , ["+",3,0], ["-",3,1] , ["/",3,2] , ["*",3,3] , ["(",1,3] , [")",2,3] ] #button text, x pos, y pos
        self.button_dict = {}

        self.to_calculate = ""

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # creates all number + operator buttons
        for item in self.button_info_list:
            self.number_button = QPushButton(str(item[0]))
            self.number_button.setFixedSize(50,50)
            self.number_button.setShortcut(f"{item[0]}")
            self.number_button.clicked.connect(self.on_num_operator_clicked)
            grid_layout.addWidget(self.number_button, item[2],item[1]) 
            
            self.button_dict[str(item[0])] = self.number_button
            del self.number_button
        
        # enter button
        self.enter_button = QPushButton("=")
        self.enter_button.setFixedSize(50,50)
        grid_layout.addWidget(self.enter_button,4,3)
        self.enter_button.clicked.connect(self.on_enter)
        self.enter_button.setShortcut("=")
        self.enter_button.setShortcut("Return")

        #output label
        font = QFont("Arial", 12, QFont.Bold)
        self.output_label = QLabel("")
        self.output_label.setFont(font)
        grid_layout.addWidget(self.output_label,4,0,4,3)
        
    def on_enter(self):
        try:
            self.multiply_unprefixed_brackets()
            self.multiply_unsuffixed_brackets()
            self.output_label.setText(str(eval(self.to_calculate)))
            self.to_calculate = str(eval(self.to_calculate))
        except:
            self.output_label.setText("ERROR.")

    def on_num_operator_clicked(self):
        self.to_calculate += self.sender().text()

        self.check_prev_char()
        self.check_first_char()

        self.output_label.setText(str(self.to_calculate))
        self.previous_input = self.sender().text()
        
    #removes most recent input
    def on_CE_pressed(self):
        self.to_calculate = self.to_calculate[:-1]
        self.output_label.setText(str(self.to_calculate))

    #clears input
    def on_C_pressed(self):
        self.to_calculate = ""
        self.output_label.setText(str(self.to_calculate))

    # used to stop user from entering operator more than once in succession, excluding "-"    
    def check_prev_char(self):
        if len(self.to_calculate) > 1:
            self.to_add = self.to_calculate[-1:]
            if self.to_add in self.repeat_operator_list and self.previous_input in self.repeat_operator_list:
                self.to_calculate = self.to_calculate[:-1]

    # used to make sure the first input isnt an operator, excluding "-"
    def check_first_char(self):
        if self.to_calculate[0] in self.repeat_operator_list and len(self.to_calculate) <= 1:
            self.to_calculate = ""

    def multiply_unprefixed_brackets(self):
        self.indexes = [i for i, letter in enumerate(self.to_calculate) if letter == "("]
        if len(self.to_calculate) > 1:
            for self.index in self.indexes:
                self.temp_array = list(self.to_calculate)
                self.temp_array.insert(self.index, "*")
                self.to_calculate = ""
                for char in self.temp_array:
                    self.to_calculate += char

    def multiply_unsuffixed_brackets(self):
        self.indexes = [i for i, letter in enumerate(self.to_calculate) if letter == ")"]
        if len(self.to_calculate) > 1:
            for self.index in self.indexes:
                self.temp_array = list(self.to_calculate)
                self.temp_array.insert(self.index+1, "*")
                self.to_calculate = ""
                for char in self.temp_array:
                    self.to_calculate += char

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = main_window()
    window.resize(225,0)
    window.show()
    sys.exit(app.exec_())
