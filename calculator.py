import sys, os, re
from PyQt5.QtWidgets import *   
from PyQt5.QtGui import QKeySequence, QIcon, QFont, QColor
from PyQt5 import QtCore

class button_info:
    def __init__(self,button_text,button_function,xpos,ypos):
        self.button_text = button_text
        self.button_function = button_function
        self.xpos = xpos
        self.ypos = ypos
        
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

        self.to_calculate = ""
        self.repeat_operator_list = ["+", "/", "*"]
        self.operator_list = ["+", "/", "*","-"]
        self.number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        #button text, function, x pos, y pos
        self.button_info_list = [ button_info("0","0",0,0) , button_info("1","1",1,0) , button_info("2","2",2,0) , button_info("+","+",3,0) , 
                                  button_info("3","3",0,1) , button_info("4","4",1,1) , button_info("5","5",2,1) , button_info("-","-",3,1) ,
                                  button_info("6","6",0,2) , button_info("7","7",1,2) , button_info("8","8",2,2) , button_info("/","/",3,2) ,
                                  button_info("9","9",0,3) , button_info("(","(",1,3) , button_info(")",")",2,3) , button_info("x","*",3,3) ,
                                                                                        button_info("^","**",2,4)                           ]

        self.button_dict = {} #to be populated by button objects

        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # creates all buttons in button_info_list, adds to button_dict
        for button_info_obj in self.button_info_list:
            self.number_button = QPushButton(button_info_obj.button_text)
            self.number_button.setFixedSize(50,50)
            self.number_button.setShortcut(button_info_obj.button_text)
            self.number_button.setStyleSheet("background-color: white")
            self.number_button.clicked.connect(self.on_num_operator_clicked)
            grid_layout.addWidget(self.number_button, button_info_obj.ypos, button_info_obj.xpos) 
            
            self.button_dict[button_info_obj.button_text] = self.number_button
            del self.number_button
        
        # enter button
        self.enter_button = QPushButton("=")
        self.enter_button.setFixedSize(50,50)
        self.enter_button.setShortcut("=")
        self.enter_button.setShortcut("Return")
        self.enter_button.setStyleSheet("background-color: white")
        self.enter_button.clicked.connect(self.on_enter)
        grid_layout.addWidget(self.enter_button,4,3)

        #output label
        font = QFont("Arial", 12, QFont.Bold)
        self.output_label = QLabel("")
        self.output_label.setFont(font)
        grid_layout.addWidget(self.output_label,4,0,4,2)
        
    def on_enter(self):
        try:
            self.multiply_unprefixed_brackets()
            self.multiply_unsuffixed_brackets()
            self.check_first_char()
            self.to_calculate = str(eval(self.to_calculate))
            self.output_label.setText(str(self.to_calculate))

        except Exception as e:
            print(e)
            self.output_label.setText("ERROR.")

    def on_num_operator_clicked(self):
        try: #searches for corresponding object info, and adds its function to self.to_calculate
            for self.num_operator in self.button_info_list:
                if str(self.num_operator.button_text) == str(self.sender().text()):
                    self.to_calculate += str(self.num_operator.button_function)
        except Exception as e:
            print(e)

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
        for _ in range(len(self.to_calculate)):
            if self.to_calculate[0] in self.repeat_operator_list and len(self.to_calculate) <= 1:
                self.to_calculate = self.to_calculate[1:]

    def multiply_unprefixed_brackets(self):
        self.indexes = [i for i, letter in enumerate(self.to_calculate) if letter == "("]
        try:
            self.indexes.remove(0)
        except:
            pass

        if len(self.to_calculate) > 1:
            for self.index in self.indexes:
                try:
                    if self.to_calculate[self.index-1] not in self.operator_list:
                        self.temp_array = list(self.to_calculate)
                        self.temp_array.insert(self.index, "*")
                        self.to_calculate = ""
                        for char in self.temp_array:
                            self.to_calculate += char
                except Exception as e:
                    print(e)

    def multiply_unsuffixed_brackets(self):
        self.indexes = [i for i, letter in enumerate(self.to_calculate) if letter == ")"]
        if len(self.to_calculate) > 1:
            for self.index in self.indexes:
                try:
                    if self.to_calculate[self.index+1] not in self.operator_list:
                        self.temp_array = list(self.to_calculate)
                        self.temp_array.insert(self.index+1, "*")
                        self.to_calculate = ""
                        for char in self.temp_array:
                            self.to_calculate += char
                except Exception as e:
                    print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = main_window()
    window.resize(225,0)
    window.show()
    sys.exit(app.exec_())
