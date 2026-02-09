import sys
from PyQt5.QtWidgets import (
    QApplication, QFrame, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMainWindow, QLabel,
    QGraphicsDropShadowEffect, QLineEdit, QComboBox, QSizePolicy, QWidget, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from components.app_style import estilo_app

# Clase: Ventana Consulta
class Ventana_consulta(QFrame):
    def __init__(self, controlador):
        super().__init__()
        # Definir Variables Iniciales
        self.controlador = controlador
        self.estilo = estilo_app.obtener_estilo_completo()

        # Establecer el Tema del Fondo
        self.setStyleSheet(self.estilo["styles"]["fondo"])
                
        # Registrar esta vista para actualización automática
        estilo_app.registrar_vista(self)
        
        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)
        
        # Inicializar Métodos Iniciales
        self._configurar_combo_ordenacion()
        self._configurar_tabla()
        self.setup_panel()
        self._conectar_senales()

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
        titulo = QLabel("Consulta")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        layout_panel.addWidget(titulo)

        # Buscador y Ordenación
        layout_buscador_ordenacion = QHBoxLayout()
        layout_buscador_ordenacion.setSpacing(10)
        
        # Campo de Búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar por ID o Título...")
        self.campo_busqueda.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.campo_busqueda.setStyleSheet(self.estilo["styles"]["input"])
        
        # Label de Ordenar
        etiqueta_ordenar = QLabel("Buscar de manera")
        etiqueta_ordenar.setStyleSheet(self.estilo["styles"]["title"])
        etiqueta_ordenar.setContentsMargins(5, 10, 0, 10)
        etiqueta_ordenar.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Añadir los Widget a la fila de Búsqueda
        layout_buscador_ordenacion.addWidget(self.campo_busqueda)
        layout_buscador_ordenacion.addWidget(etiqueta_ordenar)
        layout_buscador_ordenacion.addWidget(self.combo_ordenacion)

        layout_panel.addLayout(layout_buscador_ordenacion)

        # Tabla
        self.tabla.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_panel.addWidget(self.tabla, 1)

        # Crear Botones
        layout_botones = QHBoxLayout()
        layout_panel.addLayout(layout_botones)
        boton_pdf = QPushButton("Reporte-PDF")
        boton_pptx = QPushButton("Reporte-PPTX")
        boton_eliminar = QPushButton("Eliminar")

        # Aplicar estilo a todos los botones
        for boton in [boton_pdf, boton_pptx, boton_eliminar]:
            boton.setStyleSheet(self.estilo["styles"]["boton"])
        
        # Conectar señales
        boton_pdf.clicked.connect(self.Abrir_modal_pdf)
        boton_pptx.clicked.connect(self.Abrir_modal)
        boton_eliminar.clicked.connect(self.Eliminar_reporte)
        
        # Centrar botones
        layout_botones.addWidget(boton_pdf)
        layout_botones.addWidget(boton_pptx)
        layout_botones.addWidget(boton_eliminar)
        
        

        # Añadir Contenedor al Layout Principal
        self.layout_principal.addWidget(contenedor_panel)

    def _configurar_combo_ordenacion(self):
        # ==Configura los ítems y el estilo inicial del QComboBox==
        self.combo_ordenacion = QComboBox()
        self.combo_ordenacion.addItem("Ascendente")
        self.combo_ordenacion.addItem("Descendente")
        self.combo_ordenacion.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.combo_ordenacion.setStyleSheet(self.estilo["styles"]["input"])
        
    def _configurar_tabla(self):
        # ==Configura los encabezados y el estilo de la tabla==
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels([ "ID", "Titulo", "Fecha" ])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(40)
        
        cabecera = self.tabla.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.Fixed)  # ID
        self.tabla.setColumnWidth(0, 100)
        cabecera.setSectionResizeMode(1, QHeaderView.Stretch)  # Título
        cabecera.setSectionResizeMode(2, QHeaderView.Fixed)  # Fecha
        self.tabla.setColumnWidth(2, 150)
        
        # Aplicar Estilo a la Tabla
        self.tabla.setStyleSheet(self.estilo["styles"]["tabla"])
        
        self.actulizar_tabla()
        
        
    def actulizar_tabla(self):
        self.datos_prueba = self.controlador.Obtener_reportes()
        self._cargar_datos_en_tabla(self.datos_prueba)

    def _conectar_senales(self):
        # ==Conecta las señales de los widgets a sus métodos==
        self.campo_busqueda.textChanged.connect(self._aplicar_filtro)
        self.combo_ordenacion.currentIndexChanged.connect(self._aplicar_filtro)
        
    # LÓGICA DE FILTRADO Y ORDENACIÓN
    def _aplicar_filtro(self, *args):
        filtro = self.campo_busqueda.text().strip().lower()
        orden_descendente = (self.combo_ordenacion.currentIndex() == 1)

        if not filtro:
            datos_filtrados = list(self.datos_prueba)
        else:
            datos_filtrados = [
                fila for fila in self.datos_prueba
                if filtro in f"{fila[0]} {fila[1]}".lower()
            ]

        # Ordenar por el primer elemento (ID)
        datos_filtrados.sort(key=lambda x: int(x[0]), reverse=orden_descendente)

        self._cargar_datos_en_tabla(datos_filtrados)

    def _cargar_datos_en_tabla(self, datos):
        self.tabla.setRowCount(len(datos))
        colores = self.estilo["colors"]
        
        for indice_fila, datos_fila in enumerate(datos):
            for indice_columna, item in enumerate(datos_fila):
                item_tabla = QTableWidgetItem(str(item))
                # **SOLUCIÓN 7: Aplicar color de texto correcto**
                item_tabla.setForeground(QBrush(QColor(colores["text_primary"])))
                
                if indice_columna == 0 or indice_columna == 1 or indice_columna == 2:
                    item_tabla.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(indice_fila, indice_columna, item_tabla)
                
        #if len(datos) > 0:
        #    self.tabla.selectRow(0)

    def Eliminar_reporte(self):
            datos_reporte = self.Obtener_reporte_seleccionado()
            if datos_reporte != None:
                id_reporte = datos_reporte[0]
                
                confirmacion = QMessageBox.question(self, "Eliminar Reporte", "Estás seguro que deseas eliminar?", QMessageBox.Yes | QMessageBox.No)    
                
                if confirmacion == QMessageBox.Yes:
                    self.controlador.Eliminar_reporte(id_reporte)
            else:
                self.mensaje_error("error", "no hay una actividad seleccionada")
            


    def Obtener_reporte_seleccionado(self):
        #fila seleccionada
        fila_seleccionda = self.tabla.currentRow()
        if fila_seleccionda >= 0:
            id_reporte = self.tabla.item(fila_seleccionda, 0).text()
            nombre_reporte = self.tabla.item(fila_seleccionda, 1).text()
            datos_reporte = [id_reporte, nombre_reporte]
        else:
            datos_reporte = None

        return datos_reporte
    
    def Abrir_modal(self):
        datos_reporte = self.Obtener_reporte_seleccionado()
        try:
            nombre_reporte = datos_reporte[1]
            self.controlador.abrir_modal(nombre_reporte)
        except:
            self.mensaje_advertencia("Advertencia", "Por favor seleccione un Reporte")

    def Abrir_modal_pdf(self):
        datos_reporte = self.Obtener_reporte_seleccionado()
        try:
            nombre_reporte = datos_reporte[1]
            self.controlador.abrir_modal_pdf(nombre_reporte)
        except:
            self.mensaje_advertencia("Advertencia", "Por favor seleccione un Reporte")


    def mensaje_advertencia(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def mensaje_informativo(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)

    def actualizar_estilos(self):
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        
        # Aplicar fondo a la vista principal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar panel principal y sombra
        for widget in self.findChildren(QFrame):
            if hasattr(widget, 'graphicsEffect'):
                if widget.graphicsEffect():
                    effect = widget.graphicsEffect()
                    if isinstance(effect, QGraphicsDropShadowEffect):
                        effect.setColor(QColor(colores.get("shadow", Qt.gray)))
                widget.setStyleSheet(self.estilo["styles"]["panel"])
        
        # Actualizar título
        for widget in self.findChildren(QLabel):
            if widget.text() == "Consulta":
                widget.setStyleSheet(self.estilo["styles"]["header"])
        
        # Actualizar tabla
        if hasattr(self, 'tabla'):
            # Actualizar estilo de la tabla completa
            self.tabla.setStyleSheet(self.estilo["styles"]["tabla"])
            
            # Actualizar header de la tabla
            cabecera = self.tabla.horizontalHeader()
            cabecera.setStyleSheet(f"""
                QHeaderView::section {{
                    background-color: {colores["table_header"]};
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    border: 1px solid {colores["border"]};
                    font-size: {self.estilo["font_size"] + 2}px;
                }}
            """)
            
            # Actualizar colores de texto en todas las celdas
            for row in range(self.tabla.rowCount()):
                for col in range(self.tabla.columnCount()):
                    item = self.tabla.item(row, col)
                    if item:
                        item.setForeground(QBrush(QColor(colores["text_primary"])))
        
        # Actualizar inputs
        for widget in self.findChildren((QLineEdit, QComboBox)):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        # Actualizar labels
        for widget in self.findChildren(QLabel):
            if widget.text() != "Consulta":  # Ya actualizamos el título
                widget.setStyleSheet(self.estilo["styles"]["title"])
        
        # Actualizar botones
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(self.estilo["styles"]["boton"])
        
        # Actualizar área de contenido
        for widget in self.findChildren(QFrame):
            if "Buscar de manera" in [child.text() for child in widget.findChildren(QLabel) if child.text()]:
                widget.setStyleSheet(f"""
                    QFrame {{
                        background: {colores["bg_panel"]};
                        border-radius: 8px;
                        padding: 0;
                        margin: 0;
                    }}
                """)