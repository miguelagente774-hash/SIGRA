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

        # Contenedor para el Mensaje de error
        self.contenedor_error = QFrame()
        self.contenedor_error.setMinimumHeight(60)
        self.contenedor_error.setMaximumHeight(80)
        self.contenedor_error.setStyleSheet("background: transparent; border: none; margin: 5px 15px;")

        # Layout para el Mensaje de Error
        layout_error = QVBoxLayout(self.contenedor_error)
        layout_error.setContentsMargins(0, 0, 0, 0)
        layout_error.setSpacing(0)

        # Mensaje de error
        self.label_error = QLabel("")
        self.label_error.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_ERROR};
                font-family: {FONT_FAMILY};
                font-size: 12px;
                padding: 12px;
                margin: 0 15px 10px 15px;
                background-color: #fdeded;
                border: 1px solid {COLOR_ERROR}20;
                border-radius: 8px;
                font-weight: 500;
            }}
        """)
        self.label_error.setAlignment(Qt.AlignCenter)
        self.label_error.setVisible(False)
        self.label_error.setWordWrap(True)
        
        layout_error.addWidget(self.label_error)
        layout_registro.addWidget(self.contenedor_error)

        # Botón de login
        self.crear_boton_registro(layout_registro)
        
        # Espaciador mínimo al final para que no toque el borde
        layout_registro.addSpacing(10)
        
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
                color: #222;
                font-weight: normal;
                padding: 0;
                margin: 0 0 10px 0;
                border: none;
            }}
        """)
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

    def crear_campos_formulario(self, layout):
    # ==Campos del Formulario de Registro==
        self.label_preguntas = QLabel("Preguntas de Seguridad")
        self.label_preguntas.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin: 10px 0 5px 15px;")
        layout.addWidget(self.label_preguntas)

        # Contenedor para el Grid
        contenedor_grid = QFrame()
        contenedor_grid.setStyleSheet("margin: 0 15px; border: none;")
        contenedor_grid.setFixedHeight(120)
        
        grid_layout = QGridLayout(contenedor_grid)
        grid_layout.setContentsMargins(0, 5, 0, 20)
        grid_layout.setSpacing(10)

        # Establecer alturas minimas para las filas
        grid_layout.setRowMinimumHeight(0, 50)
        grid_layout.setRowMinimumHeight(1, 50)

        # Definir las preguntas
        preguntas_lista = [
            "¿Nombre de tu mascota?",
            "¿Ciudad de nacimiento?",
            "¿Nombre de tu abuela?",
            "¿Tu comida favorita?",
            "¿Tu película favorita?"
        ]

        # Crear los 3 Combos (Fila 0) y los 3 Inputs (Fila 1)
        self.combos_seguridad = []
        self.inputs_seguridad = []

        for i in range(3):
            combo = QComboBox()
            combo.addItems(preguntas_lista)
            combo.setCurrentIndex(i)
            combo.setStyleSheet(self.obtener_estilo_combo())
            combo.setMinimumHeight(45)
            grid_layout.addWidget(combo, 0, i)
            self.combos_seguridad.append(combo)

            input_respuesta = QLineEdit()
            input_respuesta.setPlaceholderText(f"Respuesta {i+1}")
            input_respuesta.setStyleSheet(self.obtener_estilo_input())
            input_respuesta.setMinimumHeight(45)
            grid_layout.addWidget(input_respuesta, 1, i)
            self.inputs_seguridad.append(input_respuesta)
        
        layout.addWidget(contenedor_grid)

        # ==Campos de Contraseñas: Label de Contraseña==
        self.label_pass = QLabel("Contraseña")
        self.label_pass.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin-left: 15px;")
        layout.addWidget(self.label_pass)
        
        # ==Contenedor para contraseña con botón DENTRO del input==
        self.contenedor_password = QFrame()
        self.contenedor_password.setStyleSheet("background: transparent; border: none; margin: 0 15px;")
        self.contenedor_password.setFixedHeight(45)
        
        # Crear un layout horizontal para el contenedor
        layout_password = QHBoxLayout(self.contenedor_password)
        layout_password.setContentsMargins(0, 0, 0, 0)
        layout_password.setSpacing(0)
        
        # Input de contraseña (ocupará el espacio disponible)
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setMinimumHeight(45)
        
        # Estilo para el input
        self.input_password.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 1.5px solid {COLOR_GRIS_BORDE};
                border-radius: 10px;
                padding: 14px 45px 14px 18px;
                font-size: 15px;
                font-family: {FONT_FAMILY};
                selection-background-color: {COLOR_PRIMARIO};
                color: {COLOR_TEXTO};
            }}
            QLineEdit:focus {{
                border: 1.5px solid {COLOR_PRIMARIO};
                background-color: {COLOR_BLANCO};
            }}
            QLineEdit:hover {{
                border: 1.5px solid {COLOR_SECUNDARIO};
            }}
        """)
        layout_password.addWidget(self.input_password)
        
        # Botón mostrar/ocultar (con tamaño fijo)
        self.btn_mostrar_pass = QPushButton("👁")
        self.btn_mostrar_pass.setCursor(Qt.PointingHandCursor)
        self.btn_mostrar_pass.setFixedSize(50, 50)
        self.btn_mostrar_pass.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-size: 20px;
                color: {COLOR_TEXTO};
                margin-left: -10px;  /* Margen negativo para superponerlo */
            }}
            QPushButton:hover {{
                color: {COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                color: {COLOR_PRIMARIO};
            }}
        """)
        self.btn_mostrar_pass.setCheckable(True)
        layout_password.addWidget(self.btn_mostrar_pass)
        
        layout.addWidget(self.contenedor_password)

        # ==Label de Confirmar Contraseña==
        self.label_confirm = QLabel("Confirmar Contraseña")
        self.label_confirm.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin-left: 15px;")
        layout.addWidget(self.label_confirm)

        # ==Contenedor para confirmar contraseña con botón DENTRO del input==
        self.contenedor_confirm = QFrame()
        self.contenedor_confirm.setStyleSheet("background: transparent; border: none; margin: 0 15px;")
        self.contenedor_confirm.setFixedHeight(45)
        
        # Crear un layout horizontal para el contenedor
        layout_confirm = QHBoxLayout(self.contenedor_confirm)
        layout_confirm.setContentsMargins(0, 0, 0, 0)
        layout_confirm.setSpacing(0)
        
        # Input de confirmar contraseña
        self.input_password_confirmation = QLineEdit()
        self.input_password_confirmation.setPlaceholderText("Confirme su contraseña")
        self.input_password_confirmation.setEchoMode(QLineEdit.Password)
        self.input_password_confirmation.setMinimumHeight(45)
        
        # Estilo para el input
        self.input_password_confirmation.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 1.5px solid {COLOR_GRIS_BORDE};
                border-radius: 10px;
                padding: 14px 45px 14px 18px;
                font-size: 15px;
                font-family: {FONT_FAMILY};
                selection-background-color: {COLOR_PRIMARIO};
                color: {COLOR_TEXTO};
            }}
            QLineEdit:focus {{
                border: 1.5px solid {COLOR_PRIMARIO};
                background-color: {COLOR_BLANCO};
            }}
            QLineEdit:hover {{
                border: 1.5px solid {COLOR_SECUNDARIO};
            }}
        """)
        layout_confirm.addWidget(self.input_password_confirmation)
        
        # Botón mostrar/ocultar (con tamaño fijo)
        self.btn_mostrar_confirm = QPushButton("👁")
        self.btn_mostrar_confirm.setCursor(Qt.PointingHandCursor)
        self.btn_mostrar_confirm.setFixedSize(50, 50)
        self.btn_mostrar_confirm.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-size: 20px;
                margin-left: -10px;
                color: {COLOR_TEXTO};
            }}
            QPushButton:hover {{
                color: {COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                color: {COLOR_PRIMARIO};
            }}
        """)
        self.btn_mostrar_confirm.setCheckable(True)
        layout_confirm.addWidget(self.btn_mostrar_confirm)
        
        layout.addWidget(self.contenedor_confirm)
        
    def crear_boton_registro(self, layout):
        # Crear el Botón para Validar el Registro
        self.boton_registro = QPushButton("Registrarse")
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
                padding: 12px;  /* Reducido padding */
                border-radius: 10px;
                border: none;
                margin: 0 15px 5px 15px;  /* Reducido margen superior */
            }}
            QPushButton:hover {{
                background-color: {COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_AZUL_HOVER};
                padding: 11px;
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
        padding: 8px 12px;
        background: {COLOR_BLANCO};
        color: {COLOR_TEXTO};
        min-height: 25px;
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
        QComboBox QAbstractItemView {{
            border: 1px solid {COLOR_GRIS_BORDE};
            border-radius: 5px;
            background: {COLOR_BLANCO};
            selection-background-color: {COLOR_PRIMARIO};
        }}
    """
        

    def obtener_estilo_combo_error(self):
            """Estilo para combobox en estado de error"""
            return f""" 
            QComboBox {{
                font-family: {FONT_FAMILY};
                font-size: {FONT_SIZE}px;
                border: 2px solid {COLOR_ERROR};
                border-radius: 10px;
                padding: 8px 12px;
                background: {COLOR_BLANCO};
                color: {COLOR_TEXTO};
                min-height: 25px;
            }}
            QComboBox:focus, QComboBox:hover {{
                border: 2px solid {COLOR_ERROR};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid {COLOR_ERROR};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid {COLOR_ERROR};
                border-radius: 5px;
                background: {COLOR_BLANCO};
                selection-background-color: {COLOR_ERROR}80;
            }}
            """