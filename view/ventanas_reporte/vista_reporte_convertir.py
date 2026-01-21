from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView,
                             QCheckBox, QMessageBox, QLineEdit, QTextEdit, QComboBox, QDateEdit)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from comunicador import Comunicador_global
from datetime import datetime
from components.app_style import estilo_app

FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"

class Ventana_convertir_reporte(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.estilo = estilo_app.obtener_estilo_completo()
        self.controller = controller
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        estilo_app.registrar_vista(self)
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)        

        self.Panel_reporte()
        self.cargar_datos_tabla()
        #actulizar tabla cada vez que se agraga una nueva
        Comunicador_global.actividad_agregada.connect(self.cargar_datos_tabla)


    def Panel_reporte(self):
        # Configurando los layouts
        Panel_layout = QVBoxLayout()

        Panel_reporte = QFrame()
        Panel_layout.setContentsMargins(0, 0, 0, 0)
        Panel_layout.setSpacing(0)
        Panel_reporte.setStyleSheet("""
                                    background: #f5f5f5; 
                                    margin: 20px 20px 20px 25px;
                                    border-radius: 30px;
                                    padding: 0;
                                    """)
        Panel_reporte.setLayout(Panel_layout)

        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setColor(Qt.gray)
        sombra.setOffset(2, 2)

        Panel_reporte.setGraphicsEffect(sombra)

        titulo = QLabel("Convertir Reporte")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignLeft)
        titulo.setMaximumHeight(70)
        
        Panel_layout.addWidget(titulo, alignment=Qt.AlignTop)
        
        # Crear contenedor para controles de búsqueda
        controles_layout = QHBoxLayout()
        
        # Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar actividades por título o ID...")
        self.campo_busqueda.setStyleSheet(self.estilo["styles"]["input"])
        self.campo_busqueda.textChanged.connect(self.filtrar_actividades)
        
        controles_layout.addWidget(self.campo_busqueda)
        
        Panel_layout.addLayout(controles_layout)
        
        # Crear tabla de actividades
        self.crear_tabla_actividades(Panel_layout)
        
        # Crear botones de acción
        self.crear_botones_accion(Panel_layout)

        self.layout_main.addWidget(Panel_reporte)
    
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

        header.setStyleSheet("margin: 0; padding: 0;")
        
        # Configurar altura del header y tamaño mínimo
        header.setMinimumSectionSize(60)  # Tamaño mínimo para columnas
        header.setDefaultSectionSize(100)  # Tamaño por defecto
        header.setFixedHeight(70)  # Altura fija del header
        
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
                    
                    # Crear separador con nombre del mes
                    elemento_separador = QTableWidgetItem(f"  {nombre_mes}")
                    elemento_separador.setBackground(QColor(200, 220, 240))  # Azul claro
                    
                    # Hacer el texto en negrita
                    fuente = QFont()
                    fuente.setBold(True)
                    elemento_separador.setFont(fuente)
                    
                    # Centrar el texto
                    elemento_separador.setTextAlignment(Qt.AlignCenter)
                    
                    # Deshabilitar edición del separador
                    elemento_separador.setFlags(elemento_separador.flags() & ~Qt.ItemIsEditable)
                    
                    # Colocar en la columna de título (columna 2)
                    self.tabla_actividades.setItem(numero_fila, 2, elemento_separador)
                    
                    # Unir celdas para el separador (columnas 2, 3)
                    self.tabla_actividades.setSpan(numero_fila, 2, 1, 2)
                    
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
            self.tabla_actividades.setItem(numero_fila, 1, id_item)
            
            # Título (columna 2)
            titulo_item = QTableWidgetItem(actividad[1])
            titulo_item.setFlags(titulo_item.flags() & ~Qt.ItemIsEditable)
            self.tabla_actividades.setItem(numero_fila, 2, titulo_item)
            
            # Fecha (columna 3)
            fecha_item = QTableWidgetItem(actividad[2])
            fecha_item.setTextAlignment(Qt.AlignCenter)
            fecha_item.setFlags(fecha_item.flags() & ~Qt.ItemIsEditable)
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
                
                print("Id:",id_actividad,"Titulo:", titulo,"Fecha:",fecha)
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