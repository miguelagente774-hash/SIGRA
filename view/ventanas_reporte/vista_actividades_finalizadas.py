from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, 
                            QHBoxLayout, QGraphicsDropShadowEffect, QPushButton,
                            QTableWidget, QTableWidgetItem, QHeaderView, 
                            QLineEdit, QTextEdit, QComboBox, QDateEdit, QMessageBox)
from PyQt5.QtCore import (Qt)
from components.app_style import estilo_app

class Ventana_reporte_finalizados(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.estilo = estilo_app.obtener_estilo_completo()
        self.controller = controller
        self.Main_layout = QVBoxLayout()
        self.Main_layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(self.Main_layout)

        estilo_app.registrar_vista(self)
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)        

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
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignLeft)
        self.Panel_layout.addWidget(titulo)
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

        self.tabla_actividades.setStyleSheet(self.estilo["styles"]["tabla"])
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
        boton_modificar.setStyleSheet(self.estilo["styles"]["boton"])
        boton_modificar.clicked.connect(self.Abrir_modal)
        layout_botones.addWidget(boton_modificar)


        boton_eliminar = QPushButton("Eliminar")
        boton_eliminar.setStyleSheet(self.estilo["styles"]["boton"])
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

    # Método en cada vista:
    def actualizar_estilos(self):
        """Actualiza los estilos de esta vista"""
        self.estilo = estilo_app.obtener_estilo_completo()
        
        # Aplica el fondo
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar paneles específicos
        for widget in self.findChildren(QFrame):
            if hasattr(widget, 'panel') or 'panel' in widget.objectName().lower():
                widget.setStyleSheet(self.estilo["styles"]["panel"])
        
        # Actualizar botones
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(self.estilo["styles"]["boton"])
        
        # Actualizar inputs
        for widget in self.findChildren((QLineEdit, QTextEdit, QComboBox, QDateEdit)):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        # Actualizar tablas
        for widget in self.findChildren(QTableWidget):
            widget.setStyleSheet(self.estilo["styles"]["tabla"])
        
        print(f"🔄 {self.__class__.__name__} actualizada")