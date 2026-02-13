from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QFrame, QAction,
                            QLabel, QGraphicsDropShadowEffect, QSpacerItem,
                            QMessageBox, QLineEdit, QPushButton, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
import sys

# Paleta de colores mejorada
FONT_FAMILY = "Arial"
FONT_SIZE = "15"
COLOR_PRIMARIO = "#005a6e"
COLOR_AZUL_HOVER = "#00485a"
COLOR_SECUNDARIO = "#007a94"
COLOR_BLANCO = "#FFFFFF"
COLOR_GRIS_CLARO = "#f8f9fa"
COLOR_GRIS_BORDE = "#dee2e6"
COLOR_TEXTO = "#2c3e50"
COLOR_ERROR = "#e74c3c"
COLOR_EXITO = "#27ae60"
COLOR_SOMBRA = "#e0e0e0"

# Clase: Ventana Recuperar
class Ventana_recuperar(QFrame):
    recuperacion_exitoso = pyqtSignal()  # Modificado para enviar el nombre de usuario
    
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
        
    def inicializar_ui(self):
        # Configuración Inicial del Interfaz
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLOR_BLANCO};
                border-radius: 20px;
            }}
        """)
        
        # Layout principal
        self.layout_main = QVBoxLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)
        
        # Contenedor centrado
        contenedor_centro = QFrame()
        contenedor_centro.setStyleSheet("background: transparent;")
        layout_centro = QVBoxLayout()
        layout_centro.setContentsMargins(0, 0, 0, 0)
        
        self.contenedor_main = QFrame()
        self.contenedor_main.setStyleSheet("background: transparent;")
        
        self.layout_contenedor = QHBoxLayout()
        self.layout_contenedor.setContentsMargins(0, 0, 0, 0)
        self.contenedor_main.setLayout(self.layout_contenedor)
        
        layout_centro.addWidget(self.contenedor_main, alignment=Qt.AlignCenter)
        layout_centro.addStretch()
        contenedor_centro.setLayout(layout_centro)
        
        self.layout_main.addWidget(contenedor_centro, 1)
        
        self.crear_panel_registro()
        
        # Acción para atajo de teclado
        self.registro_action = QAction("Recuperar", self)
        self.registro_action.setShortcut("Return")
        self.addAction(self.registro_action)
        
    def crear_panel_registro(self):
        # ==Crea el panel del formulario de recuperar con el botón al final==
        # Contenedor principal del Recuperar Contraseña
        self.contenedor_registro = QFrame()
        self.contenedor_registro.setFixedSize(800, 600)

        layout_registro = QVBoxLayout()
        layout_registro.setContentsMargins(0, 0, 0, 0)
        layout_registro.setSpacing(15)
        self.contenedor_registro.setLayout(layout_registro)
        
        # Estilo del contenedor
        self.contenedor_registro.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BLANCO};
                border: none;
            }},
            QLabel {{
            border: none;
            background: transparent:
            }}
        """)
        
        # Sombra
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(30)
        sombra.setColor(QColor(0, 0, 0, 25))
        sombra.setOffset(0, 5)
        self.contenedor_registro.setGraphicsEffect(sombra)
        
        # 1. Elementos superiores
        self.crear_encabezado_registro(layout_registro)
        self.crear_campos_recuperacion(layout_registro)
        self.crear_elementos_ocultos(layout_registro)
        
        # 2. EL STRETCH: Empuja todo lo anterior hacia arriba
        layout_registro.addStretch(1)
        
        # 3. Mensaje de error (encima del botón)
        self.label_error = QLabel("")
        self.label_error.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_ERROR};
                font-family: {FONT_FAMILY};
                font-size: 13px;
                padding: 12px;
                margin: 0 15px 10px 15px;
                background-color: #fdeded;
                border: 1px solid {COLOR_ERROR}20;
                border-radius: 8px;
                font-weight: 500;
            }}
        """)
        self.setMinimumHeight(25)
        self.label_error.setAlignment(Qt.AlignCenter)
        self.label_error.setVisible(False)
        layout_registro.addWidget(self.label_error)

        # 4. Botón de recuperar
        self.crear_boton_registro(layout_registro)
        
        # 5. Espaciador mínimo al final para que no toque el borde redondeado
        layout_registro.addSpacing(20)
        
        self.layout_contenedor.addWidget(self.contenedor_registro)

        
    def crear_encabezado_registro(self, layout):
        # Crea el encabezado del panel de Recuperar==
        titulo = QLabel("Recuperar Contraseña")
        titulo.setStyleSheet(f"""
            QLabel {{
                background: #005a6e;
                font-family: {FONT_FAMILY};
                font-size: 32px;
                color: white;
                font-weight: 600;
                padding: 15px 0;
                margin: 0 0 10px 0;
                border: none;
                border-bottom-right-radius: 0;
                border-bottom-left-radius: 0;
            }}
        """)
        titulo.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(titulo)
        
        # Subtítulo opcional para más elegancia
        subtitulo = QLabel("Recupere la Contraseña Respondiendo a las Preguntas de Seguridad")
        subtitulo.setStyleSheet(f"""
            QLabel {{
                background: transparent;
                font-family: {FONT_FAMILY};
                font-size: 18px;
                color: #7f8c8d;
                font-weight: normal;
                padding: 0;
                margin: 0 0 10px 0;
                border: none;
            }}
        """)
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

    def crear_campos_seguridad(self, layout):
        self.combos_seguridad = [] # LISTA para almacenar los 3 combos
        self.inputs_seguridad = [] # LISTA para las 3 respuestas
        
        for i in range(3):
            combo = QComboBox()
            combo.setStyleSheet(self.obtener_estilo_combo())
            layout.addWidget(combo, 0, i)
            self.combos_seguridad.append(combo) # Agregamos a la lista
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Respuesta {i+1}")
            line_edit.setStyleSheet(self.obtener_estilo_input())
            layout.addWidget(line_edit, 1, i)
            self.inputs_seguridad.append(line_edit) # Agregamos a la lista

    def crear_campos_recuperacion(self, layout):
        # Campos de Formulario para la recuperación
        self.label_preguntas = QLabel("Preguntas de Seguridad")
        self.label_preguntas.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin: 10px 0 0 15px;")
        layout.addWidget(self.label_preguntas)

        # Contenedor para el GridLayout
        contenedor_grid = QFrame()
        contenedor_grid.setStyleSheet("margin: 0 15px; border: none;")
        grid_layout = QGridLayout(contenedor_grid)
        grid_layout.setContentsMargins(0, 5, 0, 0)
        grid_layout.setSpacing(10)

        
        # Aquí el usuario debe responder las 3 preguntas
        self.crear_campos_seguridad(grid_layout)

        layout.addWidget(contenedor_grid)

    def crear_boton_registro(self, layout):
        # =Crear el Botón para Recuperar la Contraseña=
        self.boton_recuperar = QPushButton("Validar Preguntas")
        self.boton_recuperar.setCursor(Qt.PointingHandCursor)
        
        # Estilo más moderno con transiciones
        self.boton_recuperar.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARIO};
                color: {COLOR_BLANCO};
                font-family: {FONT_FAMILY};
                font-weight: 600;
                font-size: 16px;
                min-height: 18px;
                padding: 16px;
                border-radius: 10px;
                border: none;
                margin: 25px 15px 10px 15px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_AZUL_HOVER};
                padding: 15px;
            }}
            QPushButton:focus{{
             outline: none;
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
                color: #7f8c8d;
            }}
        """)
        
        # Añadir efecto de sombra al botón
        sombra_boton = QGraphicsDropShadowEffect()
        sombra_boton.setBlurRadius(15)
        sombra_boton.setColor(QColor(0, 90, 110, 40))
        sombra_boton.setOffset(0, 4)
        self.boton_recuperar.setGraphicsEffect(sombra_boton)
        
        layout.addWidget(self.boton_recuperar)


    def crear_elementos_ocultos(self, layout):
        # Labels y Edits de Contraseña
        self.label_nueva_pass = QLabel("Nueva Contraseña:")
        self.input_nueva_pass = QLineEdit()
        self.input_nueva_pass.setEchoMode(QLineEdit.Password)
        
        self.label_conf_pass = QLabel("Confirmar Contraseña:")
        self.input_conf_pass = QLineEdit()
        self.input_conf_pass.setEchoMode(QLineEdit.Password)

        # Aplicar estilos y ocultar
        elementos = [self.label_nueva_pass, self.input_nueva_pass, 
                     self.label_conf_pass, self.input_conf_pass]
        
        for el in elementos:
            el.setVisible(False)
            if isinstance(el, QLineEdit):
                el.setStyleSheet(self.obtener_estilo_input())
            layout.addWidget(el)

    def toggle_campos_password(self, mostrar=True):
        self.label_nueva_pass.setVisible(mostrar)
        self.input_nueva_pass.setVisible(mostrar)
        self.label_conf_pass.setVisible(mostrar)
        self.input_conf_pass.setVisible(mostrar)
        # Deshabilitar edición de preguntas una vez validadas
        for combo in self.combos_seguridad: combo.setEnabled(False)
        for inp in self.inputs_seguridad: inp.setEnabled(False)

        
    def obtener_estilo_input(self, error=False):
        # Devuelve el estilo para los inputs
        estilo_base = f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 1.5px solid {'#e74c3c' if error else COLOR_GRIS_BORDE};
                border-radius: 10px;
                padding: 14px 18px;
                font-size: 15px;
                font-family: {FONT_FAMILY};
                margin: 0 15px;
                selection-background-color: {COLOR_PRIMARIO};
                color: {COLOR_TEXTO};
            }}
            QLineEdit:focus {{
                border: 1.5px solid {'#e74c3c' if error else COLOR_PRIMARIO};
                background-color: {COLOR_BLANCO};
            }}
            QLineEdit:hover {{
                border: 1.5px solid {'#e74c3c' if error else COLOR_SECUNDARIO};
            }}
        """
        return estilo_base

    def obtener_estilo_combo(self):
        return f""" 
        QComboBox {{
            font-family: {FONT_FAMILY};
            font-size: {FONT_SIZE}px;
            border: 1.5px solid {COLOR_GRIS_BORDE};
            border-radius: 10px;
            padding: 20px 15px;
            background: {COLOR_BLANCO};
            color: {COLOR_TEXTO};
        }}
        QComboBox:focus, QComboBox:hover {{
            border: 2px solid {COLOR_PRIMARIO};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        QComboBox::down-arrow {{
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 8px solid {COLOR_PRIMARIO};
            margin-right: 10px;
        }}
    """
        

    def obtener_datos_seguridad(self):
        # Retorna una lista de diccionarios con la pregunta y respuesta de cada campo.
        
        datos = []
        for i in range(3):
            pregunta = self.combos_seguridad[i].currentText()
            respuesta = self.inputs_seguridad[i].text().strip()
            datos.append({
                "pregunta": pregunta,
                "respuesta": respuesta
            })
        return datos
