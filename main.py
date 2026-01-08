#integrantes del grupo
#Miguel Lagente
#Carlos Campos
#Ezequiel Rojas
#archivo .py usado como punto de entrada se comenzara a trabajar con el patron de arcquictura mvc
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QIcon
from controller.Controller_main import Controlador_principal
import sys

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        #propiedades de la ventana
        self.setWindowTitle("Sistema Integral de Gestión de Reportes de Actividades")
        self.setWindowIcon(QIcon("img/icon.ico"))
        #seria bueno cambiarlo por un max y min weihg
        #self.resize(900, 690)
        #self.setMinimumHeight(900)
        self.setCentralWidget(Controlador_principal(self))
        #cargar aqui el controlador principal (necesario importar el modulo)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    app.exec()