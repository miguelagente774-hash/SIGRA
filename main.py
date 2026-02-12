# integrantes del grupo
# Miguel Lagente
# Carlos Campos
# Ezequiel Rojas
# archivo .py usado como punto de entrada se comenzara a trabajar con el patron de arcquictura mvc
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt
from controller.Controller_login import controlador_login
from controller.Controller_main import Controlador_principal
import sys

class App(QMainWindow):
    login_exitoso = pyqtSignal()
    def __init__(self):
        super().__init__()
        # Propiedades de la ventana
        self.setWindowTitle("Sistema Integral de Gestión de Reportes de Actividades")
        self.setWindowIcon(QIcon("img/icono.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Instanciar el Controlador del Login
        self.mostrar_login()
    
    def mostrar_login(self):
        # ==Muestra el Login al iniciar el programa==
        self.controlador_login = controlador_login()

        self.controlador_login.get_widget().login_exitoso.connect(self.mostrar_principal)

        self.setCentralWidget(self.controlador_login.get_widget())

        # Establecer tamaño fijo
        self.setFixedSize(420, 600)

        # Centrar la Ventana después del Cambio de Tamaño
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def mostrar_principal(self):
        # ==Cambia del Login al Controlador Principal donde se encuentra el Programa==
        self.controlador_principal = Controlador_principal(self)

        # Añadir Widget Principal al Programa
        self.setCentralWidget(self.controlador_principal)

        # Restaurar bordes normales para la app principal
        self.setWindowFlags(Qt.Window) 
        self.setAttribute(Qt.WA_TranslucentBackground, False) # Quitar transparencia
        self.show() # Es necesario re-mostrar la ventana al cambiar los flags

        # Establecer tamaño fijo
        self.setFixedSize(1200, 800)

        # Centrar la Ventana después del Cambio de Tamaño
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    app.exec()