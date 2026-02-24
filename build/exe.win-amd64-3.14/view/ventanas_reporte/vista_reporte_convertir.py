from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView,
                             QCheckBox, QMessageBox, QLineEdit, QTextEdit, QComboBox, QSizePolicy)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from comunicador import Comunicador_global
from datetime import datetime
from components.app_style import estilo_app
import locale

# Ventana de Convertir Actividades en Reportes
class Ventana_convertir_reporte(QFrame):
    def __init__(self, controller):
        super().__init__()
        # Definir Variables Iniciales
        self.estilo = estilo_app.obtener_estilo_completo()
        self.controller = controller
        
        #estableciendo el sistema a español
        locale.setlocale(locale.LC_TIME, "Spanish_Spain")

        # Establecer el Tema de Fondo
        self.setStyleSheet(self.estilo["styles"]["fondo"])

        # Registrar esta vista para actualización automática
        estilo_app.registrar_vista(self)
        
        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)    

        # Conectar señal del Comunicador
        Comunicador_global.actividad_agregada.connect(self.cargar_datos_tabla)

        # Inicializar Métodos Iniciales
        self.setup_panel()
        self.cargar_datos_tabla()

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
        titulo = QLabel("Convertir Reporte")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        layout_panel.addWidget(titulo)
        
        # Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar actividades por título o ID...")
        self.campo_busqueda.setStyleSheet(self.estilo["styles"]["input"])
        self.campo_busqueda.textChanged.connect(self.filtrar_actividades)
        
        layout_panel.addWidget(self.campo_busqueda)
        
        # Crear tabla de actividades
        self.crear_tabla_actividades(layout_panel)
        
        # Crear botones de acción
        self.crear_botones_accion(layout_panel)

        self.layout_principal.addWidget(contenedor_panel)

    def crear_tabla_actividades(self, layout):
        """Crea la tabla con las actividades y checkboxes de selección"""
        self.tabla_actividades = QTableWidget()
        self.tabla_actividades.setColumnCount(4)  # Checkbox, ID, Título, Fecha
        self.tabla_actividades.setHorizontalHeaderLabels(["✓", "ID", "Título", "Fecha"])
        
        # Configurar tabla
        self.tabla_actividades.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_actividades.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_actividades.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_actividades.verticalHeader().setVisible(False)
        self.tabla_actividades.setAlternatingRowColors(True)
        
        # Estilo de la tabla
        self.tabla_actividades.setStyleSheet(self.estilo["styles"]["tabla"])
        
        # Configurar cabeceras
        header = self.tabla_actividades.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Checkbox
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # Título
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Fecha
        
        
        # Configurar altura de filas
        self.tabla_actividades.verticalHeader().setDefaultSectionSize(50)
        
        # Asegurar que el header sea visible
        header.setVisible(True)
        
        layout.addWidget(self.tabla_actividades)
    
    # cargar los datos para mostrar en la tabla
    def cargar_datos_tabla(self):
        """Carga los datos de actividades en la tabla agrupadas por mes"""
        # Obtener actividades desde el controlador
        self.actividades = self.controller.Obtener_actividades()
        
        # Si no hay actividades, limpiar tabla y salir
        if not self.actividades:
            self.tabla_actividades.setRowCount(0)
            return
        
        # Obtener colores del tema actual
        colores = self.estilo["colors"]
        
        # Ordenar actividades por fecha (actividad[2] es la fecha)
        actividades_ordenadas = sorted(self.actividades, key=lambda x: datetime.strptime(x[2], '%d-%m-%Y'), reverse=True)
        
        # Inicializar variables de control
        mes_actual = actividades_ordenadas[0]

        
        numero_fila = 0
        
        # Limpiar tabla completamente
        self.tabla_actividades.setRowCount(0)
        
        # Recorrer todas las actividades ordenadas
        for actividad in actividades_ordenadas:
            # Extraer el mes de la fecha (asumiendo formato "YYYY-MM-DD")
            try:
                fecha_obj = datetime.strptime(actividad[2], "%d-%m-%Y")
                año_mes = fecha_obj.strftime("%Y-%m")
                nombre_mes = fecha_obj.strftime("%B %Y")  # Ej: "Enero 2024"
                nombre_mes = nombre_mes.capitalize()  # Para asegurar que el nombre del mes esté en mayúscula
                
            except ValueError:
                # Si hay error en el formato de fecha, usar un valor por defecto
                año_mes = "Fecha inválida"
                nombre_mes = "Fecha inválida"

            # Verificar si cambió el mes
            if año_mes != mes_actual:
                # Si no es el primer mes, agregar separador
                if mes_actual is not None:
                    # Agregar fila para el separador
                    self.tabla_actividades.insertRow(numero_fila)
                    
                    # **SOLUCIÓN: Usar color del tema para el separador**
                    elemento_separador = QTableWidgetItem(f"{nombre_mes}")
                    elemento_separador.setBackground(QColor(colores["table_header_secondary"]))  # Color del tema
                    elemento_separador.setForeground(QColor("White"))  # Texto blanco para mejor contraste
                    
                    # Deshabilitar edición del separador
                    elemento_separador.setFlags(elemento_separador.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable)
                    
                    # Hacer el texto en negrita
                    fuente = QFont()
                    fuente.setBold(True)
                    elemento_separador.setFont(fuente)
                    
                    # Centrar el texto
                    elemento_separador.setTextAlignment(Qt.AlignCenter)
                    
                    # Colocar en la columna de título (columna 0)
                    self.tabla_actividades.setItem(numero_fila, 0, elemento_separador)
                    
                    # Unir celdas para el separador (columnas 2, 3)
                    self.tabla_actividades.setSpan(numero_fila, 0, 1, 4)
                    
                    # Avanzar a la siguiente fila
                    numero_fila += 1
                
                # Actualizar el mes actual
                mes_actual = año_mes
            
            # Agregar fila para la actividad
            self.tabla_actividades.insertRow(numero_fila)
            
            # Checkbox de selección (columna 0)
            checkbox = QCheckBox()
            checkbox.setStyleSheet(self.estilo["styles"]["checkbox"])
            self.tabla_actividades.setCellWidget(numero_fila, 0, checkbox)
            
            # ID (columna 1)
            id_item = QTableWidgetItem(str(actividad[0]))
            id_item.setTextAlignment(Qt.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            # **SOLUCIÓN: Aplicar color de texto del tema**
            id_item.setForeground(QColor(colores["text_primary"]))
            self.tabla_actividades.setItem(numero_fila, 1, id_item)
            
            # Título (columna 2)
            titulo_item = QTableWidgetItem(actividad[1])
            titulo_item.setFlags(titulo_item.flags() & ~Qt.ItemIsEditable)
            # **SOLUCIÓN: Aplicar color de texto del tema**
            titulo_item.setForeground(QColor(colores["text_primary"]))
            self.tabla_actividades.setItem(numero_fila, 2, titulo_item)
            
            # Fecha (columna 3)
            fecha_item = QTableWidgetItem(actividad[2])
            fecha_item.setTextAlignment(Qt.AlignCenter)
            fecha_item.setFlags(fecha_item.flags() & ~Qt.ItemIsEditable)
            # **SOLUCIÓN: Aplicar color de texto del tema**
            fecha_item.setForeground(QColor(colores["text_primary"]))
            self.tabla_actividades.setItem(numero_fila, 3, fecha_item)
            
            # Avanzar a la siguiente fila
            numero_fila += 1
        
        # Ajustar columnas después de cargar datos
        self.ajustar_columnas_tabla()

    
    def ajustar_columnas_tabla(self):
        """Ajusta el tamaño de las columnas para mejor visualización"""
        # Establecer anchos específicos para mejor visibilidad
        self.tabla_actividades.setColumnWidth(0, 60)   # Checkbox
        self.tabla_actividades.setColumnWidth(1, 80)   # ID
        self.tabla_actividades.setColumnWidth(3, 120)  # Fecha
        # La columna 2 (Título) se expandirá con Stretch
    
    def crear_botones_accion(self, layout):
        """Crea los botones de acción"""
        botones_layout = QHBoxLayout()

        self.campo_nombre_reporte = QLineEdit()
        self.campo_nombre_reporte.setPlaceholderText("Nombre para el reporte")
        self.campo_nombre_reporte.setStyleSheet(self.estilo["styles"]["input"])
        botones_layout.addWidget(self.campo_nombre_reporte)
        
        # Botón para seleccionar todos
        self.btn_seleccionar_todos = QPushButton("Seleccionar Todos")
        self.btn_seleccionar_todos.setStyleSheet(self.estilo["styles"]["boton"])
        self.btn_seleccionar_todos.clicked.connect(self.toggle_seleccion_todos)

        # Botón para continuar
        btn_continuar = QPushButton("Continuar")
        btn_continuar.setStyleSheet(self.estilo["styles"]["boton"])
        btn_continuar.clicked.connect(self.continuar_con_seleccion)
        
        botones_layout.addWidget(self.btn_seleccionar_todos)
        botones_layout.addWidget(btn_continuar)
        
        layout.addLayout(botones_layout)
    
    def filtrar_actividades(self):
        """Filtra las actividades según el texto de búsqueda"""
        texto = self.campo_busqueda.text().lower()
        
        for fila in range(self.tabla_actividades.rowCount()):
            titulo = self.tabla_actividades.item(fila, 2).text().lower()
            id_texto = self.tabla_actividades.item(fila, 2).text().lower()
            
            # Mostrar u ocultar fila según coincidencia
            if texto in titulo or texto in id_texto:
                self.tabla_actividades.setRowHidden(fila, False)
            else:
                self.tabla_actividades.setRowHidden(fila, True)
    
    def obtener_actividades_seleccionadas(self):
        """Retorna una lista con las actividades que tienen el checkbox marcado"""
        seleccionados = []
    
        for fila in range(self.tabla_actividades.rowCount()):
            # Obtener el checkbox de la columna 0
            checkbox = self.tabla_actividades.cellWidget(fila, 0)
            
            if checkbox and checkbox.isChecked():
                # Obtener datos de la fila
                id_actividad = self.tabla_actividades.item(fila, 1).text()
                titulo = self.tabla_actividades.item(fila, 2).text()
                fecha = self.tabla_actividades.item(fila, 3).text()
                
                ("Id:",id_actividad,"Titulo:", titulo,"Fecha:",fecha)
                # Agregar a la lista de seleccionados
                seleccionados.append({
                    'id': int(id_actividad)
                })
        
        return seleccionados

    def toggle_seleccion_todos(self):
        """Selecciona o deselecciona todas las actividades"""
        todas_seleccionadas = True
        
        # Verificar si ya están todas seleccionadas
        for fila in range(self.tabla_actividades.rowCount()):
            if not self.tabla_actividades.isRowHidden(fila):
                checkbox = self.tabla_actividades.cellWidget(fila, 0)
                if checkbox and not checkbox.isChecked():
                    todas_seleccionadas = False
                    break
        
        # Toggle: si todas están seleccionadas, deseleccionar; si no, seleccionar todas
        for fila in range(self.tabla_actividades.rowCount()):
            if not self.tabla_actividades.isRowHidden(fila):
                checkbox = self.tabla_actividades.cellWidget(fila, 0)
                if checkbox:
                    checkbox.setChecked(not todas_seleccionadas)
        
        # Cambiar texto del botón
        if todas_seleccionadas:
            self.btn_seleccionar_todos.setText("Seleccionar Todos")
        else:
            self.btn_seleccionar_todos.setText("Deseleccionar Todos")

    def continuar_con_seleccion(self):
        """Procesa la creación del reporte"""
        # 1. Obtener nombre del reporte
        nombre_reporte = self.campo_nombre_reporte.text().strip()
        if not nombre_reporte:
            self.mensaje_advertencia("Advertencia", "Por favor, ingresa un nombre para el reporte")
            return
        
        # 2. Obtener actividades seleccionadas
        actividades_seleccionadas = self.obtener_actividades_seleccionadas()
        if not actividades_seleccionadas:
            self.mensaje_advertencia("Advertencia", "Selecciona al menos una actividad")
            return
        
        # 3. Confirmar con el usuario
        confirmacion = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Crear reporte '{nombre_reporte}' con {len(actividades_seleccionadas)} actividades?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion == QMessageBox.Yes:
            # Extraer solo los IDs de las actividades
            actividades_ids = [act['id'] for act in actividades_seleccionadas]
            
            # Llamar al controlador para guardar
            self.controller.Guardar_datos_reporte(nombre_reporte, actividades_ids)

    def mensaje_advertencia(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def mensaje_informativo(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)

    def actualizar_estilos(self):
        # Actualizar los estilo de la vista
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        
        # Aplicar fondo a la vista principal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar panel principal
        for widget in self.findChildren(QFrame):
            # Verificar si es el panel principal
            if widget.layout() and widget.layout().count() > 0:
                # Buscar el título "Convertir Reporte"
                for child in widget.findChildren(QLabel):
                    if child.text() == "Convertir Reporte":
                        # Este es el panel principal
                        widget.setStyleSheet(self.estilo["styles"]["panel"])
                        
                        # Actualizar sombra
                        if widget.graphicsEffect():
                            effect = widget.graphicsEffect()
                            if isinstance(effect, QGraphicsDropShadowEffect):
                                effect.setColor(QColor(colores.get("shadow", Qt.gray)))
                        break
        
        # Actualizar título
        for widget in self.findChildren(QLabel):
            if widget.text() == "Convertir Reporte":
                widget.setStyleSheet(self.estilo["styles"]["header"])
        
        # Actualizar tabla
        if hasattr(self, 'tabla_actividades'):
            # Actualizar estilo de la tabla completa
            self.tabla_actividades.setStyleSheet(self.estilo["styles"]["tabla"])
            
            # Actualizar checkboxes en la tabla
            for fila in range(self.tabla_actividades.rowCount()):
                checkbox = self.tabla_actividades.cellWidget(fila, 0)
                if checkbox and isinstance(checkbox, QCheckBox):
                    checkbox.setStyleSheet(self.estilo["styles"]["checkbox"])
            
            # Actualizar texto en las celdas
            for row in range(self.tabla_actividades.rowCount()):
                for col in range(1, self.tabla_actividades.columnCount()):
                    item = self.tabla_actividades.item(row, col)
                    if item:
                        # Establecer color de texto según el tema
                        item.setForeground(QColor(colores["text_primary"]))
        
        # Actualizar inputs
        for widget in self.findChildren((QLineEdit, QComboBox, QTextEdit)):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        # Actualizar botones
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(self.estilo["styles"]["boton"])
        