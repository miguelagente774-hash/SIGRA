# integrantes del grupo
# Miguel Lagente
# Carlos Campos
# Ezequiel Rojas
# archivo .py usado como punto de entrada se comenzara a trabajar con el patron de arcquictura mvc
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt
from controller.Controller_login import controlador_login, controlador_setup, controlador_recuperar
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

        self.verificar_primer_inicio()

    def verificar_primer_inicio(self):
        from models.Modelo_login import Model_Login
        modelo = Model_Login()
        # Verifica si existe la Base de Datos, la Tabla Usuario
        if modelo.verificar_usuarios_existentes():
            # Si existen usuarios (como 'admin'), ir al login
            self.mostrar_login()
        else:
            # Si no hay usuarios, es el primer inicio, ir al setup
            self.mostrar_setup()

    def mostrar_setup(self):
        # ==Muestra el Setup al Iniciar el Programa por Primera Vez==
        self.controlador_setup= controlador_setup()

        self.controlador_setup.get_widget().registro_exitoso.connect(self.mostrar_login)
        self.setCentralWidget(self.controlador_setup.get_widget())
        
        # Establecer Tamaño Fijo
        self.setFixedSize(800, 600)

        # Centrar Ventana
        self.centrar_ventana()

    
    def mostrar_login(self):
        # ==Muestra el Login al iniciar el programa==
        self.controlador_login = controlador_login()

        # Conectar Métodos al recibir la Señal
        self.controlador_login.get_widget().recuperar_login.connect(self.mostrar_recuperar)
        self.controlador_login.get_widget().login_exitoso.connect(self.mostrar_principal)

        self.setCentralWidget(self.controlador_login.get_widget())

        # Establecer Tamaño Fijo
        self.setFixedSize(420, 600)
        
        # Centrar Ventana
        self.centrar_ventana()

    def mostrar_recuperar(self):
        # == Muestra el recuperar
        self.controlador_recuperar = controlador_recuperar()
        
        self.controlador_recuperar.get_widget().recuperacion_exitoso.connect(self.mostrar_login)
        
        self.setCentralWidget(self.controlador_recuperar.get_widget())
        
        # Establecer Tamaño Fijo
        self.setFixedSize(800, 600)

        # Centrar Ventana
        self.centrar_ventana()
        
    def mostrar_principal(self):
        # ==Cambia del Login al Controlador Principal donde se encuentra el Programa==
        self.controlador_principal = Controlador_principal(self)

        # Añadir Widget Principal al Programa
        self.setCentralWidget(self.controlador_principal)

        # Restaurar bordes normales para la app principal
        self.setWindowFlags(Qt.Window) 
        self.setAttribute(Qt.WA_TranslucentBackground, False) # Quitar transparencia
        self.show()

        # Establecer Tamaño Fijo
        self.setFixedSize(1200, 800)

        # Centrar Ventana
        self.centrar_ventana()

    def centrar_ventana(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    app.exec()