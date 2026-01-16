from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, 
                            QHBoxLayout, QGraphicsDropShadowEffect, QPushButton,
                            QTableWidget, QTableWidgetItem, QHeaderView, 
                            QAbstractItemView, QScrollArea, QWidget, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from components.app_style import estilo_app

# Instancia global para el uso en toda la aplicación
estilo = estilo_app.obtener_estilo_completo()

# Variables globales para la consistencia
FONT_FAMILY = estilo["font_family"]
COLOR_PRIMARIO = estilo["color_primario"]
COLOR_AZUL_HOVER = estilo["color_hover"]
COLOR_SECUNDARIO = estilo["color_secundario"]
BG_COLOR_PANEL = estilo["colors"]["bg_panel"]
BG_COLOR_FONDO = estilo["colors"]["bg_fondo"]

class Ventana_reporte_finalizados(QFrame):
    modificar_actividad = pyqtSignal()
    eliminar_actividad = pyqtSignal()
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.Main_layout = QVBoxLayout()
        self.Main_layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(self.Main_layout)
        

        #funciones
        self.Panel_r_finalizado()
        self.tabla_actividade()
        self.botones()

    def Panel_r_finalizado(self):
        self.Panel_layout = QVBoxLayout()
        self.Panel_layout.setContentsMargins(0, 0, 0, 0)
        self.Panel_layout.setSpacing(10)
        
        Panel_R_finalizado = QFrame()
        Panel_R_finalizado.setLayout(self.Panel_layout)
        Panel_R_finalizado.setStyleSheet(f"""
                                         QFrame{{
                                         background: {BG_COLOR_PANEL};
                                         border-top-left-radius: 15px;
                                         border-top-right-radius: 15px;
                                         border-bottom-left-radius: 15px;
                                         border-bottom-right-radius: 15px;
                                         }}""")
        #sombra del panel
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(2, 2)
        Panel_R_finalizado.setGraphicsEffect(sombra)

        titulo = QLabel("Actividades Finalizadas")
        titulo.setStyleSheet(estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        self.Panel_layout.addWidget(titulo)
        self.Main_layout.addWidget(Panel_R_finalizado)

    def tabla_actividade(self):
        #crear tabla
        self.tabla_actividades = QTableWidget()
        datos = self.controller.Obtener_datos_tabla()
        self.tabla_actividades.setEditTriggers(QTableWidget.NoEditTriggers)
        
        #ocultar encabezado vertical
        header_verticar = self.tabla_actividades.verticalHeader()
        header_verticar.setSectionResizeMode(QHeaderView.Fixed)
        header_verticar.setDefaultAlignment(Qt.AlignCenter)
        header_verticar.setFixedWidth(70)

        #configuracion de las filas y columnas de la tabla
        self.tabla_actividades.setColumnCount(4)

        self.tabla_actividades.setRowCount(len(datos))

        self.tabla_actividades.setStyleSheet(estilo["styles"]["tabla"])

        encabezados = ["ID", "Titulo", "Descripcion", "Fecha"]
        self.tabla_actividades.setHorizontalHeaderLabels(encabezados)

        self.Panel_layout.addWidget(self.tabla_actividades)

        #configuracion de la tabla
        header = self.tabla_actividades.horizontalHeader()
        #conbfiguracion de la primera columna
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.tabla_actividades.setColumnWidth(0, 100)
        #configuracion de la segunda columna
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        self.tabla_actividades.setColumnWidth(1, 300)
        #configuracion de la tercera columna
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        #configuracion de la cuarta columna
        header.setSectionResizeMode(3, QHeaderView.Interactive)
        self.tabla_actividades.setColumnWidth(3, 250)

        #insertar datos en la tablas
        #obteniendo fila y las tuplas 
        for indice_fila, fila_datos in enumerate(datos):
            #obteniendo columna y los valores
            for indice_columna, valores in enumerate(fila_datos):
                #volviendo tdos los valores en string
                item = QTableWidgetItem(str(valores))
                item.setTextAlignment(Qt.AlignCenter)
                #insertando los datos en sus posiciones correspondiente
                self.tabla_actividades.setItem(indice_fila, indice_columna, item)
            

    def botones(self):
        layout_botones = QHBoxLayout()
        self.Panel_layout.addLayout(layout_botones)

        boton_modificar = QPushButton("Modificar")
        boton_modificar.setStyleSheet(estilo["styles"]["boton"])
        boton_modificar.clicked.connect(self.modificar_actividad.emit)
        layout_botones.addWidget(boton_modificar)


        boton_eliminar = QPushButton("Eliminar")
        boton_eliminar.setStyleSheet(estilo["styles"]["boton"])
        boton_eliminar.clicked.connect(self.eliminar_actividad.emit)
        layout_botones.addWidget(boton_eliminar)

    
    def Mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)
    
    def Mensaje_info(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def Mensaje_Warning(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)