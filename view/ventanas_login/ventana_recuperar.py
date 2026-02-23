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
    recuperacion_exitosa = pyqtSignal()
    
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
        
        self.crear_panel_recuperar()
        
        # Acción para atajo de teclado
        self.recuperar_action = QAction("Recuperar", self)
        self.recuperar_action.setShortcut("Return")
        self.addAction(self.recuperar_action)
        
    def crear_panel_recuperar(self):
        # ==Crea el panel del formulario de recuperar con el botón al final==
        # Contenedor principal del Recuperar Contraseña
        self.contenedor_recuperar = QFrame()
        self.contenedor_recuperar.setFixedSize(800, 600)  # Aumentado para dar espacio fijo

        layout_recuperar = QVBoxLayout()
        layout_recuperar.setContentsMargins(0, 0, 0, 0)
        layout_recuperar.setSpacing(15)
        self.contenedor_recuperar.setLayout(layout_recuperar)
        
        # Estilo del contenedor
        self.contenedor_recuperar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BLANCO};
                border: none;
            }}
        """)
        
        # Sombra
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(30)
        sombra.setColor(QColor(0, 0, 0, 25))
        sombra.setOffset(0, 5)
        self.contenedor_recuperar.setGraphicsEffect(sombra)
        
        # Instanciar los métodos para el panel
        self.crear_encabezado_recuperar(layout_recuperar)
        self.crear_campos_recuperacion(layout_recuperar)
        
        # Contenedor fijo para los campos de contraseña (siempre presente, pero invisible)
        self.contenedor_password_fijo = QFrame()
        self.contenedor_password_fijo.setFixedHeight(150)  # Altura fija para los campos de contraseña
        self.contenedor_password_fijo.setStyleSheet("background: transparent; border: none;")
        
        layout_password_fijo = QVBoxLayout(self.contenedor_password_fijo)
        layout_password_fijo.setContentsMargins(0, 0, 0, 0)
        layout_password_fijo.setSpacing(10)
        
        # Crear campos de contraseña (siempre existen, pero ocultos inicialmente)
        self.crear_campos_password_con_botones(layout_password_fijo)
        
        layout_recuperar.addWidget(self.contenedor_password_fijo)
        
        # Contenedor para el Mensaje de Error
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
        layout_recuperar.addWidget(self.contenedor_error)

        # Botón de recuperar
        self.crear_boton_recuperar(layout_recuperar)
        
        # Espaciador mínimo al final
        layout_recuperar.addSpacing(10)
        
        self.layout_contenedor.addWidget(self.contenedor_recuperar)

    def crear_campos_password_con_botones(self, layout):
        """Crea los campos de contraseña con botones dentro (siempre existen)"""
        
        # Label Nueva Contraseña
        self.label_nueva_pass = QLabel("Nueva Contraseña")
        self.label_nueva_pass.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin-left: 15px;")
        layout.addWidget(self.label_nueva_pass)
        
        # Contenedor para nueva contraseña con botón
        contenedor_nueva = QFrame()
        contenedor_nueva.setStyleSheet("background: transparent; border: none; margin: 0 15px;")
        contenedor_nueva.setFixedHeight(45)
        
        layout_nueva = QHBoxLayout(contenedor_nueva)
        layout_nueva.setContentsMargins(0, 0, 0, 0)
        layout_nueva.setSpacing(0)
        
        # Input de nueva contraseña
        self.input_nueva_pass = QLineEdit()
        self.input_nueva_pass.setPlaceholderText("Ingrese su nueva contraseña")
        self.input_nueva_pass.setEchoMode(QLineEdit.Password)
        self.input_nueva_pass.setMinimumHeight(45)
        
        self.input_nueva_pass.setStyleSheet(f"""
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
        layout_nueva.addWidget(self.input_nueva_pass)
        
        # Botón mostrar/ocultar
        self.btn_mostrar_pass = QPushButton("👁")
        self.btn_mostrar_pass.setCursor(Qt.PointingHandCursor)
        self.btn_mostrar_pass.setFixedSize(50, 50)
        self.btn_mostrar_pass.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-size: 20px;
                color: {COLOR_TEXTO};
                margin-left: -10px;
            }}
            QPushButton:hover {{
                color: {COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                color: {COLOR_PRIMARIO};
            }}
        """)
        self.btn_mostrar_pass.setCheckable(True)
        layout_nueva.addWidget(self.btn_mostrar_pass)
        
        layout.addWidget(contenedor_nueva)

        # Label Confirmar Contraseña
        self.label_conf_pass = QLabel("Confirmar Contraseña")
        self.label_conf_pass.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin-left: 15px;")
        layout.addWidget(self.label_conf_pass)

        # Contenedor para confirmar contraseña con botón
        contenedor_confirm = QFrame()
        contenedor_confirm.setStyleSheet("background: transparent; border: none; margin: 0 15px;")
        contenedor_confirm.setFixedHeight(45)
        
        layout_confirm = QHBoxLayout(contenedor_confirm)
        layout_confirm.setContentsMargins(0, 0, 0, 0)
        layout_confirm.setSpacing(0)
        
        # Input de confirmar contraseña
        self.input_conf_pass = QLineEdit()
        self.input_conf_pass.setPlaceholderText("Confirme su nueva contraseña")
        self.input_conf_pass.setEchoMode(QLineEdit.Password)
        self.input_conf_pass.setMinimumHeight(45)
        
        self.input_conf_pass.setStyleSheet(f"""
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
        layout_confirm.addWidget(self.input_conf_pass)
        
        # Botón mostrar/ocultar
        self.btn_mostrar_confirm = QPushButton("👁")
        self.btn_mostrar_confirm.setCursor(Qt.PointingHandCursor)
        self.btn_mostrar_confirm.setFixedSize(50, 50)
        self.btn_mostrar_confirm.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-size: 20px;
                color: {COLOR_TEXTO};
                margin-left: -10px;
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
        
        layout.addWidget(contenedor_confirm)
        
    def crear_encabezado_recuperar(self, layout):
        # Crea el encabezado del panel de Recuperar
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
        
        # Subtítulo
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
        self.combos_seguridad = []  # LISTA para almacenar los 3 combos
        self.inputs_seguridad = []  # LISTA para las 3 respuestas
        
        for i in range(3):
            combo = QComboBox()
            combo.setStyleSheet(self.obtener_estilo_combo())
            combo.setMinimumHeight(45)
            layout.addWidget(combo, 0, i)
            self.combos_seguridad.append(combo)
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Respuesta {i+1}")
            line_edit.setStyleSheet(self.obtener_estilo_input())
            line_edit.setMinimumHeight(45)
            layout.addWidget(line_edit, 1, i)
            self.inputs_seguridad.append(line_edit)

    def crear_campos_recuperacion(self, layout):
        # Campos de Formulario para la recuperación
        self.label_preguntas = QLabel("Preguntas de Seguridad")
        self.label_preguntas.setStyleSheet(f"color: {COLOR_TEXTO}; font-weight: bold; margin: 10px 0 5px 15px;")
        layout.addWidget(self.label_preguntas)

        # Contenedor para el GridLayout con altura fija
        contenedor_grid = QFrame()
        contenedor_grid.setStyleSheet("margin: 0 15px; border: none;")
        contenedor_grid.setFixedHeight(120)  # Altura fija para el grid
        
        grid_layout = QGridLayout(contenedor_grid)
        grid_layout.setContentsMargins(0, 5, 0, 20)
        grid_layout.setSpacing(10)
        
        # Alturas mínimas fijas
        grid_layout.setRowMinimumHeight(0, 50)
        grid_layout.setRowMinimumHeight(1, 50)
        
        # Aquí el usuario debe responder las 3 preguntas
        self.crear_campos_seguridad(grid_layout)

        layout.addWidget(contenedor_grid)

    def crear_boton_recuperar(self, layout):
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
                padding: 12px;
                border-radius: 10px;
                border: none;
                margin: 0 15px 5px 15px;
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
        self.boton_recuperar.setGraphicsEffect(sombra_boton)
        
        layout.addWidget(self.boton_recuperar)
        
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