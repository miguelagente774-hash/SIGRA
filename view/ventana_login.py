from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QFrame, QAction,
                            QLabel, QGraphicsDropShadowEffect, QSpacerItem,
                            QSizePolicy, QLineEdit, QPushButton, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
import sys
#variables globales
FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"

# configuraciones del Frame de la ventana
class Ventana_login(QFrame):
    login_exitoso = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        #self.layout_main.setContentsMargins(130, 0, 130, 0)
        self.setStyleSheet("""            
                QFrame {
                background-repeat: no-repeat;
                background-position: center;
            }""")  
        # Cambiado de rojo a gris claro
        self.Panel()

    # ----- panel de la ventana principal ---------
    def Panel(self):
        # --- configurando los layouts
        layout_panel = QVBoxLayout()
        
        layout_panel_v = QVBoxLayout()
        layout_panel_v.setSpacing(0)

        layout_panel_h = QHBoxLayout()
        
        layout_panel.addLayout(layout_panel_v)
        layout_panel.addLayout(layout_panel_h)

        #-------eliminando margenes entre widgets del panel ----------
        layout_panel.setContentsMargins(0, 0, 0, 0)

        #------------ panel -----------------
        Contenedor_panel = QFrame()
        Contenedor_panel.setMinimumWidth(500)
        Contenedor_panel.setMinimumHeight(650)
        
        
        #layout del panel
        Contenedor_panel.setLayout(layout_panel)
        #configuracion del panel
        Contenedor_panel.setStyleSheet("""
            background: rgba(255, 255, 255, 1); 
            margin: auto;
            border-radius: 20px;
        """)
        
        #----------------anexando sombra al panel--------------
        sombra = QGraphicsDropShadowEffect()
        #difuminado de la sombra
        sombra.setBlurRadius(25)
        #colocando el color de la sombra
        sombra.setColor(Qt.gray)
        #desplazamiento de la sombra
        sombra.setOffset(1, 1)
        Contenedor_panel.setGraphicsEffect(sombra)
        
        #---------------- titulos de la ventana ------------------
        titulo = QLabel("Bienvenido al Sistema")
        titulo.setStyleSheet(f"""
            background: "#005a6e";
            font-family: {FONT_FAMILY};
            font-size: 28px; 
            color: white;
            font-weight: bold;
            padding: 20px;
            margin: 0;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        """)
        titulo.setAlignment(Qt.AlignHCenter)
        layout_panel_v.addWidget(titulo, alignment=Qt.AlignTop)

        #---------- logo ---------------
        imagen = QLabel()
        imagen.setStyleSheet("margin: 0;")
        pixmap = QPixmap("img/logos/login_logo.png")
        imagen.setPixmap(pixmap)
        imagen.setContentsMargins(0, 0, 1, 1)
        layout_panel_v.addWidget(imagen, alignment=Qt.AlignCenter)

        #---------------- campos de login ------------------
        # Campo de usuario
        label_usuario = QLabel("Usuario:")
        label_usuario.setStyleSheet(f"""
            background: none;
            font-family: {FONT_FAMILY};
            font-size: 14px;
            color: #333;
            font-weight: bold;
            margin: 0 10px;
            min-height: 40px;
            min-width: 40px;
            border: none
        """)
        layout_panel_v.addWidget(label_usuario)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su usuario")
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                margin: 0 10px 30px;
                min-height: 20px;
                min-width: 40px;
            }
            QLineEdit:focus {
                border: 2px solid #005a6e;
            }
        """)
        layout_panel_v.addWidget(self.input_usuario)

        # Campo de contraseña
        label_password = QLabel("Contraseña:")
        label_password.setStyleSheet(f"""
            background: none;
            font-family: {FONT_FAMILY};
            font-size: 14px;
            color: #333;
            font-weight: bold;
            margin: 10px 10px 0px;
            min-height: 40px;
            min-width: 40px;
            border: none
        """)
        layout_panel_v.addWidget(label_password)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese su contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                margin: 0 10px 25px;
                min-height: 20px;
                min-width: 40px;    
            }
            QLineEdit:focus {
                border: 2px solid #005a6e;
            }
        """)
        layout_panel_v.addWidget(self.input_password)

        # Botón de login
        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.setStyleSheet("""
            QPushButton {
                background: #005a6e;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                border-radius: 8px;
                border: none;
                margin: 20px 15px;
                min-height: 20px;
                min-width: 30px;    
            }
            QPushButton:hover {
                background: #007a94;
            }
            QPushButton:pressed {
                background: #00485a;
            }
        """)

        layout_panel_v.addWidget(self.boton_login)

        # Agregar el panel al layout principal
        self.layout_main.addWidget(Contenedor_panel, alignment=Qt.AlignCenter)
        
        # Atajo de Teclado para Verificar el Login
        self.login_btn = QAction(self)
        self.login_btn.setShortcut("Return")
        self.addAction(self.login_btn)