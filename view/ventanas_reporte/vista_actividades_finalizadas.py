from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, 
                            QHBoxLayout, QGraphicsDropShadowEffect, QPushButton,
                            QTableWidget, QTableWidgetItem, QHeaderView, 
                            QSizePolicy, QMessageBox)
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QColor
from components.app_style import estilo_app

# Clase: Ventana de Reportes Finalizados
class Ventana_reporte_finalizados(QFrame):
    def __init__(self, controller):
        super().__init__()
        # Definir Variables Iniciales
        self.estilo = estilo_app.obtener_estilo_completo()
        self.controller = controller
        
        # Establecer el Tema del Fondo
        self.setStyleSheet(self.estilo["styles"]["fondo"])
                
        # Registrar esta vista para actualización automática
        estilo_app.registrar_vista(self)
        
        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)
        
        # Inicializar Métodos Iniciales
        self.setup_panel()

    def setup_panel(self):
        # Layout Principal
        self.layout_principal = QVBoxLayout(self)

        # Contenedor
        contenedor_panel = QFrame()
        contenedor_panel.setMinimumHeight(250)
        contenedor_panel.setStyleSheet(self.estilo["styles"]["panel"])
        contenedor_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contenedor_panel.setMinimumSize(700, 450)

        # Sombra de la Ventana
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        colores = self.estilo["colors"]
        sombra.setColor(QColor(colores.get("shadow", Qt.gray)))
        sombra.setOffset(2, 2)
        contenedor_panel.setGraphicsEffect(sombra)

        # Layout del Panel
        layout_panel = QVBoxLayout(contenedor_panel)

        # Título de la Ventana
        titulo = QLabel("Actividades Finalizadas")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        layout_panel.addWidget(titulo)
        
        # Métodos
        self.tabla(layout_panel)
        self.botones(layout_panel)

        # Añadir Contenedor al Layout Principal
        self.layout_principal.addWidget(contenedor_panel)

    def tabla(self, layout):
        #crear tabla
        self.tabla_actividades = QTableWidget()
        datos = self.controller.Obtener_datos_tabla()
        self.tabla_actividades.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.tabla_actividades)

        #ocultar encabezado vertical
        header_verticar = self.tabla_actividades.verticalHeader()
        header_verticar.setSectionResizeMode(QHeaderView.Fixed)
        header_verticar.setDefaultAlignment(Qt.AlignCenter)
        header_verticar.setFixedWidth(60)
        header_verticar.setVisible(False)

        #configuracion de las filas y columnas de la tabla
        self.tabla_actividades.setColumnCount(4)

        self.tabla_actividades.setRowCount(len(datos))

        self.tabla_actividades.setStyleSheet(self.estilo["styles"]["tabla"])
        encabezados = ["ID", "Titulo", "Descripcion", "Fecha"]
        self.tabla_actividades.setHorizontalHeaderLabels(encabezados)

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
        

    def botones(self, layout):
        layout_botones = QHBoxLayout()

        boton_modificar = QPushButton("Modificar")
        boton_modificar.setStyleSheet(self.estilo["styles"]["boton"])
        boton_modificar.clicked.connect(self.Abrir_modal)
        layout_botones.addWidget(boton_modificar)


        boton_eliminar = QPushButton("Eliminar")
        boton_eliminar.setStyleSheet(self.estilo["styles"]["boton"])
        boton_eliminar.clicked.connect(self.Elminar_actividad)
        layout_botones.addWidget(boton_eliminar)
        
        layout.addLayout(layout_botones)

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
        # Actualizar los estilo de la vista
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        
        # Aplicar fondo a la vista principal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar panel principal
        for widget in self.findChildren(QFrame):
            # Buscar el panel principal por su título
            child_labels = [child.text() for child in widget.findChildren(QLabel) if child.text()]
            if "Actividades Finalizadas" in child_labels:
                widget.setStyleSheet(self.estilo["styles"]["panel"])
                
                # Actualizar sombra
                if widget.graphicsEffect():
                    effect = widget.graphicsEffect()
                    if isinstance(effect, QGraphicsDropShadowEffect):
                        effect.setColor(QColor(colores.get("shadow", Qt.gray)))
        
        # Actualizar título
        for widget in self.findChildren(QLabel):
            if widget.text() == "Actividades Finalizadas":
                widget.setStyleSheet(self.estilo["styles"]["header"])
        
        # Actualizar tabla
        if hasattr(self, 'tabla_actividades'):
            # Actualizar estilo de la tabla completa
            self.tabla_actividades.setStyleSheet(self.estilo["styles"]["tabla"])
            
            # Actualizar header horizontal
            header = self.tabla_actividades.horizontalHeader()
            header.setStyleSheet(f"""
                QHeaderView::section {{
                    background-color: {colores["table_header"]};
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    border: 1px solid {colores["border"]};
                    font-size: {self.estilo["font_size"] + 2}px;
                }}
            """)
            
            # Actualizar texto en las celdas
            for row in range(self.tabla_actividades.rowCount()):
                for col in range(self.tabla_actividades.columnCount()):
                    item = self.tabla_actividades.item(row, col)
                    if item:
                        item.setForeground(QColor(colores["text_primary"]))
        
        # Actualizar botones
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(self.estilo["styles"]["boton"])