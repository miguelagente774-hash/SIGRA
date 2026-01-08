import sys
from PyQt5.QtWidgets import (
    QApplication, QFrame, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMainWindow, QLabel,
    QGraphicsDropShadowEffect, QLineEdit, QComboBox, QSizePolicy, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Definición de la familia de fuente y colores
FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"

BTN_STYLE = """
        QPushButton{
        background: #005a6e;
        color: White;
        font-weight: bold;
        font-size: 18px;
        padding: 15px;
        border-radius: 15px;
        text-align: left;
        border: none;
        }  
        QPushButton:hover{
        background: #007a94;
        }    
        QPushButton:pressed{
        background: #00485a;
        }"""

# --- CLASE: Ventana_Consulta (Contenido Principal) ---

class Ventana_consulta(QFrame):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        
        # Inicialización de widgets
        self.tabla = QTableWidget()
        self.campo_busqueda = QLineEdit()
        self.combo_ordenacion = QComboBox()
        self.layout_principal = QVBoxLayout(self)

        self._configurar_interfaz()
        self._conectar_senales()
    
    def _configurar_interfaz(self):
        """Configura el estilo base, layout principal y los subcomponentes."""
        self.setStyleSheet("background-color: white;")
        
        self.layout_principal.setContentsMargins(40, 20, 40, 20)
        self.layout_principal.setSpacing(0)
        
        self._configurar_combo_ordenacion()
        self._configurar_tabla()
        self._crear_panel_consulta_centrado()

    def _configurar_combo_ordenacion(self):
        """Configura los ítems y el estilo inicial del QComboBox."""
        self.combo_ordenacion.addItem("Ascendente")
        self.combo_ordenacion.addItem("Descendente")
        self.combo_ordenacion.setFixedHeight(40)
        self.combo_ordenacion.setMinimumWidth(120)
        self.combo_ordenacion.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.combo_ordenacion.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0; border: 1px solid #ccc;
                border-radius: 5px; padding: 1px 10px 1px 3px;
            }
            QComboBox::drop-down { border: 0px; }
        """)
        
    def _configurar_tabla(self):
        """Configura los encabezados y el estilo de la tabla."""
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels([ "ID", "Titulo", "Fecha" ])
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(70) # Modificar altura de celdas
        
        cabecera = self.tabla.horizontalHeader()
        cabecera.setStyleSheet("""
            QHeaderView::section {
                background-color: #f0f0f0; padding: 8px;
                border: 2px solid #ddd; font-weight: bold;
            }
        """)
        cabecera.setSectionResizeMode(QHeaderView.Stretch)
        cabecera.setStretchLastSection(False)

        self.actulizar_tabla()
        
        
    def actulizar_tabla(self):
        self.datos_prueba = self.controlador.Obtener_reportes()
        self._cargar_datos_en_tabla(self.datos_prueba)

    def _conectar_senales(self):
        """Conecta las señales de los widgets a sus métodos."""
        self.campo_busqueda.textChanged.connect(self._aplicar_filtro)
        self.combo_ordenacion.currentIndexChanged.connect(self._aplicar_filtro)
        
    # ESTRUCTURA DEL PANEL
    
    def _crear_panel_consulta_centrado(self):
        marco_central = QFrame()
        layout_contenedor = QVBoxLayout(marco_central)
        layout_contenedor.setContentsMargins(20, 20, 20, 20)
        layout_contenedor.setSpacing(0)
        
        panel_consulta = QFrame()
        panel_consulta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        panel_consulta.setMinimumSize(700, 450)
        
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25); sombra.setColor(Qt.gray)
        sombra.setOffset(2, 2)
        panel_consulta.setGraphicsEffect(sombra)

        layout_panel = QVBoxLayout(panel_consulta)
        layout_panel.setContentsMargins(0, 0, 0, 0); layout_panel.setSpacing(0)
        
        # Título Consulta
        titulo = QLabel("Consulta")
        titulo.setStyleSheet(f"""
            background: {COLOR_PRIMARIO}; font-family: {FONT_FAMILY};
            font-size: 28px; color: white; font-weight: bold;
            padding: 15px 20px; border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        """)
        titulo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        titulo.setMaximumHeight(60)
        layout_panel.addWidget(titulo, alignment = Qt.AlignTop)
        
        # Área de Contenido (Buscador, Tabla, Botones)
        area_contenido = QFrame()
        area_contenido.setStyleSheet("background: white; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;")
        layout_contenido = QVBoxLayout(area_contenido)
        layout_contenido.setContentsMargins(20, 5, 20, 5)
        layout_contenido.setSpacing(10)
        
        # Buscador y Ordenación
        layout_buscador_ordenacion = QHBoxLayout()
        layout_buscador_ordenacion.setContentsMargins(0, 0, 0, 0); layout_buscador_ordenacion.setSpacing(10)
        
        self.campo_busqueda.setPlaceholderText("Buscar por ID o Título...")
        self.campo_busqueda.setMaximumHeight(60)
        self.campo_busqueda.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.campo_busqueda.setStyleSheet(f"""
            QLineEdit {{ padding: 10px; border: 1px solid #ccc;
                         border-radius: 3px; margin: 10px;}}
            QLineEdit:hover, QLineEdit:focus {{ border: 1px solid {COLOR_AZUL_HOVER};
                                            }}
        """)
        
        etiqueta_ordenar = QLabel("Buscar de manera")
        etiqueta_ordenar.setFixedHeight(30)
        etiqueta_ordenar.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        layout_buscador_ordenacion.addWidget(self.campo_busqueda)
        layout_buscador_ordenacion.addWidget(etiqueta_ordenar)
        layout_buscador_ordenacion.addWidget(self.combo_ordenacion)
        
        layout_contenido.addLayout(layout_buscador_ordenacion)
        
        # Tabla y botones
        layout_contenido.addWidget(self.tabla)
        marco_botones_accion = self._crear_botones_accion()
        layout_contenido.addWidget(marco_botones_accion)
        
        layout_panel.addWidget(area_contenido)
        layout_contenedor.addWidget(panel_consulta)
        self.layout_principal.addWidget(marco_central)

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
        
        for indice_fila, datos_fila in enumerate(datos):
            for indice_columna, item in enumerate(datos_fila):
                item_tabla = QTableWidgetItem(str(item))
                # No se aplica padding por CSS al ítem, se usa el setDefaultSectionSize de la fila
                # para el espacio vertical.
                
                if indice_columna == 0 or indice_columna == 1 or indice_columna == 2:
                    item_tabla.setTextAlignment(Qt.AlignCenter)
                self.tabla.setItem(indice_fila, indice_columna, item_tabla)
                
        #if len(datos) > 0:
        #    self.tabla.selectRow(0)

    def Eliminar_reporte(self):
        id_reporte = self.Obtener_reporte_seleccionado()
        self.controlador.Eliminar_reporte(id_reporte)

    def Obtener_reporte_seleccionado(self):
        #fila seleccionada
        fila_seleccionda = self.tabla.currentRow()
        print(fila_seleccionda)
        if fila_seleccionda >= 0:
            id_reporte = self.tabla.item(fila_seleccionda, 0).text()
        else:
            id_reporte = None

        return id_reporte
            
    # MÉTODOS AUXILIARES Y DE BOTONES
    def _crear_botones_accion(self):
        marco_botones = QFrame()
        layout_botones = QHBoxLayout(marco_botones)
        layout_botones.setContentsMargins(0, 20, 0, 20)
        layout_botones.setSpacing(60)

        def crear_boton(texto):
            boton = QPushButton(texto)
            boton.setFixedSize(450, 50)
            # Estilo de botón
            boton.setStyleSheet(BTN_STYLE)
            return boton

        boton_excel = crear_boton("Excel-Reporte")
        boton_pptx = crear_boton("PTTX-Reporte")
        
        boton_eliminar = crear_boton("Eliminar")
        boton_eliminar.clicked.connect(self.Eliminar_reporte)
        
        layout_botones.addWidget(boton_excel)
        layout_botones.addWidget(boton_pptx)
        layout_botones.addWidget(boton_eliminar)
        
        return marco_botones

    def mensaje_advertencia(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def mensaje_informativo(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)