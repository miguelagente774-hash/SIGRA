#contenedor principal donde van todas las ventanas juntas con el menu
#todo se va importar aqui

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame)
from controller.Controller_login import controlador_login
from controller.Controller_estadisticas import controlador_estadistica 
from controller.Controller_consulta import controlador_consulta
from controller.Controller_configuraciones import controlador_configuraciones
from controller.ventanas_reporte.Controller_reporte_convertir import controlador_reporte_convertir
from controller.ventanas_reporte.Controller_actividad_crear import controlador_reporte_crear
from controller.ventanas_reporte.Controller_actividades_finalizadas import controlador_reporte_finalizados
from components.menu import Menu
from PyQt5.QtCore import pyqtSignal, QObject


class Comunicador(QObject):
    def __init__(self):
        super().__init__()
        self.señal = pyqtSignal()

comunicador_global = Comunicador()


#----contenedor de toda la app (instanciada en el main.py)
class Controlador_principal(QWidget):
    def __init__(self, ventana):
        super().__init__()

        #Crear la página Principal
        self.ventana = ventana
        self.layout_principal = QHBoxLayout()
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        self.setLayout(self.layout_principal)

        # La Ventana Login como Variable para usarse después
        self.estadistica = controlador_estadistica()
        self.reporte_crear = controlador_reporte_crear()
        self.reporte_finalizados = controlador_reporte_finalizados()
        self.reporte_convertir = controlador_reporte_convertir()
        self.consulta = controlador_consulta()
        self.configuracion = controlador_configuraciones()
        
        # La Ventana de Login como Variable para después.
        self.login = controlador_login()

        # Conectar la Señal de un Login Exitoso
        self.login.get_widget().login_exitoso.connect(self.mostrar_aplicacion_principal)
        
        # Inicialmente mostrar solo el Login al iniciar.
        self.layout_principal.addWidget(self.login.get_widget())
        

    def mostrar_aplicacion_principal(self):
        # Muestra la Aplicación Principal con Menú tras un login exitoso
        for i in reversed(range(self.layout_principal.count())):
            self.layout_principal.itemAt(i).widget().setParent(None)

        # Pantalla completa
        self.mostrar_pantalla_completa()

        # Crear y mostrar la aplicación principal con Menú
        self.Menu()
        self.Contenedor_ventanas()

        # Mostrar la Ventana Principal
        self.Mostrar_Ventana_Principal

    def mostrar_pantalla_completa(self):
    # Configura la Ventana del Programa para que se haga pantalla completa al Iniciar Sesión.
        try:
            # Intentar obtener la ventana principal de diferentes maneras
            main_window = self.window()
            if main_window and hasattr(main_window, 'showMaximized'):
                main_window.showMaximized()
                # Forzar la actualización
                main_window.activateWindow()
                main_window.raise_() 
        except Exception as e:
            print(f"Error al hacer pantalla completa: {e}")


    #----- Metodo que debe contener las configuraciones del menu---------
    def Menu(self):
        self.menu = Menu(self.ventana)
        self.layout_principal.addWidget(self.menu, 1)

    # metodo donde se almacenan las ventanas
    def Contenedor_ventanas(self):
        self.layout_ventanas = QStackedLayout()
        self.menu.funcion_ventanas(
                                    self.layout_ventanas,
                                    self.estadistica.get_widget(),          # Indice 1
                                    self.reporte_crear.get_widget(),        # Indice 2 
                                    self.reporte_finalizados.get_widget(),  # Indice 3
                                    self.reporte_convertir.get_widget(),    # Indice 4
                                    self.consulta.get_widget(),             # Indice 5
                                    self.configuracion.get_widget()         # Indice 6
                                   )
        self.layout_principal.addLayout(self.layout_ventanas, 3)

    def Mostrar_Ventana_Login(self):
        # Muestra la Ventana de Login al Iniciar el Programa.
        self.layout_ventanas.setCurrentIndex(0) # Indice de Login
        self.menu.hide()

    def Mostrar_Ventana_Principal(self):
        # Muestra la Ventana Principal de Programa tras un Login Exitoso.
        self.layout_ventanas.setCurrentIndex(1) # Indice de Ventana Principal
        self.menu.show()
