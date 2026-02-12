from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QFrame, QAction,
                            QLabel, QGraphicsDropShadowEffect, QSpacerItem,
                            QSizePolicy, QLineEdit, QPushButton, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QColor
import sys

# Paleta de colores mejorada
FONT_FAMILY = "Arial"
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
class Ventana_login(QFrame):
    login_exitoso = pyqtSignal()  # Modificado para enviar el nombre de usuario
    
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
        self.conectar_eventos()
        
    def inicializar_ui(self):
        """Configuración inicial de la interfaz de usuario"""
        self.setMinimumSize(900, 650)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {COLOR_GRIS_CLARO},
                    stop: 1 #f0f4f8
                );
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
        layout_centro.addStretch()
        
        self.contenedor_main = QFrame()
        self.contenedor_main.setStyleSheet("background: transparent;")
        
        self.layout_contenedor = QHBoxLayout()
        self.layout_contenedor.setContentsMargins(0, 0, 0, 0)
        self.layout_contenedor.addStretch()
        self.contenedor_main.setLayout(self.layout_contenedor)
        
        layout_centro.addWidget(self.contenedor_main, alignment=Qt.AlignCenter)
        layout_centro.addStretch()
        contenedor_centro.setLayout(layout_centro)
        
        self.layout_main.addWidget(contenedor_centro)
        
        self.crear_panel_login()
        
        # Acción para atajo de teclado
        self.login_action = QAction("Login", self)
        self.login_action.setShortcut("Return")
        self.login_action.triggered.connect(self.verificar_login)
        self.addAction(self.login_action)
        
    def crear_panel_login(self):
        """Crea el panel del formulario de login"""
        # Contenedor principal del login
        self.contenedor_login = QFrame()
        self.contenedor_login.setFixedWidth(420)
        
        # Layout del login
        layout_login = QVBoxLayout()
        layout_login.setContentsMargins(0, 0, 0, 0)
        layout_login.setSpacing(20)
        self.contenedor_login.setLayout(layout_login)
        
        # Estilo del contenedor
        self.contenedor_login.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BLANCO};
                border-radius: 16px;
                border: 1px solid {COLOR_GRIS_BORDE};
                margin: 0;
            }}
        """)
        
        # Sombra más pronunciada
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(30)
        sombra.setColor(QColor(0, 0, 0, 25))
        sombra.setOffset(0, 5)
        self.contenedor_login.setGraphicsEffect(sombra)
        
        # Encabezado
        self.crear_encabezado_login(layout_login)
        
        # Logo
        self.crear_logo(layout_login)
        
        # Campos del formulario
        self.crear_campos_formulario(layout_login)
        
        # Botón de login
        self.crear_boton_login(layout_login)
        
        # Mensaje de error
        self.label_error = QLabel("")
        self.label_error.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_ERROR};
                font-family: {FONT_FAMILY};
                font-size: 13px;
                padding: 12px;
                margin: 5px 0;
                background-color: #fdeded;
                border: 1px solid {COLOR_ERROR}20;
                border-radius: 8px;
                font-weight: 500;
            }}
        """)
        self.label_error.setAlignment(Qt.AlignCenter)
        self.label_error.setVisible(False)
        layout_login.addWidget(self.label_error)
        
        # Espaciador final
        layout_login.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.layout_contenedor.addWidget(self.contenedor_login)
        self.layout_contenedor.addStretch()
        
    def crear_encabezado_login(self, layout):
        """Crea el encabezado del panel de login"""
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
        titulo.setMinimumHeight(50)
        layout.addWidget(titulo)
        
        # Subtítulo opcional para más elegancia
        subtitulo = QLabel("Inicia sesión en tu cuenta")
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
        
    def crear_logo(self, layout):
        """Crea y configura el logo"""
        contenedor_logo = QFrame()
        contenedor_logo.setStyleSheet("background: transparent; margin: 0; border: none;")
        
        layout_logo = QVBoxLayout()
        layout_logo.setContentsMargins(0, 0, 0, 0)
        contenedor_logo.setLayout(layout_logo)
        
        imagen = QLabel()
        pixmap = QPixmap("img/imagen.png")
        # Escalar la imagen si es necesario
        if not pixmap.isNull():
            pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            imagen.setPixmap(pixmap)
        
        imagen.setAlignment(Qt.AlignCenter)
        imagen.setStyleSheet("background: transparent; margin: 0;")
        layout_logo.addWidget(imagen)
        
        layout.addWidget(contenedor_logo, alignment=Qt.AlignCenter)
        
    def crear_campos_formulario(self, layout):
        """Crea los campos del formulario"""
        # Contenedor para mejor espaciado
        contenedor_form = QFrame()
        contenedor_form.setStyleSheet("background: transparent; border: none;")
        layout_form = QVBoxLayout()
        layout_form.setContentsMargins(0, 0, 0, 0)
        layout_form.setSpacing(10)
        contenedor_form.setLayout(layout_form)
        
        # Campo de usuario
        label_usuario = QLabel("Usuario")
        label_usuario.setStyleSheet(f"""
            QLabel {{
                background: transparent;
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_TEXTO};
                font-weight: 500;
                margin: 0 15px;
                padding: 0;
            }}
        """)
        layout_form.addWidget(label_usuario)
        
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su usuario")
        self.input_usuario.setMinimumHeight(48)
        self.input_usuario.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 1.5px solid {COLOR_GRIS_BORDE};
                border-radius: 10px;
                padding: 14px 18px;
                font-size: 15px;
                font-family: {FONT_FAMILY};
                margin: 0;
                selection-background-color: {COLOR_PRIMARIO};
                color: {COLOR_TEXTO};
                margin: 0 15px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {COLOR_PRIMARIO};
                background-color: {COLOR_BLANCO};
            }}
            QLineEdit:hover {{
                border: 1.5px solid {COLOR_SECUNDARIO};
            }}
            QLineEdit::placeholder {{
                color: #95a5a6;
                font-weight: normal;
            }}
        """)
        layout_form.addWidget(self.input_usuario)
        
        # Espaciador entre campos
        layout_form.addSpacing(10)
        
        # Campo de contraseña
        label_password = QLabel("Contraseña")
        label_password.setStyleSheet(f"""
            QLabel {{
                background: transparent;
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_TEXTO};
                font-weight: 500;
                margin: 0 15px;
                padding: 0;
            }}
        """)
        layout_form.addWidget(label_password)
        
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setMinimumHeight(48)
        self.input_password.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 1.5px solid {COLOR_GRIS_BORDE};
                border-radius: 10px;
                padding: 14px 18px;
                font-size: 15px;
                font-family: {FONT_FAMILY};
                margin: 0;
                selection-background-color: {COLOR_PRIMARIO};
                color: {COLOR_TEXTO};
                margin: 0 15px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {COLOR_PRIMARIO};
                background-color: {COLOR_BLANCO};
            }}
            QLineEdit:hover {{
                border: 1.5px solid {COLOR_SECUNDARIO};
            }}
            QLineEdit::placeholder {{
                color: #95a5a6;
                font-weight: normal;
            }}
        """)
        layout_form.addWidget(self.input_password)
        
        layout.addWidget(contenedor_form)
        
    def crear_boton_login(self, layout):
        """Crea el botón de inicio de sesión"""
        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.setMinimumHeight(52)
        self.boton_login.setCursor(Qt.PointingHandCursor)
        
        # Estilo más moderno con transiciones
        self.boton_login.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARIO};
                color: {COLOR_BLANCO};
                font-family: {FONT_FAMILY};
                font-weight: 600;
                font-size: 16px;
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
        self.boton_login.setGraphicsEffect(sombra_boton)
        
        layout.addWidget(self.boton_login)
        
    def conectar_eventos(self):
        # Conecta las señales de los widgets
        self.boton_login.clicked.connect(self.verificar_login)
        self.input_usuario.returnPressed.connect(self.verificar_login)
        self.input_password.returnPressed.connect(self.verificar_login)
        
    def verificar_login(self):
        """Verifica las credenciales del usuario"""
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()
        
        # Validación básica
        if not usuario or not password:
            self.mostrar_error("Por favor, complete todos los campos")
            return
            
        if len(usuario) < 3:
            self.mostrar_error("El usuario debe tener al menos 3 caracteres")
            return
            
        if len(password) < 5:
            self.mostrar_error("La contraseña debe tener al menos 5 caracteres")
            return
        
        # Si pasa todas las validaciones
        self.limpiar_error()
        print(f"Login exitoso: {usuario}")
        self.login_exitoso.emit()
        
    def obtener_estilo_input(self, error=False):
        """Devuelve el estilo para los inputs"""
        estilo_base = f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 1.5px solid {'#e74c3c' if error else COLOR_GRIS_BORDE};
                border-radius: 10px;
                padding: 14px 18px;
                font-size: 15px;
                font-family: {FONT_FAMILY};
                margin: 0;
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
        
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        self.label_error.setText(f"⚠ {mensaje}")
        self.label_error.setVisible(True)
        
        # Aplicar estilo de error a los campos
        self.input_usuario.setStyleSheet(self.obtener_estilo_input(True))
        self.input_password.setStyleSheet(self.obtener_estilo_input(True))
        
    def limpiar_error(self):
        """Limpia los mensajes de error"""
        self.label_error.setText("")
        self.label_error.setVisible(False)
        
        # Restaurar estilos originales
        self.input_usuario.setStyleSheet(self.obtener_estilo_input(False))
        self.input_password.setStyleSheet(self.obtener_estilo_input(False))
