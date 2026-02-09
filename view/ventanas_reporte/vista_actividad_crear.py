from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTextEdit, QWidget, 
                             QPushButton, QLineEdit, QMessageBox, QDateEdit, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QColor
from services.Cargar_imagenes import ImageFrame
from components.app_style import estilo_app

# Clase: Crear Actividades
class Ventana_reporte_crear(QFrame):
    # Definir las Señales
    guardar = pyqtSignal()
    limpiar = pyqtSignal()
    def __init__(self, controlador):
        super().__init__()
        # Inicializar Estilo y Controlador
        self.estilo = estilo_app.obtener_estilo_completo() 
        self.controller = controlador

        # Establecer el Tema del Fondo
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Registrar esta vista para actualización automática
        estilo_app.registrar_vista(self)

        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)

        # Variables para almacenar las rutas de las imágenes
        self.imagen1_path = None
        self.imagen2_path = None
        
        # Inicializar Métodos Iniciales
        self.setup_panel()

    def setup_panel(self):
        # Layout Principal y de Contenido
        self.layout_principal = QVBoxLayout(self)

        # Contenedor
        contenedor_panel = QFrame()
        contenedor_panel.setMinimumHeight(250)
        contenedor_panel.setStyleSheet(self.estilo["styles"]["panel"])
        contenedor_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contenedor_panel.setMinimumSize(700, 450)

        # Sombra de la Ventana
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        colores = self.estilo["colors"]
        sombra.setColor(QColor(colores.get("shadow", Qt.gray)))
        sombra.setOffset(2, 2)
        contenedor_panel.setGraphicsEffect(sombra)

        # Layout del Panel
        layout_panel = QVBoxLayout(contenedor_panel)

        # Título de la Ventana
        titulo = QLabel("Crear Actividad")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        layout_panel.addWidget(titulo)

        # Input Título de la Actividad
        self.titulo_actividad = QLineEdit()
        self.titulo_actividad.setPlaceholderText("Ingrese el título de la actividad")
        self.titulo_actividad.setStyleSheet(self.estilo["styles"]["input"])
        layout_panel.addWidget(self.titulo_actividad)
        
        # Contenedor de las Imágenes - Contenedor
        contenedor = QFrame()
        contenedor.setStyleSheet(self.estilo["styles"]["frame"])
        
        # Contenedor de las Imágenes - Layout
        layout_contenedor = QVBoxLayout(contenedor)
        
        # Contenedor de las Imágenes - Título de la sección de imágenes
        titulo_imagenes = QLabel("Imágenes de la actividad")
        titulo_imagenes.setStyleSheet(self.estilo["styles"]["title"])
        titulo_imagenes.setAlignment(Qt.AlignCenter)
        layout_contenedor.addWidget(titulo_imagenes)
        
        # Contenedor de las Imágenes - Fila para las imágenes
        fila_imagenes = QWidget()
        fila_imagenes.setStyleSheet(self.estilo["styles"]["widget"])
        layout_fila = QHBoxLayout(fila_imagenes)
        layout_fila.setSpacing(40)  
        layout_fila.setAlignment(Qt.AlignCenter)
        
        # Contenedor de las Imágenes - Crear frames de imágenes
        self.frame_imagen1 = ImageFrame(1, ruta_imagen=None, parent=self)
        self.frame_imagen2 = ImageFrame(2, ruta_imagen=None, parent=self)
        
        layout_fila.addWidget(self.frame_imagen1)
        layout_fila.addWidget(self.frame_imagen2)
        
        contenedor.setMinimumHeight(220)
        
        layout_contenedor.addWidget(fila_imagenes)

        layout_panel.addWidget(contenedor)
        
        # Input Descripción de la Actividad
        self.input_reporte = QTextEdit()
        self.input_reporte.setPlaceholderText("Ingrese la descripción de la Actividad...")
        self.input_reporte.setStyleSheet(self.estilo["styles"]["input"])
        self.input_reporte.setMaximumHeight(200)
        layout_panel.addWidget(self.input_reporte)
        
        # Fecha de la Actividad - Layout
        layout_fecha = QHBoxLayout()
        
        # Fecha de la Actividad - Label
        titulo = QLabel("Fecha de la actividad:")
        titulo.setStyleSheet(self.estilo["styles"]["title"])
        layout_fecha.addWidget(titulo)

        # Fecha de la Actividad - QEdit
        self.fecha = QDateEdit(self)
        self.fecha.setStyleSheet(self.estilo["styles"]["date"])
        self.fecha.setCalendarPopup(True)
        self.fecha.setFixedWidth(250)
        self.fecha.setDate(QDate.currentDate())

        layout_fecha.addWidget(self.fecha, alignment=Qt.AlignLeft)
        layout_fecha.addStretch()

        layout_panel.addLayout(layout_fecha)
        
        # Agregar Botones
        layout_botones = QHBoxLayout()
        layout_panel.addLayout(layout_botones)

        # Botón de Guardar
        btn_guardar = QPushButton("Guardar Actividad")
        btn_guardar.setStyleSheet(self.estilo["styles"]["boton"])
        btn_guardar.clicked.connect(self.guardar.emit)
        layout_botones.addWidget(btn_guardar)

        # Botón de Limpiar Campos
        btn_limpiar = QPushButton("Limpiar Campos")
        btn_limpiar.setStyleSheet(self.estilo["styles"]["boton"]) 
        btn_limpiar.clicked.connect(self.limpiar.emit)
        layout_botones.addWidget(btn_limpiar)

        self.layout_principal.addWidget(contenedor_panel)
    
    def mensaje_advertencia(self, titulo, mensaje):
        QMessageBox.warning(self, titulo, mensaje)

    def mensaje_informativo(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mensaje_error(self, titulo, mensaje):
        self.QMessageBox.critical(self, titulo, mensaje)

    # Método en cada vista:
    def actualizar_estilos(self):
        # Actualizar los estilo de la vista
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        
        # Aplicar fondo a la vista principal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar panel principal
        for widget in self.findChildren(QFrame):
            # Buscar el panel principal por su sombra
            if widget.graphicsEffect():
                widget.setStyleSheet(self.estilo["styles"]["panel"])
                
                # Actualizar sombra
                effect = widget.graphicsEffect()
                if isinstance(effect, QGraphicsDropShadowEffect):
                    effect.setColor(QColor(colores.get("shadow", Qt.gray)))
        
        # Actualizar título
        for widget in self.findChildren(QLabel):
            if widget.text() == "Crear Actividad":
                widget.setStyleSheet(self.estilo["styles"]["header"])
            elif widget.text() == "Imágenes de la actividad":
                widget.setStyleSheet(self.estilo["styles"]["title"])
            elif widget.text() == "Fecha de la actividad:":
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
            # Buscar contenedor de imágenes por su layout y contenido
            child_labels = [child.text() for child in widget.findChildren(QLabel) if child.text()]
            if "Imágenes de la actividad" in child_labels:
                widget.setStyleSheet(self.estilo["styles"]["panel"])
        
        # Actualizar frames de imágenes
        if hasattr(self, 'frame_imagen1'):
            self.frame_imagen1.actualizar_estilos()
        if hasattr(self, 'frame_imagen2'):
            self.frame_imagen2.actualizar_estilos()