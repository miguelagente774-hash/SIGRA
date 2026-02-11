from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTextEdit, QWidget, 
                             QPushButton, QLineEdit, QSizePolicy,
                             QMessageBox, QDateEdit, QDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QIcon
from services.Cargar_imagenes import ImageFrame
from components.app_style import estilo_app

# Clase: Ventana Modal para Actualizar Actividades
class Modal_actulizar_actividades(QDialog):
    def __init__(self, id_actividad, titulo, descripcion, ruta1, ruta2, fecha, controlador, parent = None):
        super().__init__(parent)
        # Definir variables necesarias así como Estilo
        self.controller = controlador
        self.id_actividad = id_actividad
        self.titulo = titulo
        self.imagen1 = ruta1
        self.imagen2 = ruta2
        self.descripcion = descripcion
        self.fecha = fecha
        self.estilo = estilo_app.obtener_estilo_completo()
        self.colores = self.estilo["colors"]
        self.setWindowIcon(QIcon("img/icono.ico"))

        # Variables para almacenar las rutas de las imágenes
        self.imagen1_path = None
        self.imagen2_path = None

        # Establecer el Tema de Fondo
        self.setStyleSheet(self.estilo["styles"]["fondo"])

        # Registrar esta vista para actualización automática
        estilo_app.registrar_vista(self)
        
        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)  

        # Inicializar Métodos iniciales
        self.setup_ui()
        self.setup_panel()

    def setup_ui(self):
        # Establecer los parámetros iniciales
        self.setWindowTitle("Actualizar Actividad")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(800, 600)

    def setup_panel(self):
        # Layout Principal
        self.layout_principal = QVBoxLayout(self)

        # Contenedor
        contenedor_panel = QFrame()
        contenedor_panel.setMinimumHeight(600)
        contenedor_panel.setStyleSheet(self.estilo["styles"]["panel"])
        contenedor_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Sombra de la Ventana
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setColor(QColor(self.colores.get("shadow", Qt.gray)))
        sombra.setOffset(2, 2)
        contenedor_panel.setGraphicsEffect(sombra)

        # Layout del Panel
        layout_panel = QVBoxLayout(contenedor_panel)

        # Agregar componentes al panel
        layout_panel.addWidget(self.crear_titulo_seccion())
        layout_panel.addWidget(self.crear_campo_titulo_actividad())
        layout_panel.addWidget(self.crear_contenedor_imagenes())
        layout_panel.addWidget(self.crear_campo_descripcion(), 1)
        layout_panel.addLayout(self.Campo_fecha())
        
        # Layout para el Botón de Guardar
        layout_h = QHBoxLayout()
        layout_panel.addLayout(layout_h)
        layout_h.addWidget(self.crear_boton_guardar())

        # Añadir el contenedor panel al Layout Principal
        self.layout_principal.addWidget(contenedor_panel)

    def crear_titulo_seccion(self):
        #Crea el título de la sección
        titulo = QLabel("Actualizar Actividad")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignLeft)
        return titulo

    def crear_campo_titulo_actividad(self):
        """Crea el campo de entrada para el título de la actividad"""
        self.titulo_actividad = QLineEdit(self.titulo)
        self.titulo_actividad.setPlaceholderText("Ingrese el título de la actividad")
        self.titulo_actividad.setStyleSheet(self.estilo["styles"]["input"])
        return self.titulo_actividad

    def crear_contenedor_imagenes(self):
        """Crea el contenedor para las imágenes"""
        contenedor = QFrame()
        contenedor.setStyleSheet(f"""
            QFrame {{
                background: {self.colores['bg_primary']};
                border: 2px solid {self.colores['border']};
                padding: 10px;
                margin: 0 15px;
            }}
        """)
        
        layout_contenedor = QVBoxLayout(contenedor)
        
        # Título de la sección de imágenes
        titulo_imagenes = QLabel("Imágenes de la actividad")
        titulo_imagenes.setStyleSheet(self.estilo["styles"]["title"])
        titulo_imagenes.setAlignment(Qt.AlignCenter)
        layout_contenedor.addWidget(titulo_imagenes)
        
        # Fila para las imágenes
        fila_imagenes = QWidget()
        fila_imagenes.setStyleSheet("background: transparent;")
        layout_fila = QHBoxLayout(fila_imagenes)
        layout_fila.setContentsMargins(0, 0, 0, 0)
        layout_fila.setSpacing(20)
        
        # Crear frames de imágenes
        self.frame_imagen1 = ImageFrame(1, self.imagen1, parent=self)
        self.frame_imagen2 = ImageFrame(2, self.imagen2, parent=self)
        
        layout_fila.addWidget(self.frame_imagen1)
        layout_fila.addWidget(self.frame_imagen2)

        contenedor.setMinimumHeight(230)
        
        layout_contenedor.addWidget(fila_imagenes, 1)
        
        return contenedor

    def crear_campo_descripcion(self):
        # Crea el campo de texto para la descripción
        self.input_reporte = QTextEdit(self.descripcion)
        self.input_reporte.setPlaceholderText("Ingrese la descripción de la Actividad...")
        self.input_reporte.setStyleSheet(self.estilo["styles"]["input"])
        return self.input_reporte
    
    def Campo_fecha(self):
        layout = QHBoxLayout()
        titulo = QLabel("Fecha de la Actividad:")
        titulo.setStyleSheet(self.estilo["styles"]["title"])
        layout.addWidget(titulo)

        fecha_actividad = self.fecha
        partes_fecha = fecha_actividad.split("-")
        dia = int(partes_fecha[0])
        mes = int(partes_fecha[1])
        año = int(partes_fecha[2])

        self.fecha = QDateEdit(QDate(año, mes, dia), self)
        self.fecha.setStyleSheet(self.estilo["styles"]["date"])
        self.fecha.setCalendarPopup(True)
        self.fecha.setFixedWidth(150)

        layout.addWidget(self.fecha, alignment=Qt.AlignLeft)

        return layout

    def crear_boton_guardar(self):
        # Crear el Botón para guardar la actividad
        btn_guardar = QPushButton("Actualizar Actividad")
        btn_guardar.setStyleSheet(self.estilo["styles"]["boton"])
        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.clicked.connect(self.Guardar_datos_actividad)

        return btn_guardar 
    
    def Guardar_datos_actividad(self):
        confirmacion = QMessageBox.question(self, "Actualizar actividad", "Seguro que deseas actulizar la actividad", QMessageBox.Yes, QMessageBox.No)
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

    # Método en cada vista:
    def actualizar_estilos(self):
        # Actualizar los estilo de la vista
        self.estilo = estilo_app.obtener_estilo_completo()
        
        # Aplicar fondo al modal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar panel principal
        for widget in self.findChildren(QFrame):
            # Buscar el panel principal por su sombra
            if widget.graphicsEffect():
                widget.setStyleSheet(self.estilo["styles"]["panel"])
                
                # Actualizar sombra
                effect = widget.graphicsEffect()
                if isinstance(effect, QGraphicsDropShadowEffect):
                    effect.setColor(QColor(self.colores.get("shadow", Qt.gray)))
        
        # Actualizar título
        for widget in self.findChildren(QLabel):
            if widget.text() == "Actualizar Actividad":
                widget.setStyleSheet(self.estilo["styles"]["header"])
            elif widget.text() == "Imágenes de la actividad":
                widget.setStyleSheet(self.estilo["styles"]["title"])
            elif widget.text() == "Fecha de la Actividad:":
                widget.setStyleSheet(self.estilo["styles"]["title"])
        
        # Actualizar inputs
        for widget in self.findChildren((QLineEdit, QTextEdit)):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        # Actualizar QDateEdit
        for widget in self.findChildren(QDateEdit):
            widget.setStyleSheet(self.estilo["styles"]["date"])
        
        # Actualizar botones
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(self.estilo["styles"]["boton"])
        
        # Actualizar contenedor de imágenes
        for widget in self.findChildren(QFrame):
            # Buscar contenedor de imágenes
            child_labels = [child.text() for child in widget.findChildren(QLabel) if child.text()]
            if "Imágenes de la actividad" in child_labels:
                widget.setStyleSheet(f"""
                    QFrame {{
                        background: {self.colores["bg_secondary"]};
                        border: 1px solid {self.colores["border"]};
                        border-radius: 8px;
                        padding: 10px;
                        margin: 0 15px;
                    }}
                """)
        
        # Actualizar frames de imágenes
        if hasattr(self, 'frame_imagen1'):
            self.frame_imagen1.actualizar_estilos()
        if hasattr(self, 'frame_imagen2'):
            self.frame_imagen2.actualizar_estilos()
        