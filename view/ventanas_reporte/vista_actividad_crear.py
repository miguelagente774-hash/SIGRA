from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTextEdit, QWidget, 
                             QPushButton, QLineEdit, QSizePolicy, QFileDialog,
                             QMessageBox, QDateEdit)
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtGui import QPixmap, QIcon, QFont
from services.Cargar_imagenes import ImageFrame
from components.app_style import estilo_app


# Instancia global para el uso en toda la aplicación
estilo = estilo_app.obtener_estilo_completo()

# Variables globales para la consistencia
FONT_FAMILY = estilo["font_family"]
COLOR_PRIMARIO = estilo["color_primario"]
COLOR_AZUL_HOVER = estilo["color_hover"]
COLOR_SECUNDARIO = estilo["color_secundario"]
BG_COLOR_PANEL = estilo["colors"]["bg_panel"]
BG_COLOR_FONDO = estilo["colors"]["bg_fondo"]

class Ventana_reporte_crear(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.estilo = estilo_app.obtener_estilo_completo()
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.layout_main.setContentsMargins(40, 40, 40, 40)
        self.setStyleSheet("""QFrame{
                        border-top-left-radius: 15px;
                        border-top-right-radius: 15px;
                        border-bottom-left-radius: 15px;
                        border-bottom-right-radius: 15px;
                        }""")

        # Aplicar el estilo
        self.setStyleSheet(self.estilo["styles"]["fondo"])

        # Variables para almacenar las rutas de las imágenes
        self.imagen1_path = None
        self.imagen2_path = None
        
        self.inicializar_ui()

    def inicializar_ui(self):
        """Inicializa todos los componentes de la interfaz de usuario"""
        self.crear_panel_principal()

    def crear_panel_principal(self):
        """Crea el panel principal con sombra y estilo"""
        panel_reporte = self.crear_panel_con_sombra()
        panel_layout = QVBoxLayout(panel_reporte)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(0)

        # Agregar componentes al panel
        panel_layout.addWidget(self.crear_titulo_seccion())
        panel_layout.addWidget(self.crear_campo_titulo_actividad())
        panel_layout.addWidget(self.crear_contenedor_imagenes())
        panel_layout.addWidget(self.crear_campo_descripcion())
        panel_layout.addLayout(self.Campo_fecha())
        
        layout_h = QHBoxLayout()
        panel_layout.addLayout(layout_h)
        layout_h.addWidget(self.crear_boton_guardar())
        layout_h.addWidget(self.btn_limpiar_campos())
        

        self.layout_main.addWidget(panel_reporte)

    def crear_panel_con_sombra(self):
        """Crea el panel principal con efecto de sombra"""
        panel = QFrame()
        panel.setStyleSheet("""
            background: #f5f5f5; 
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 0;
        """)

        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setColor(Qt.gray)
        sombra.setOffset(2, 2)
        panel.setGraphicsEffect(sombra)

        return panel

    def crear_titulo_seccion(self):
        """Crea el título de la sección"""
        titulo = QLabel("Crear Actividad")
        titulo.setStyleSheet(estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setMaximumHeight(70)
        return titulo

    def crear_campo_titulo_actividad(self):
        """Crea el campo de entrada para el título de la actividad"""
        self.titulo_actividad = QLineEdit()
        self.titulo_actividad.setPlaceholderText("Ingrese el título de la actividad")
        self.titulo_actividad.setStyleSheet(estilo["styles"]["input"])
        return self.titulo_actividad

    def crear_contenedor_imagenes(self):
        """Crea el contenedor para las imágenes"""
        contenedor = QFrame()
        contenedor.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #e5e7eb;
                padding: 10px;
                margin: 0 15px;
            }
        """)
        
        layout_contenedor = QVBoxLayout(contenedor)
        #layout_contenedor.setContentsMargins(0, 0, 0, 0)
        #layout_contenedor.setSpacing(0)
        
        # Título de la sección de imágenes
        titulo_imagenes = QLabel("Imágenes de la actividad")
        titulo_imagenes.setStyleSheet(estilo["styles"]["header"])
        titulo_imagenes.setAlignment(Qt.AlignCenter)
        layout_contenedor.addWidget(titulo_imagenes)
        
        # Fila para las imágenes
        fila_imagenes = QWidget()
        fila_imagenes.setStyleSheet("padding: 0; margin: 0; background: white;")
        layout_fila = QHBoxLayout(fila_imagenes)
        layout_fila.setContentsMargins(0, 0, 0, 0)
        layout_fila.setSpacing(20)
        #layout_fila.setAlignment(Qt.AlignCenter)
        
        # Crear frames de imágenes
        self.frame_imagen1 = ImageFrame(1, ruta_imagen=None, parent=self)
        self.frame_imagen2 = ImageFrame(2, ruta_imagen=None, parent=self)
        
        layout_fila.addWidget(self.frame_imagen1)
        layout_fila.addWidget(self.frame_imagen2)
        #layout_fila.addStretch()  # Empuja las imágenes hacia la izquierda

        
        contenedor.setMinimumHeight(300)
        contenedor.setMaximumHeight(600)
        
        layout_contenedor.addWidget(fila_imagenes)
        
        return contenedor

    def crear_campo_descripcion(self):
        """Crea el campo de texto para la descripción"""
        self.input_reporte = QTextEdit()
        self.input_reporte.setPlaceholderText("Ingrese la descripción de la Actividad...")
        self.input_reporte.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: 16px;
            padding: 12px;
            margin: 15px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            background: white;
        """)
        self.input_reporte.setMaximumHeight(200)
        return self.input_reporte
    
    def Campo_fecha(self):
        layout = QHBoxLayout()
        titulo = QLabel("Fecha de la actividad")
        titulo.setStyleSheet(estilo["styles"]["title"])
        layout.addWidget(titulo)

        self.fecha = QDateEdit(self)
        self.fecha.setStyleSheet("""QDateEdit {
        margin: 0 0 0 20px;
        border: 2px solid #005a6e;       /* Borde sólido azul */
        border-radius: 5px;              /* Esquinas redondeadas */
        padding: 10px;                    /* Espacio interno */
        background-color: #FFFFFF;       /* Fondo blanco */
        color: #333333;                  /* Color del texto */
        font-size: 14px;                 /* Tamaño de fuente */
        selection-background-color: #0056b3; /* Color de fondo del texto seleccionado */
        }

        QDateEdit:hover {
        border-color: #0056b3;           /* Borde más oscuro al pasar el cursor */
        }

        QDateEdit:disabled {
        background-color: #e0e0e0;       /* Fondo gris cuando está deshabilitado */
        color: #999999;
        }   
                            """)
        self.fecha.setCalendarPopup(True)
        self.fecha.setFixedWidth(250)
        self.fecha.setDate(QDate.currentDate())

        layout.addWidget(self.fecha)

        return layout

    def crear_boton_guardar(self):
        """Crea el botón para guardar la actividad"""
        btn_guardar = QPushButton("Guardar Actividad")
        btn_guardar.setStyleSheet(estilo["styles"]["boton"])
        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.clicked.connect(self.Guardar_datos_actividad)

        return btn_guardar
    
    def btn_limpiar_campos(self):
        btn_limpiar = QPushButton("Limpiar Campos")
        btn_limpiar.setStyleSheet(estilo["styles"]["boton"])
        btn_limpiar.clicked.connect(self.limpiar_formulario)

        return btn_limpiar


    def Guardar_datos_actividad(self):
        """Retorna todos los datos de la actividad"""
        titulo = self.titulo_actividad.text()
        imagen1 = self.frame_imagen1.get_imagen_path()
        imagen2 = self.frame_imagen2.get_imagen_path()
        descripcion = self.input_reporte.toPlainText()
        fecha = self.fecha.date()
        fecha = fecha.toString("dd-MM-yyyy")
        tipo_actividad = "Anexo"

        self.controller.Guardar_actividad(titulo, imagen1, imagen2, descripcion, fecha, tipo_actividad)

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.titulo_actividad.clear()
        self.input_reporte.clear()
        
        # Restablecer imágenes
        self.imagen1_path = None
        self.imagen2_path = None
        
        # Limpiar frames de imágenes
        self.frame_imagen1.eliminar_imagen()
        self.frame_imagen2.eliminar_imagen()
    
    def mensaje_advertencia(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def mensaje_informativo(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)