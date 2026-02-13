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

# Clase: Ventana Login
class Ventana_setup(QFrame):
    registro_exitoso = pyqtSignal()  # Modificado para enviar el nombre de usuario
    
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
        self.registro_action = QAction("Login", self)
        self.registro_action.setShortcut("Return")
        self.addAction(self.registro_action)
        
    def crear_panel_registro(self):
        # ==Crea el panel del formulario de login con el botón al final==
        # Contenedor principal del login
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
        
        # Instanciar los métodos para el panel
        self.crear_encabezado_registro(layout_registro)
        self.crear_campos_formulario(layout_registro)
        
        # El Strectch para ajustar
        layout_registro.addStretch(1)
        
        # Mensaje de error
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

        # 4. Botón de login (al final)
        self.crear_boton_registro(layout_registro)
        
        # 5. Espaciador mínimo al final para que no toque el borde redondeado
        layout_registro.addSpacing(20)
        
        self.layout_contenedor.addWidget(self.contenedor_registro)

        
    def crear_encabezado_registro(self, layout):
        # Crea el encabezado del panel de login==
        titulo = QLabel("Bienvenido")
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
        subtitulo = QLabel("Registrese llenando los campos")
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

    def crear_campos_formulario(self, layout):
        # Campos del Formulario de Registro
        self.label_preguntas = QLabel("Preguntas de Seguridad")
        self.label_preguntas.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin: 10px 0 0 15px;")
        layout.addWidget(self.label_preguntas)

        # Contenedor para el Grid
        contenedor_grid = QFrame()
        contenedor_grid.setStyleSheet("margin: 0 15px; border: none;")
        grid_layout = QGridLayout(contenedor_grid)
        grid_layout.setContentsMargins(0, 5, 0, 0)
        grid_layout.setSpacing(10)

        # Definir las preguntas
        preguntas_lista = [
            "¿Nombre de tu mascota?",
            "¿Ciudad de nacimiento?",
            "¿Nombre de tu abuela?",
            
        ]

        # Crear los 3 Combos (Fila 0) y los 3 Inputs (Fila 1)
        self.combos_seguridad = []
        self.inputs_seguridad = []

        for i in range(3):
            # ComboBox
            combo = QComboBox()
            combo.addItems(preguntas_lista)
            combo.setCurrentIndex(i) # Para que no sean iguales por defecto
            combo.setStyleSheet(self.obtener_estilo_combo())
            grid_layout.addWidget(combo, 0, i) # Fila 0, Columna i
            self.combos_seguridad.append(combo)

            # QLine Edit para las Respuestas
            input_respuesta = QLineEdit()
            input_respuesta.setPlaceholderText(f"Respuesta {i+1}")
            input_respuesta.setStyleSheet(self.obtener_estilo_input())
            grid_layout.addWidget(input_respuesta, 1, i) # Fila 1, Columna i
            self.inputs_seguridad.append(input_respuesta)
        

        layout.addWidget(contenedor_grid)

        # ==Campos de Contraseñas: Label de Contraseña==
        self.label_pass = QLabel("Contraseña")
        self.label_pass.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin-left: 15px;")
        layout.addWidget(self.label_pass)
        
        # ==Campos de Contraseñas: Input de Contraseña==
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet(self.obtener_estilo_input())
        layout.addWidget(self.input_password)

        # ==Campos de Contraseñas: Label de Confirmar Contraseña==
        self.label_confirm = QLabel("Confirmar Contraseña")
        self.label_confirm.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin-left: 15px;")
        layout.addWidget(self.label_confirm)

        # ==Campos de Contraseñas: Input de Confirmar Contraseña==
        self.input_password_confirmation = QLineEdit()
        self.input_password_confirmation.setPlaceholderText("Confirme su contraseña")
        self.input_password_confirmation.setEchoMode(QLineEdit.Password)
        self.input_password_confirmation.setStyleSheet(self.obtener_estilo_input())
        layout.addWidget(self.input_password_confirmation)
        
    def crear_boton_registro(self, layout):
        """Crea el botón de inicio de sesión"""
        self.boton_registro = QPushButton("Crear Usuario")
        self.boton_registro.setCursor(Qt.PointingHandCursor)
        
        # Estilo más moderno con transiciones
        self.boton_registro.setStyleSheet(f"""
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
        self.boton_registro.setGraphicsEffect(sombra_boton)
        
        layout.addWidget(self.boton_registro)
        
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
            padding: 10px 15px;
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
            /* Dibujamos una flecha con CSS puro */
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 8px solid {COLOR_PRIMARIO};
            margin-right: 10px;
        }}
    """
        

