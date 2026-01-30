from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout,
                             QGraphicsDropShadowEffect, QGroupBox, QRadioButton,
                             QSizePolicy, QSpacerItem, QSpinBox, QComboBox, QCheckBox,
                             QGridLayout, QLineEdit, QButtonGroup, QPushButton, QDateEdit, 
                             QScrollArea, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QColor
from components.app_style import estilo_app

class Ventana_configuracion(QFrame):
    # Señales simplificadas
    guardar_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.estilo = estilo_app.obtener_estilo_completo()
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        #Registrar esta vista
        estilo_app.registrar_vista(self)

        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la UI con el diseño original completo"""
        # Scroll area con estilo original
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet(self.estilo["styles"]["scroll"])
        
        # Widget contenedor para el scroll
        self.scroll_widget = QWidget()
        self.layout_main = QVBoxLayout(self.scroll_widget)
        self.layout_main.setContentsMargins(20, 15, 20, 15)
        self.layout_main.setSpacing(20)
        
        self.scroll_area.setWidget(self.scroll_widget)
        
        # Layout principal que contiene el scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)

        # Crear paneles con diseño original
        self.crear_panel_interfaz()
        self.crear_panel_direccion()
        self.crear_panel_jefaturas()
        self.crear_panel_gaceta()
        self.crear_boton_guardar()
        
        # Spacer final
        self.layout_main.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    # ========== PANEL INTERFAZ CON ESTILO ORIGINAL ==========
    
    def crear_panel_interfaz(self):
        """Crea panel de interfaz con el diseño original"""
        # Frame principal con sombra y bordes redondeados
        self.panel_interfaz = QFrame()
        self.panel_interfaz.setStyleSheet(self.estilo["styles"]["panel"])
        
        # Sombra elegante
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        self.panel_interfaz.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(self.panel_interfaz)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título con estilo header
        titulo = QLabel("Configuración de Interfaz")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout_panel.addWidget(titulo)
        
        # Contenedor del contenido
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(15, 20, 15, 20)
        layout_contenido.setSpacing(20)
        contenido_frame.setLayout(layout_contenido)
        layout_panel.addWidget(contenido_frame)
        
        # Layout horizontal para los grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(20)
        layout_contenido.addLayout(layout_horizontal)
        
        # ===== GRUPO TEMA CON ESTILO ORIGINAL =====
        self.grupo_tema = QGroupBox("Tema de la aplicación")
        self.grupo_tema.setMinimumWidth(200)
        self.grupo_tema.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_tema = QVBoxLayout()
        layout_tema.setSpacing(12)
        self.grupo_tema.setLayout(layout_tema)
        
        # Botones de radio con estilo
        self.tema_group = QButtonGroup()
        self.radio_tema_claro = QRadioButton("Tema Claro")
        self.radio_tema_oscuro = QRadioButton("Tema Oscuro")
    
        self.radio_tema_claro.setStyleSheet(self.estilo["styles"]["radio"])
        self.radio_tema_oscuro.setStyleSheet(self.estilo["styles"]["radio"])
        
        self.tema_group.addButton(self.radio_tema_claro)
        self.tema_group.addButton(self.radio_tema_oscuro)
        
        layout_tema.addWidget(self.radio_tema_claro)
        layout_tema.addWidget(self.radio_tema_oscuro)
        layout_tema.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # ===== GRUPO FUENTE CON ESTILO ORIGINAL =====
        self.grupo_fuente = QGroupBox("Configuración de Fuente")
        self.grupo_fuente.setMinimumWidth(200)
        self.grupo_fuente.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_fuente = QVBoxLayout()
        layout_fuente.setSpacing(15)
        self.grupo_fuente.setLayout(layout_fuente)
        
        # Combobox de fuentes
        label_tipo = QLabel("Tipo de Letra")
        label_tipo.setStyleSheet(self.estilo["styles"]["title"])
        layout_fuente.addWidget(label_tipo)
        
        self.combo_fuente = QComboBox()
        self.combo_fuente.addItems(["Arial", "Segoe UI", "Verdana", "Tahoma", "Georgia"])
        self.combo_fuente.setStyleSheet(self.estilo["styles"]["input"])
        layout_fuente.addWidget(self.combo_fuente)
        
        # Tamaño de fuente
        label_tamano = QLabel("Tamaño de la fuente")
        label_tamano.setStyleSheet(self.estilo["styles"]["title"])
        layout_fuente.addWidget(label_tamano)
        
        self.spin_tamano = QSpinBox()
        self.spin_tamano.setStyleSheet(self.estilo["styles"]["input"])
        self.spin_tamano.setMinimum(10)
        self.spin_tamano.setMaximum(18)
        self.spin_tamano.setValue(12)
        layout_fuente.addWidget(self.spin_tamano)
        
        # Checkbox de negrita
        self.check_negrita = QCheckBox("Negrita en títulos")
        self.check_negrita.setStyleSheet(self.estilo["styles"]["checkbox"])
        layout_fuente.addWidget(self.check_negrita)
        layout_fuente.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Agregar grupos al layout horizontal
        layout_horizontal.addWidget(self.grupo_tema)
        layout_horizontal.addWidget(self.grupo_fuente)
        
        # Agregar panel al layout principal
        self.layout_main.addWidget(self.panel_interfaz)
    
    # ========== PANEL DIRECCIÓN CON ESTILO ORIGINAL ==========
    
    def crear_panel_direccion(self):
        # Frame principal
        self.panel_direccion = QFrame()
        self.panel_direccion.setStyleSheet(self.estilo["styles"]["panel"])
        
        # Sombra
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        self.panel_direccion.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(self.panel_direccion)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título
        titulo = QLabel("Configuración de Datos de Dirección")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setMinimumHeight(50)
        layout_panel.addWidget(titulo)
        
        # Contenedor del contenido
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(15, 20, 15, 20)
        layout_contenido.setSpacing(25)
        contenido_frame.setLayout(layout_contenido)
        layout_panel.addWidget(contenido_frame)
        
        # ===== GRUPO DIRECCIÓN CON ESTILO ORIGINAL =====
        self.grupo_direccion = QGroupBox("Configuración de Dirección")
        self.grupo_direccion.setStyleSheet(self.estilo["styles"]["grupo"])
        
        # Layout horizontal para dos columnas
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(20)
        self.grupo_direccion.setLayout(layout_horizontal)
        
        # ===== COLUMNA IZQUIERDA (Estado y Parroquia) =====
        self.columna_izquierda = QFrame()
        self.columna_izquierda.setStyleSheet("QFrame{ background: transparent; }")
        layout_izquierda = QVBoxLayout(self.columna_izquierda)
        layout_izquierda.setSpacing(15)
        
        # Estado
        self.label_estado = QLabel("Estado:")
        self.label_estado.setStyleSheet(self.estilo["styles"]["title"])  # Aplicar estilo al label
        self.entry_estado = QLineEdit()
        self.entry_estado.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_estado.setPlaceholderText("Ingrese el estado")
        
        # Parroquia
        self.label_parroquia = QLabel("Parroquia:")
        self.label_parroquia.setStyleSheet(self.estilo["styles"]["title"])  # Aplicar estilo al label
        self.entry_parroquia = QLineEdit()
        self.entry_parroquia.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_parroquia.setPlaceholderText("Ingrese la parroquia")
        
        layout_izquierda.addWidget(self.label_estado)
        layout_izquierda.addWidget(self.entry_estado)
        layout_izquierda.addWidget(self.label_parroquia)
        layout_izquierda.addWidget(self.entry_parroquia)
        
        # ===== COLUMNA DERECHA (Municipio e Institución) =====
        self.columna_derecha = QFrame()
        self.columna_derecha.setStyleSheet("QFrame{ background: transparent; }")
        layout_derecha = QVBoxLayout(self.columna_derecha)
        layout_derecha.setSpacing(15)
        
        # Municipio
        self.label_municipio = QLabel("Municipio:")
        self.label_municipio.setStyleSheet(self.estilo["styles"]["title"])  # Aplicar estilo al label
        self.entry_municipio = QLineEdit()
        self.entry_municipio.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_municipio.setPlaceholderText("Ingrese el municipio")
        
        # Institución
        self.label_institucion = QLabel("Comunidad/Institución:")
        self.label_institucion.setStyleSheet(self.estilo["styles"]["title"])  # Aplicar estilo al label
        self.entry_institucion = QLineEdit()
        self.entry_institucion.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_institucion.setPlaceholderText("Ingrese comunidad o institución")
        
        layout_derecha.addWidget(self.label_municipio)
        layout_derecha.addWidget(self.entry_municipio)
        layout_derecha.addWidget(self.label_institucion)
        layout_derecha.addWidget(self.entry_institucion)
        
        # Agregar ambas columnas al layout horizontal
        layout_horizontal.addWidget(self.columna_izquierda)
        layout_horizontal.addWidget(self.columna_derecha)
        
        # Hacer que las columnas se expandan equitativamente
        layout_horizontal.setStretch(0, 1)
        layout_horizontal.setStretch(1, 1)
        
        # Agregar el grupo al layout de contenido
        layout_contenido.addWidget(self.grupo_direccion)
        
        # Agregar panel al layout principal
        self.layout_main.addWidget(self.panel_direccion)
    
    # ========== PANEL JEFATURAS CON ESTILO ORIGINAL ==========
    
    def crear_panel_jefaturas(self):
        """Crea panel de jefaturas con el diseño original"""
        # Frame principal
        self.panel_jefaturas = QFrame()
        self.panel_jefaturas.setStyleSheet(self.estilo["styles"]["panel"])
        
        # Sombra
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        self.panel_jefaturas.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(self.panel_jefaturas)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título
        titulo = QLabel("Datos de Jefaturas")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setMinimumHeight(50)
        layout_panel.addWidget(titulo)
        
        # Contenedor del contenido
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(15, 20, 15, 20)
        layout_contenido.setSpacing(25)
        contenido_frame.setLayout(layout_contenido)
        layout_panel.addWidget(contenido_frame)
        
        # Layout horizontal para los dos grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(20)
        layout_contenido.addLayout(layout_horizontal)
        
        # ===== GRUPO COORDINACIÓN CON ESTILO ORIGINAL =====
        self.grupo_coordinacion = QGroupBox("Jefe de Coordinación")
        self.grupo_coordinacion.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_coordinacion = QVBoxLayout()
        layout_coordinacion.setSpacing(15)
        self.grupo_coordinacion.setLayout(layout_coordinacion)
        
        # Campos coordinación        
        self.label_nombre_coord = QLabel("Nombre completo:")
        self.label_nombre_coord.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_nombre_coord = QLineEdit()
        self.entry_nombre_coord.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_nombre_coord.setPlaceholderText("Ingrese nombre completo")
        
        self.label_cedula_coord = QLabel("Cédula de identidad:")
        self.label_cedula_coord.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_cedula_coord = QLineEdit()
        self.entry_cedula_coord.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_cedula_coord.setPlaceholderText("Ej: V-12345678")
        
        layout_coordinacion.addWidget(self.label_nombre_coord)
        layout_coordinacion.addWidget(self.entry_nombre_coord)
        layout_coordinacion.addWidget(self.label_cedula_coord)
        layout_coordinacion.addWidget(self.entry_cedula_coord)
        
        # ==Datos de Gobernacion==
        self.grupo_gobernacion = QGroupBox("Jefa de Gobernación")
        self.grupo_gobernacion.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_gobernacion = QVBoxLayout()
        layout_gobernacion.setSpacing(15)
        self.grupo_gobernacion.setLayout(layout_gobernacion)
        
        self.label_nombre_gob = QLabel("Nombre completo:")
        self.label_nombre_gob.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_nombre_gob = QLineEdit()
        self.entry_nombre_gob.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_nombre_gob.setPlaceholderText("Ingrese nombre completo")
        
        self.label_cedula_gob = QLabel("Cédula de identidad:")
        self.label_cedula_gob.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_cedula_gob = QLineEdit()
        self.entry_cedula_gob.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_cedula_gob.setPlaceholderText("Ej: V-12345678")
        
        layout_gobernacion.addWidget(self.label_nombre_gob)
        layout_gobernacion.addWidget(self.entry_nombre_gob)
        layout_gobernacion.addWidget(self.label_cedula_gob)
        layout_gobernacion.addWidget(self.entry_cedula_gob)
        
        # Agregar grupos al layout horizontal
        layout_horizontal.addWidget(self.grupo_coordinacion)
        layout_horizontal.addWidget(self.grupo_gobernacion)
        
        # Hacer que los grupos se expandan equitativamente
        layout_horizontal.setStretch(0, 1)
        layout_horizontal.setStretch(1, 1)
        self.layout_main.addWidget(self.panel_jefaturas)
    
    def crear_panel_gaceta(self):
        # ==Crear panel de Gaceta==
        # Frame Principal
        self.panel_gaceta = QFrame()
        self.panel_gaceta.setStyleSheet(self.estilo["styles"]["panel"])

        # Sombra
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        self.panel_gaceta.setGraphicsEffect(sombra)

        layout_panel = QVBoxLayout(self.panel_gaceta)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título
        titulo = QLabel("Gaceta Coordinador")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setMinimumHeight(50)
        layout_panel.addWidget(titulo)

        # Contenedor del contenido
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(15, 20, 15, 20)
        layout_contenido.setSpacing(25)
        contenido_frame.setLayout(layout_contenido)
        layout_panel.addWidget(contenido_frame)

        # Layout horizontal para los dos grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(20)
        layout_contenido.addLayout(layout_horizontal)

        # ==Grupo de Gaceta Coordinador==
        self.grupo_gaceta = QGroupBox("Gaceta Coordinador")
        self.grupo_gaceta.setStyleSheet(self.estilo["styles"]["grupo"])

        layout_gaceta = QVBoxLayout()
        layout_gaceta.setSpacing(15)
        self.grupo_gaceta.setLayout(layout_gaceta)

        # Campos Coordinacion: Decreto
        self.label_decreto = QLabel("Decreto:")
        self.label_decreto.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_decreto = QLineEdit()
        self.entry_decreto.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_decreto.setPlaceholderText("Ingrese el Decreto de la Gaceta Coordinador")

        # Campos Coordiancion: Fecha de Publicacion
        self.label_fechaPublicacion = QLabel("Fecha de Publicacion: ")
        self.label_fechaPublicacion.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_fechaPublicacion = QLineEdit()
        self.entry_fechaPublicacion.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_fechaPublicacion.setPlaceholderText("Ingrese un dato Válido")

        # Añadir Widgets al Layout
        layout_gaceta.addWidget(self.label_decreto)
        layout_gaceta.addWidget(self.entry_decreto)
        layout_gaceta.addWidget(self.label_fechaPublicacion)
        layout_gaceta.addWidget(self.entry_fechaPublicacion)

        # Añadir Grupo al Layout
        layout_horizontal.addWidget(self.grupo_gaceta)
        
        # Añadir el Panel Gaceta al Layout
        self.layout_main.addWidget(self.panel_gaceta)
        
    # ==Método de Botón de Guardar==
    def crear_boton_guardar(self):
        """Crea botón de guardar con el diseño original"""
        layout_boton = QHBoxLayout()
        
        # Spacer izquierdo
        layout_boton.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Botón guardar con estilo original
        self.boton_guardar = QPushButton("Guardar Cambios")
        self.boton_guardar.setStyleSheet(self.estilo["styles"]["boton"])
        self.boton_guardar.clicked.connect(self.guardar_clicked.emit)
        layout_boton.addWidget(self.boton_guardar)
        
        # Spacer derecho
        layout_boton.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.layout_main.addLayout(layout_boton)
    
    def actualizar_estilos(self):
        """Actualiza los estilos de esta vista"""
        print(f"🔄 {self.__class__.__name__} actualizando estilos...")
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        font_size = self.estilo["font_size"]
        
        # Aplicar fondo a la vista principal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar scroll area
        self.scroll_area.setStyleSheet(self.estilo["styles"]["scroll"])
        
        # Lista de paneles para actualizar
        paneles = [
            self.panel_interfaz,
            self.panel_direccion,
            self.panel_jefaturas,
            self.panel_gaceta
        ]
        
        # Actualizar cada panel
        for panel in paneles:
            if panel:
                # Actualizar estilo del panel
                panel.setStyleSheet(f"""
                    QFrame {{
                        {self.estilo["styles"]["panel"]}
                        background-color: {colores["bg_panel"]};
                    }}
                """)
                
                # Actualizar sombra
                if panel.graphicsEffect():
                    effect = panel.graphicsEffect()
                    if isinstance(effect, QGraphicsDropShadowEffect):
                        effect.setColor(QColor(colores.get("shadow", Qt.gray)))
        
        # Actualizar todos los QGroupBox con estilo específico
        for widget in self.findChildren(QGroupBox):
            widget.setStyleSheet(self.estilo["styles"]["grupo"])
        
        # Actualizar todos los QLabel
        for widget in self.findChildren(QLabel):
            # Verificar si es un título de sección
            text = widget.text()
            if text in [
                "Configuración de Interfaz",
                "Configuración de Datos de Dirección", 
                "Datos de Jefaturas",
                "Gaceta Coordinador"
            ]:
                widget.setStyleSheet(self.estilo["styles"]["title"])
            elif text in ["Tipo de Letra", "Tamaño de la fuente", "Estado:", "Parroquia:", 
                        "Municipio:", "Comunidad/Institución:", "Nombre completo:", 
                        "Cédula de identidad:", "Decreto:", "Fecha de Publicacion:"]:
                widget.setStyleSheet(self.estilo["styles"]["label"])
        
        # Actualizar todos los inputs con estilos más visibles
        for widget in self.findChildren(QLineEdit):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        for widget in self.findChildren(QComboBox):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        for widget in self.findChildren(QSpinBox):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        # Actualizar todos los QRadioButton
        for widget in self.findChildren(QRadioButton):
            widget.setStyleSheet(self.estilo["styles"]["radio"])
        
        # Actualizar todos los QCheckBox
        for widget in self.findChildren(QCheckBox):
            widget.setStyleSheet(self.estilo["styles"]["checkbox"])
        
        # Actualizar botón guardar con estilo más destacado
        if hasattr(self, 'boton_guardar'):
            self.boton_guardar.setStyleSheet(self.estilo["styles"]["boton"])
        
        print(f"✅ {self.__class__.__name__} estilos actualizados")