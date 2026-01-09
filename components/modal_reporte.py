# Ventana modal para exportar reporte a pptx
from PyQt5.QtWidgets import (QPushButton, QDialog, QLabel, QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout,
                             QMessageBox, QGroupBox, QGridLayout, QApplication)
from PyQt5.QtCore import Qt

COLOR_PRIMARIO = "#005a6e" 
COLOR_SECUNDARIO = "#e8f4f8"
COLOR_BOTON_HOVER = "#007d99"
COLOR_BOTON_ACTIVO = "#004a5c"
FONT_FAMILY = "Arial"

class Modal_exportar_Reporte(QDialog):
    def __init__(self, nombre_reporte, parent):
        super().__init__(parent=None)
        self.nombre_reporte = nombre_reporte
        self.meses_seleccionados = []
        
        # Variables para almacenar los datos que se retornarán
        self.datos_exportar = []
        self.trimestre_seleccionado = ""
        
        # Reajustando propiedades de la ventana
        self.setGeometry(600, 100, 400, 700)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.centrar_ventana()

        # Configurando layout principal o main
        self.Layout_main = QVBoxLayout()
        self.Layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.Layout_main)

        self.Interfaz_gui()

    def centrar_ventana(self):
        # 2. Obtener la geometría de la pantalla principal
        pantalla = QApplication.primaryScreen().availableGeometry()
        
        # 3. Obtener la geometría de esta ventana (su tamaño actual)
        ventana = self.frameGeometry()
        
        # 4. Mover el centro del rectángulo de la ventana al centro de la pantalla
        centro_pantalla = pantalla.center()
        ventana.moveCenter(centro_pantalla)
        
        # 5. Mover la esquina superior izquierda de la ventana real a la posición calculada
        self.move(ventana.topLeft())

    def Interfaz_gui(self):
        # Configurando layouts
        layout_interfaz = QVBoxLayout() 
        layout_interfaz.setContentsMargins(0, 0, 0, 10)
        self.Layout_main.addLayout(layout_interfaz)
        
        titulo = QLabel("Exportar Reporte")
        titulo.setStyleSheet(f"""
                             padding: 25px;
                             margin: 0;
                             background: {COLOR_PRIMARIO};
                             font-size: 22px;
                             color: white;
                             font-family: {FONT_FAMILY};
                             font-weight: bold;
                             border-top-left-radius: 8px;
                             border-top-right-radius: 8px;
                             letter-spacing: 1px;""")
        titulo.setMaximumHeight(70)
        titulo.setAlignment(Qt.AlignCenter)
        layout_interfaz.addWidget(titulo)

        # Contenedor principal con fondo
        contenedor_principal = QVBoxLayout()
        contenedor_principal.setContentsMargins(30, 15, 30, 15)
        contenedor_principal.setSpacing(15)
        
        layout_interfaz.addLayout(contenedor_principal)

        nombre_reporte = QLabel(f"Nombre: {self.nombre_reporte}")
        nombre_reporte.setStyleSheet(f"""
                                     font-size: 16px;
                                     padding: 12px;
                                     margin: 0;
                                     color: #333333;
                                     background-color: {COLOR_SECUNDARIO};
                                     font-family: {FONT_FAMILY};
                                     font-weight: 600;
                                     border-radius: 6px;
                                     border: 1px solid #d1e7ed;""")
        nombre_reporte.setMaximumHeight(40)
        nombre_reporte.setAlignment(Qt.AlignCenter)
        contenedor_principal.addWidget(nombre_reporte)

        # Selección de trimestre
        contenedor_principal.addWidget(QLabel("Seleccione Trimestre:"))
        self.lista_trimestre = QComboBox()
        self.lista_trimestre.setStyleSheet(f"""
            QComboBox {{
                padding: 12px;
                font-size: 14px;
                font-family: {FONT_FAMILY};
                color: #333333;
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 6px;
                selection-background-color: {COLOR_SECUNDARIO};
            }}
            QComboBox:hover {{
                border: 1px solid {COLOR_PRIMARIO};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {COLOR_PRIMARIO};
                width: 0;
                height: 0;
                margin-right: 10px;
            }}
        """)

        self.lista_trimestre.addItem("Seleccione un trimestre", [])
        self.lista_trimestre.addItem("Trimestre 1", ["Enero", "Febrero", "Marzo"])
        self.lista_trimestre.addItem("Trimestre 2", ["Abril", "Mayo", "Junio"])
        self.lista_trimestre.addItem("Trimestre 3", ["Julio", "Agosto", "Septiembre"])
        self.lista_trimestre.addItem("Trimestre 4", ["Octubre", "Noviembre", "Diciembre"])
        
        # Conectar el cambio de selección
        self.lista_trimestre.currentIndexChanged.connect(self.on_trimestre_seleccionado)
        
        contenedor_principal.addWidget(self.lista_trimestre)

        # Crear grupo para las ponderaciones
        self.grupo_ponderaciones = QGroupBox("Ponderaciones por Mes")
        self.grupo_ponderaciones.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-family: {FONT_FAMILY};
                font-weight: bold;
                color: {COLOR_PRIMARIO};
                border: 2px solid {COLOR_PRIMARIO};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        
        self.layout_ponderaciones = QVBoxLayout()
        self.grupo_ponderaciones.setLayout(self.layout_ponderaciones)
        self.grupo_ponderaciones.setEnabled(False)  # Inicialmente deshabilitado
        
        contenedor_principal.addWidget(self.grupo_ponderaciones)

        # Diccionario para almacenar los campos por mes
        self.campos_por_mes = {}

        # Area botones
        layout_botones = QHBoxLayout()
        contenedor_principal.addLayout(layout_botones)
        layout_botones.setContentsMargins(0, 20, 0, 10)
        layout_botones.setSpacing(10)
        
        boton_crear = QPushButton("Exportar Reporte")
        boton_crear.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARIO};
                color: white;
                font-family: {FONT_FAMILY};
                font-size: 15px;
                font-weight: bold;
                padding: 14px;
                border: none;
                border-radius: 6px;
                min-width: 160px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BOTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_BOTON_ACTIVO};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        boton_crear.clicked.connect(self.on_accept)
        boton_crear.setEnabled(False)  # Inicialmente deshabilitado
        self.boton_exportar = boton_crear  # Guardar referencia
        layout_botones.addWidget(boton_crear)

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARIO};
                color: white;
                font-family: {FONT_FAMILY};
                font-size: 15px;
                font-weight: bold;
                padding: 14px;
                border: none;
                border-radius: 6px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BOTON_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_BOTON_ACTIVO};
            }}
        """)
        boton_cancelar.clicked.connect(self.reject)
        layout_botones.addWidget(boton_cancelar)

    def on_trimestre_seleccionado(self, index):
        """Activa los campos de ponderación cuando se selecciona un trimestre"""
        if index > 0:  # No es la opción "Seleccione un trimestre"
            self.meses_seleccionados = self.lista_trimestre.currentData()
            self.trimestre_seleccionado = self.lista_trimestre.currentText()
            self.grupo_ponderaciones.setEnabled(True)
            self.crear_campos_ponderaciones()
            self.boton_exportar.setEnabled(True)
        else:
            self.meses_seleccionados = []
            self.trimestre_seleccionado = ""
            self.limpiar_campos_ponderaciones()
            self.grupo_ponderaciones.setEnabled(False)
            self.boton_exportar.setEnabled(False)

    def crear_campos_ponderaciones(self):
        """Crea los campos de entrada para las ponderaciones de cada mes"""
        self.limpiar_campos_ponderaciones()
        self.campos_por_mes = {}
        
        # Estilos para los textos
        estylos_texto = f"""
        margin: 8px 5px 3px 5px;
        font-size: 14px;
        font-family: {FONT_FAMILY};
        color: #444444;
        font-weight: 500;"""
        
        # Estilos para los input
        estylos_input = f"""
        QLineEdit {{
            padding: 10px;
            margin: 5px 5px 15px 5px;
            font-size: 14px;
            font-family: {FONT_FAMILY};
            color: #333333;
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 6px;
        }}
        QLineEdit:focus {{
            border: 2px solid {COLOR_PRIMARIO};
            background-color: #f8fbfc;
        }}
        QLineEdit:hover {{
            border: 1px solid {COLOR_PRIMARIO};
        }}
        """
        
        # Labels para las categorías
        self.categorias = [
            "Mantenimiento preventivo:",
            "Política mantenimiento:",
            "Manuales mantenimiento:",
            "Verificación cumplimiento:",
            "Asignación trabajo:"
        ]
        
        # Crear layout de grid para organizar mejor
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(10)
        grid_layout.setHorizontalSpacing(15)
        
        # Agregar encabezados de meses
        for col, mes in enumerate(self.meses_seleccionados):
            label_mes = QLabel(mes)
            label_mes.setStyleSheet(f"""
                font-weight: bold;
                color: {COLOR_PRIMARIO};
                font-size: 14px;
                padding: 5px;
                background-color: {COLOR_SECUNDARIO};
                border-radius: 4px;
                text-align: center;
            """)
            grid_layout.addWidget(label_mes, 0, col + 1, Qt.AlignCenter)
        
        # Agregar categorías y campos de entrada
        for row, categoria in enumerate(self.categorias):
            # Label de la categoría
            label_categoria = QLabel(categoria)
            label_categoria.setStyleSheet(estylos_texto)
            label_categoria.setWordWrap(True)
            grid_layout.addWidget(label_categoria, row + 1, 0)
            
            # Campos de entrada para cada mes
            campos_mes = []
            for col, mes in enumerate(self.meses_seleccionados):
                entrada = QLineEdit()
                entrada.setPlaceholderText("Ponderación")
                entrada.setStyleSheet(estylos_input)
                grid_layout.addWidget(entrada, row + 1, col + 1)
                campos_mes.append(entrada)
            
            self.campos_por_mes[categoria] = campos_mes
        
        self.layout_ponderaciones.addLayout(grid_layout)

    def limpiar_campos_ponderaciones(self):
        """Limpia todos los campos de ponderación existentes"""
        # Eliminar todos los widgets del layout
        while self.layout_ponderaciones.count():
            item = self.layout_ponderaciones.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.limpiar_layout(item.layout())
        
        self.campos_por_mes.clear()

    def limpiar_layout(self, layout):
        """Función auxiliar para limpiar un layout recursivamente"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.limpiar_layout(item.layout())

    def validar_campos(self):
        """Valida que todos los campos de ponderación estén completos"""
        if not self.campos_por_mes:
            return False, "Primero seleccione un trimestre"
        
        for categoria, campos in self.campos_por_mes.items():
            for i, campo in enumerate(campos):
                if not campo.text().strip():
                    mes = self.meses_seleccionados[i]
                    return False, f"Complete la ponderación para '{categoria}' en {mes}"
        
        # Validar que los valores sean numéricos (opcional)
        for categoria, campos in self.campos_por_mes.items():
            for i, campo in enumerate(campos):
                valor = campo.text().strip()
                if valor:  # Solo validar si no está vacío
                    try:
                        float(valor)  # Intentar convertir a número
                    except ValueError:
                        mes = self.meses_seleccionados[i]
                        return False, f"La ponderación para '{categoria}' en {mes} debe ser un número"
        
        return True, ""

    def obtener_lista_simple(self):
        """
        Retorna una lista simple donde cada elemento contiene:
        {
            'mes': 'Nombre del mes',
            'valores': ['valor1', 'valor2', 'valor3', 'valor4', 'valor5']
        }
        """
        if not self.campos_por_mes or not self.meses_seleccionados:
            return []
        
        lista_resultado = []
        
        # Para cada mes, recopilar todos sus valores
        for mes_index, mes in enumerate(self.meses_seleccionados):
            valores_mes = []
            
            # Para cada categoría, obtener el valor correspondiente a este mes
            for categoria in self.categorias:
                if categoria in self.campos_por_mes:
                    campos = self.campos_por_mes[categoria]
                    if mes_index < len(campos):
                        valor = campos[mes_index].text().strip()
                        valores_mes.append(valor)
            
            # Crear el diccionario para este mes
            item_mes = {
                'mes': mes,
                'valores': valores_mes
            }
            
            lista_resultado.append(item_mes)
        
        return lista_resultado

    def on_accept(self):
        """Maneja el evento de exportación"""
        # Validar campos
        valido, mensaje_error = self.validar_campos()
        
        if not valido:
            self.mensaje_advertencia("Error", mensaje_error)
            return
        
        # Obtener los datos en formato lista simple
        self.datos_exportar = self.obtener_lista_simple()
        
        # Mostrar mensaje de éxito y cerrar
        self.mensaje_informativo("Éxito", "Los datos están listos para exportar")
        self.accept()

    def obtener_datos_completos(self):
        """
        Método público para obtener todos los datos después de cerrar el diálogo.
        Retorna: (nombre_reporte, trimestre, lista_simple)
        """
        return {
            'nombre_reporte': self.nombre_reporte,
            'trimestre': self.trimestre_seleccionado,
            'meses': self.meses_seleccionados.copy(),
            'datos': self.datos_exportar.copy()
        }

    def mensaje_advertencia(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def mensaje_informativo(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)

    """
    # Ejemplo de lo que retorna:simple
[
    {
        'mes': 'Enero',
        'valores': ['10', '20', '30', '40', '50']  # 5 valores (uno por categoría)
    },
    {
        'mes': 'Febrero',
        'valores': ['11', '21', '31', '41', '51']
    },
    {
        'mes': 'Marzo',
        'valores': ['12', '22', '32', '42', '52']
    }
]
    """
    """
    # Ejemplo de lo que retorna:Completo
{
    'nombre_reporte': 'Reporte Mantenimiento',
    'trimestre': 'Trimestre 1',
    'meses': ['Enero', 'Febrero', 'Marzo'],
    'datos': [
        {'mes': 'Enero', 'valores': ['10', '20', '30', '40', '50']},
        {'mes': 'Febrero', 'valores': ['11', '21', '31', '41', '51']},
        {'mes': 'Marzo', 'valores': ['12', '22', '32', '42', '52']}
    ]
}
    """