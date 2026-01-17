from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QFrame, QAction,
                            QLabel, QGraphicsDropShadowEffect, QSpacerItem,
                            QSizePolicy, QLineEdit, QPushButton, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QColor
import sys

# Variables globales mejoradas
FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e"
COLOR_AZUL_HOVER = "#00485a"
COLOR_SECUNDARIO = "#007a94"
COLOR_BLANCO = "#FFFFFF"
COLOR_GRIS_CLARO = "#f5f5f5"
COLOR_GRIS_BORDE = "#ddd"
COLOR_TEXTO = "#333"
COLOR_ERROR = "#e74c3c"

class Ventana_login(QFrame):
    login_exitoso = pyqtSignal()  # Modificado para enviar el nombre de usuario
    
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
        self.conectar_eventos()
        
    def inicializar_ui(self):
        """Configuración inicial de la interfaz de usuario"""
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_GRIS_CLARO};
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)
        
        # Layout principal
        self.layout_main = QVBoxLayout()
        self.layout_main.setContentsMargins(50, 50, 50, 50)
        self.setLayout(self.layout_main)
        
        # Contenedor principal
        self.contenedor_main = QFrame()
        self.contenedor_main.setMaximumHeight(700)
        self.contenedor_main.setStyleSheet("background: transparent;")
        
        self.layout_contenedor = QHBoxLayout()
        self.layout_contenedor.setContentsMargins(0, 0, 0, 0)
        self.layout_contenedor.setSpacing(0)
        self.contenedor_main.setLayout(self.layout_contenedor)
        
        self.layout_main.addWidget(self.contenedor_main, alignment=Qt.AlignCenter)
        
        # Crear paneles
        self.crear_panel_imagen()
        self.crear_panel_login()
        
        # Acción para atajo de teclado
        self.login_action = QAction("Login", self)
        self.login_action.setShortcut("Return")
        self.login_action.triggered.connect(self.verificar_login)
        self.addAction(self.login_action)
        
    def crear_panel_imagen(self):
        """Crea el panel con la imagen decorativa"""
        contenedor_imagen = QFrame()
        contenedor_imagen.setFixedWidth(600)
        contenedor_imagen.setMinimumHeight(650)
        
        # Mejorar el estilo de la imagen
        contenedor_imagen.setStyleSheet(f"""
            QFrame {{
                background-image: url(img/login_image.jpg);
                background-position: center;
                background-repeat: no-repeat;
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
                margin: 0;
            }}
        """)
        
        # Agregar overlay para mejor contraste
        overlay = QFrame(contenedor_imagen)
        overlay.setStyleSheet(f"""
            background-color: rgba(0, 90, 110, 0.3);
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
        """)
        overlay.setGeometry(0, 0, 600, 650)
        
        # Título en la imagen
        titulo_imagen = QLabel("Sistema de Gestión", contenedor_imagen)
        titulo_imagen.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_BLANCO};
                font-family: {FONT_FAMILY};
                font-size: 36px;
                font-weight: bold;
                background: transparent;
                padding: 20px;
            }}
        """)
        titulo_imagen.setAlignment(Qt.AlignCenter)
        titulo_imagen.setGeometry(50, 100, 500, 100)

        # Descripcion del programa
        titulo_imagen = QLabel("Sistema de Gestión de Reportes\nIngrese sus credenciales", contenedor_imagen)
        titulo_imagen.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_BLANCO};
                font-family: {FONT_FAMILY};
                font-size: 30px;
                font-weight: bold;
                background: transparent;
                padding: 20px;
            }}
        """)
        titulo_imagen.setAlignment(Qt.AlignCenter)
        titulo_imagen.setGeometry(50, 100, 500, 500)
        
        self.layout_contenedor.addWidget(contenedor_imagen)
        
    def crear_panel_login(self):
        """Crea el panel del formulario de login"""
        # Contenedor principal del login
        self.contenedor_login = QFrame()
        self.contenedor_login.setFixedWidth(500)
        self.contenedor_login.setMinimumHeight(650)
        
        # Layout del login
        layout_login = QVBoxLayout()
        layout_login.setContentsMargins(40, 40, 40, 20)
        layout_login.setSpacing(20)
        self.contenedor_login.setLayout(layout_login)
        
        # Estilo del contenedor
        self.contenedor_login.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_BLANCO};
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
                margin: 0;
            }}
        """)
        
        # Sombra más pronunciada
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(40)
        sombra.setColor(QColor(0, 0, 0, 60))
        sombra.setOffset(4, 4)
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
                font-size: 12px;
                padding: 5px;
                margin: 0 10px;
                background: transparent;
            }}
        """)
        self.label_error.setAlignment(Qt.AlignCenter)
        self.label_error.setVisible(False)
        layout_login.addWidget(self.label_error)
        
        # Espaciador final
        layout_login.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.layout_contenedor.addWidget(self.contenedor_login)
        
    def crear_encabezado_login(self, layout):
        """Crea el encabezado del panel de login"""
        titulo = QLabel("Bienvenido")
        titulo.setStyleSheet(f"""
            QLabel {{
                background: white;
                font-family: {FONT_FAMILY};
                font-size: 34px;
                color: black;
                font-weight: bold;
                padding: 25px;
                margin: -50px -40px 0 -40px;
                border-top-right-radius: 20px;
            }}
        """)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setMinimumHeight(80)
        layout.addWidget(titulo)
        
    def crear_logo(self, layout):
        """Crea y configura el logo"""
        contenedor_logo = QFrame()
        contenedor_logo.setStyleSheet("background: transparent; margin: 5px;")
        
        layout_logo = QVBoxLayout()
        layout_logo.setContentsMargins(0, 10, 0, 10)
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
        # Campo de usuario
        label_usuario = QLabel("Usuario:")
        label_usuario.setStyleSheet(f"""
            QLabel {{
                background: transparent;
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_TEXTO};
                font-weight: bold;
                margin: 5px 10px 5px 10px;
            }}
        """)
        layout.addWidget(label_usuario)
        
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su usuario")
        self.input_usuario.setMinimumHeight(45)
        self.input_usuario.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 2px solid {COLOR_GRIS_BORDE};
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                font-family: {FONT_FAMILY};
                margin: 0 10px 15px 10px;
                selection-background-color: {COLOR_PRIMARIO};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARIO};
                background-color: {COLOR_BLANCO};
            }}
            QLineEdit:hover {{
                border: 2px solid {COLOR_SECUNDARIO};
            }}
        """)
        layout.addWidget(self.input_usuario)
        
        # Campo de contraseña
        label_password = QLabel("Contraseña:")
        label_password.setStyleSheet(f"""
            QLabel {{
                background: transparent;
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_TEXTO};
                font-weight: bold;
                margin: 5px 10px 5px 10px;
            }}
        """)
        layout.addWidget(label_password)
        
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setMinimumHeight(45)
        self.input_password.setStyleSheet(f"""
            QLineEdit {{
                background: {COLOR_BLANCO};
                border: 2px solid {COLOR_GRIS_BORDE};
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                font-family: {FONT_FAMILY};
                margin: 0 10px 15px 10px;
                selection-background-color: {COLOR_PRIMARIO};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARIO};
                background-color: {COLOR_BLANCO};
            }}
            QLineEdit:hover {{
                border: 2px solid {COLOR_SECUNDARIO};
            }}
        """)
        layout.addWidget(self.input_password)
        
    def crear_boton_login(self, layout):
        """Crea el botón de inicio de sesión"""
        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.setMinimumHeight(50)
        self.boton_login.setCursor(Qt.PointingHandCursor)
        self.boton_login.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARIO};
                color: {COLOR_BLANCO};
                font-family: {FONT_FAMILY};
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                border-radius: 8px;
                border: none;
                margin: 20px 10px 10px 10px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_SECUNDARIO};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_AZUL_HOVER};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)
        layout.addWidget(self.boton_login)
        
    def conectar_eventos(self):
        """Conecta las señales de los widgets"""
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
            
        
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        self.label_error.setText(mensaje)
        self.label_error.setVisible(True)
        
        # Aplicar estilo de error a los campos
        self.input_usuario.setStyleSheet(self.input_usuario.styleSheet() + f"border: 2px solid {COLOR_ERROR};")
        self.input_password.setStyleSheet(self.input_password.styleSheet() + f"border: 2px solid {COLOR_ERROR};")
        
    def limpiar_error(self):
        """Limpia los mensajes de error"""
        self.label_error.setText("")
        self.label_error.setVisible(False)
        
        # Restaurar estilos originales
        self.input_usuario.setStyleSheet(self.input_usuario.styleSheet().replace(f"border: 2px solid {COLOR_ERROR};", ""))
        self.input_password.setStyleSheet(self.input_password.styleSheet().replace(f"border: 2px solid {COLOR_ERROR};", ""))
        
