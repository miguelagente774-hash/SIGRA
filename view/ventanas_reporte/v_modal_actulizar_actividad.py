from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTextEdit, QWidget, 
                             QPushButton, QLineEdit, QSizePolicy, QFileDialog,
                             QMessageBox, QDateEdit, QDialog)
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtGui import QPixmap, QIcon, QFont
from services.Cargar_imagenes import ImageFrame

FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"

BTN_STYLE = """
        QPushButton{
        background: #005a6e;
        color: White;
        font-weight: bold;
        font-size: 18px;
        min-width: 200px;
        min-height: 20px;
        padding: 15px;
        border-radius: 15px;
        text-align: left;
        border: none;
        margin: 15px 15px;
        }  
        QPushButton:hover{
        background: #007a94;
        }    
        QPushButton:pressed{
        background: #00485a;
        }"""

class Modal_actulizar_actividades(QDialog):
    def __init__(self, id_actividad, titulo, descripcion, ruta1, ruta2, fecha, controlador, parent = None):
        super().__init__(parent)
        #valores de la actividad a modificar
        self.controller = controlador
        self.id_actividad = id_actividad
        self.titulo = titulo
        self.imagen1 = ruta1
        self.imagen2 = ruta2
        self.descripcion = descripcion
        self.fecha = fecha
        self.setWindowTitle("Actividad_actulizacion")
        self.setWindowModality(Qt.ApplicationModal)

        self.setGeometry(100, 100, 700, 300)
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.setStyleSheet("""QFrame{
                        border-top-left-radius: 15px;
                        border-top-right-radius: 15px;
                        border-bottom-left-radius: 15px;
                        border-bottom-right-radius: 15px;
                        }""")
        
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
        titulo = QLabel("Actualizar Actividad")
        titulo.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            background: #005a6e;
            font-size: 28px; 
            color: white;
            font-weight: bold;
            margin: 0;
            padding: 20px 15px;
            border-radius: 0;
            text-align: left;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
                        
        """)
        titulo.setAlignment(Qt.AlignLeft)
        titulo.setMaximumHeight(70)
        return titulo

    def crear_campo_titulo_actividad(self):
        """Crea el campo de entrada para el título de la actividad"""
        self.titulo_actividad = QLineEdit(self.titulo)
        self.titulo_actividad.setPlaceholderText("Ingrese el título de la actividad")
        self.titulo_actividad.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: 16px;
            padding: 12px;
            margin: 10px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            background: white;
        """)
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
        titulo_imagenes.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: 24px;
            color: #374151;
            font-weight: bold;
            margin: 20px;
            padding: 0;
            border: none;
        """)
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
        self.frame_imagen1 = ImageFrame(1, self.imagen1, self)
        self.frame_imagen2 = ImageFrame(2, self.imagen2, self)
        
        layout_fila.addWidget(self.frame_imagen1)
        layout_fila.addWidget(self.frame_imagen2)
        #layout_fila.addStretch()  # Empuja las imágenes hacia la izquierda

        contenedor.setMinimumHeight(350)
        contenedor.setMaximumHeight(600)
        
        layout_contenedor.addWidget(fila_imagenes)
        
        return contenedor

    def crear_campo_descripcion(self):
        """Crea el campo de texto para la descripción"""
        self.input_reporte = QTextEdit(self.descripcion)
        self.input_reporte.setPlaceholderText("Ingrese la descripción de la Actividad...")
        self.input_reporte.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: 16px;
            padding: 5px;
            margin: 5px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            background: white;
        """)
        self.input_reporte.setMaximumHeight(200)
        return self.input_reporte
    
    def Campo_fecha(self):
        layout = QHBoxLayout()
        titulo = QLabel("fecha de la actividad")
        titulo.setStyleSheet("""            
            font-family: {FONT_FAMILY};
            font-size: 24px;
            color: #374151;
            font-weight: bold;
            margin: 10px;
            padding: 0;
            border: none;""")
        layout.addWidget(titulo)

        fecha_actividad = self.fecha
        partes_fecha = fecha_actividad.split("-")
        dia = int(partes_fecha[0])
        mes = int(partes_fecha[1])
        año = int(partes_fecha[2])

        self.fecha = QDateEdit(QDate(año, mes, dia), self)
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
        self.fecha.setFixedWidth(150)

        layout.addWidget(self.fecha)

        return layout

    def crear_boton_guardar(self):
        """Crea el botón para guardar la actividad"""
        btn_guardar = QPushButton("Actulizar Actividad")
        btn_guardar.setStyleSheet(BTN_STYLE)


        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.clicked.connect(self.Guardar_datos_actividad)

        return btn_guardar 
    
    def Guardar_datos_actividad(self):
        confirmacion = QMessageBox.question(self, "Actulizar actividad", "Seguro que deseas actulizar la actividad", QMessageBox.Yes, QMessageBox.No)
        if confirmacion == QMessageBox.Yes:
            id_actividad = self.id_actividad
            titulo = self.titulo_actividad.text()
            imagen1 = self.frame_imagen1.get_imagen_path()
            imagen2 = self.frame_imagen2.get_imagen_path()
            descripcion = self.input_reporte.toPlainText()
            fecha = self.fecha.date()
            fecha = fecha.toString("dd-MM-yyyy")
            #tipo_actividad = "Anexo"

            self.controller.Actulizar_actividad(id_actividad, titulo, descripcion, imagen1, imagen2, fecha, self.imagen1, self.imagen2)
        
    def mensaje_advertencia(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def mensaje_informativo(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)