#contenedor principal donde van todas las ventanas juntas con el menu
#todo se va importar aqui

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame)
from controller.Controller_estadisticas import ControladorEstadistica 
from controller.Controller_consulta import controlador_consulta
from controller.Controller_configuraciones import controlador_configuraciones
from controller.ventanas_reporte.Controller_reporte_convertir import controlador_reporte_convertir
from controller.ventanas_reporte.Controller_actividad_crear import controlador_reporte_crear
from controller.ventanas_reporte.Controller_actividades_finalizadas import controlador_reporte_finalizados
from components.menu import Menu
from PyQt5.QtCore import pyqtSignal, QObject
from components.app_style import estilo_app


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

        # Instanciar controladores de cada vista del programa
        self.estadistica = ControladorEstadistica()
        self.reporte_crear = controlador_reporte_crear()
        self.reporte_finalizados = controlador_reporte_finalizados()
        self.reporte_convertir = controlador_reporte_convertir()
        self.consulta = controlador_consulta()
        self.configuracion = controlador_configuraciones()

        # Inicialmente mostrar solo el Login al iniciar.
        self.registrar_vistas()


        # Crear y mostrar la aplicación principal con Menú
        self.Menu()
        self.Contenedor_ventanas()
        self.Mostrar_Ventana_Principal()

        self.actualizar_vistas()

        # Actualizar las ventanas
        self.configuracion.Actualizar_Vista.connect(self.on_config_guardada)


    def registrar_vistas(self):
            vistas = [
                # Registrar vistas para ctualización automática
                self.estadistica.get_widget(),
                self.reporte_crear.get_widget(),
                self.reporte_finalizados.get_widget(),
                self.reporte_convertir.get_widget(),
                self.consulta.get_widget(),
                self.configuracion.get_widget()
            ]
            for vista in vistas:
                if vista:
                    estilo_app.registrar_vista(vista)

        # Incializar estilos
    

    def actualizar_vistas(self):
        # ==Actualiza todas las vistas de la aplicación==
        vistas = [
            self.estadistica.get_widget(),          # Indice 1
            self.reporte_crear.get_widget(),        # Indice 2 
            self.reporte_finalizados.get_widget(),  # Indice 3
            self.reporte_convertir.get_widget(),    # Indice 4
            self.consulta.get_widget(),             # Indice 5
            self.configuracion.get_widget()         # Indice 6
        ]
        # Registrar cada vista si no lo está
        for vista in vistas:
            if vista and vista not in estilo_app.vistas_registradas:
                estilo_app.registrar_vista(vista)
        
        # Notificar cambios
        estilo_app.notificar_cambio_estilos()

    def on_config_guardada(self):
        pass


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

    def Mostrar_Ventana_Principal(self):
        # Muestra la Ventana Principal de Programa tras un Login Exitoso.
        self.layout_ventanas.setCurrentIndex(0) # Indice de Ventana Principal
        self.menu.show()
