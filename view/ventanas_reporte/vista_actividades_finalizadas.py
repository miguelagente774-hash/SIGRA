from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, 
                            QHBoxLayout, QGraphicsDropShadowEffect, QPushButton,
                            QTableWidget, QTableWidgetItem, QHeaderView, 
                            QAbstractItemView, QScrollArea, QWidget, QSizePolicy, QMessageBox)
from PyQt5.QtCore import (Qt)


FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"

BTN_STYLE = """
        QPushButton{
        background: #005a6e;
        color: White;
        font-weight: bold;
        font-size: 18px;
        min-width: 200px;
        min-height: 20px;
        padding: 15px;
        border-radius: 15px;
        text-align: left;
        border: none;
        margin: 0 15px 20px;
        }  
        QPushButton:hover{
        background: #007a94;
        }    
        QPushButton:pressed{
        background: #00485a;
        }"""


class Ventana_reporte_finalizados(QFrame):
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
        Panel_R_finalizado.setStyleSheet("""
                                         QFrame{
                                         background: rgba(255, 255, 255, 0.9);
                                         border-top-left-radius: 15px;
                                         border-top-right-radius: 15px;
                                         border-bottom-left-radius: 15px;
                                         border-bottom-right-radius: 15px;
                                         }""")
        #sombra del panel
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(2, 2)
        Panel_R_finalizado.setGraphicsEffect(sombra)

        titulo = QLabel("Actividades Finalizadas")
        titulo.setStyleSheet("""
                             QLabel{
                             font-family: arial;
                             font-size: 28px; 
                             color: white;
                             font-weight: bold;
                             padding: 20px 15px;
                             margin: 0;
                             background: #005a6e;
                             border-bottom-left-radius: 0;
                             border-bottom-right-radius: 0;
                             }""")
        titulo.setAlignment(Qt.AlignLeft)
        self.Panel_layout.addWidget(titulo)

        #tabla
        

        #----------no tocar-------------------------
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

        self.tabla_actividades.setStyleSheet("""
                                        QTableWidget {
                                        background-color: #f0f0f0; /* Color de fondo de la tabla */
                                        color: #333; /* Color de texto predeterminado */
                                        font-size: 14px;
                                        border: 1px solid #ccc;
                                        margin: 0;
                                        font-family: arial;
                                        }
                                        QHeaderView::section {
                                        background-color: #005a6e;
                                        color: White;
                                        font-size: 16px;
                                        font-weight: bold;
                                        border: 1px solid gray;
                                        text-align: center;
                                        padding: 8px;
                                        margin: 0;
                                        }
                                        QTableWidget::item:selected {
                                             background-color: #a0c0ff;
                                             color: white;
            }
                                        """)
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
        boton_modificar.setStyleSheet(BTN_STYLE)
        boton_modificar.clicked.connect(self.Abrir_modal)
        layout_botones.addWidget(boton_modificar)


        boton_eliminar = QPushButton("Eliminar")
        boton_eliminar.setStyleSheet(BTN_STYLE)
        boton_eliminar.clicked.connect(self.Elminar_actividad)
        layout_botones.addWidget(boton_eliminar)


    def actulizar_tabla(self):
        datos_nuevo = self.controller.Obtener_datos_tabla()
        #limpiar tabla
        self.tabla_actividades.setRowCount(0)

        self.tabla_actividades.setRowCount(len(datos_nuevo))
        #insertamos los nuevos datos
        for indice_fila, fila_datos in enumerate(datos_nuevo):
            #obteniendo columna y los valores
            for indice_columna, valores in enumerate(fila_datos):
                #volviendo tdos los valores en string
                item = QTableWidgetItem(str(valores))
                item.setTextAlignment(Qt.AlignCenter)
                #insertando los datos en sus posiciones correspondiente
                self.tabla_actividades.setItem(indice_fila, indice_columna, item)
        

    def Obtener_indice_tabla(self):
        self.fila_seleccionada = self.tabla_actividades.currentRow()
        
        if self.fila_seleccionada >= 0:
            item = self.tabla_actividades.item(self.fila_seleccionada, 0)
            id_actividad = item.text()
        else:
            id_actividad = None

        return id_actividad
    
    def Limpiar_seleccion_fila(self):
        self.fila_seleccionada = None


    def Abrir_modal(self):
        #self.tabla_actividades.viewport().installEventFilter(self)
        self.controller.Abrir_modal()

    def Elminar_actividad(self):
        confirmacion = QMessageBox.question(self, "Eliminar actividad", "Estas seguro que deseas eliminar?", QMessageBox.Yes, QMessageBox.No)
        if confirmacion == QMessageBox.Yes:
            id_actividad = self.Obtener_indice_tabla()
            self.tabla_actividades.viewport().installEventFilter(self)
            self.controller.Eliminar_actividad(id_actividad)

    def Mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)
    
    def Mensaje_info(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def Mensaje_Warning(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)