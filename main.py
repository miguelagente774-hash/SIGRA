# integrantes del grupo
# Miguel Lagente
# Carlos Campos
# Ezequiel Rojas
# archivo .py usado como punto de entrada se comenzara a trabajar con el patron de arcquictura mvc
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QIcon
from controller.Controller_main import Controlador_principal
from models.Modelo_login import Model_Login
import sys

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        # == Propiedades de la Ventana==
        self.setWindowTitle("Sistema Integral de Gestión de Reportes de Actividades")
        self.setWindowIcon(QIcon("img/ico/icon.ico"))
        self.setCentralWidget(Controlador_principal(self))

        modelo_login = Model_Login()
        modelo_login.inicializar_configuracion()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    app.exec()