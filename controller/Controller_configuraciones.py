from view.vista_configuracion import Ventana_configuracion
from models.Modelo_configuraciones import Model_Configuraciones
from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout,
                             QGraphicsDropShadowEffect, QGroupBox, QRadioButton,
                             QSizePolicy, QSpacerItem, QSpinBox, QComboBox, QCheckBox,
                             QGridLayout, QLineEdit, QButtonGroup, QPushButton, 
                             QScrollArea, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class controlador_configuraciones():
    def __init__(self):
        self.configuraciones = Ventana_configuracion()
        self.modelo = Model_Configuraciones()

    def resizeEvent(self, event):
        """Detectar cambios de tamaño y ajustar layout"""
        super().resizeEvent(event)
        if self.current_width != self.width():
            self.current_width = self.width()
            self.ajustar_responsive()

    def ajustar_responsive(self):
        """Ajustar la interfaz según el ancho de pantalla"""
        ancho = self.current_width
        
        # Definir breakpoints
        if ancho <= 600:  # Móviles
            self.aplicar_estilo_movil()
        elif ancho <= 900:  # Tablets
            self.aplicar_estilo_tablet()
        else:  # Desktop
            self.aplicar_estilo_desktop()

    def aplicar_estilo_movil(self):
        """Estilos para dispositivos móviles"""
        self.layout_main.setContentsMargins(10, 10, 10, 10)
        self.layout_main.setSpacing(15)
        
        grupos = self.findChildren(QGroupBox)
        for grupo in grupos:
            grupo.setStyleSheet(grupo.styleSheet() + """
                QGroupBox {
                    margin: 5px;
                    padding: 15px 10px;
                    min-width: 200px;
                }
            """)

    def aplicar_estilo_tablet(self):
        """Estilos para tablets"""
        self.layout_main.setContentsMargins(15, 15, 15, 15)
        self.layout_main.setSpacing(20)

    def aplicar_estilo_desktop(self):
        """Estilos para desktop"""
        self.layout_main.setContentsMargins(20, 20, 20, 20)
        self.layout_main.setSpacing(30)


    def get_widget(self):
        # Retorna el widget de Configuraciones
        return self.configuraciones
    
    def get_modelo(self):
        # Obtiene el modelo
        return self.modelo