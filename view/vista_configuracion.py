from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout,
                             QGraphicsDropShadowEffect, QGroupBox, QRadioButton,
                             QSizePolicy, QSpacerItem, QSpinBox, QComboBox, QCheckBox,
                             QLineEdit, QButtonGroup, QPushButton,
                             QScrollArea, QWidget, QAction)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from components.app_style import estilo_app

# Clase: Ventana Configuración
class Ventana_configuracion(QFrame):
    # Señales simplificadas
    guardar_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # Inicializar Estilo
        self.estilo = estilo_app.obtener_estilo_completo()

        # Establecer el Tema de Fondo
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Registrar esta vista
        estilo_app.registrar_vista(self)

        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)
        
        # Inicializar Método Inicial
        self.setup_panel()
    
    def setup_panel(self):
        # == Configura el Panel Principal ==
        # Layout Principal (igual que en vista_consulta)
        self.layout_principal = QVBoxLayout(self)

        # Contenedor Principal con panel
        contenedor_panel = QFrame()
        contenedor_panel.setMinimumHeight(250)
        contenedor_panel.setStyleSheet(self.estilo["styles"]["panel"])
        contenedor_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contenedor_panel.setMinimumSize(700, 450)

        # Sombra del panel principal
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        colores = self.estilo["colors"]
        sombra.setColor(QColor(colores.get("shadow", Qt.gray)))
        sombra.setOffset(2, 2)
        contenedor_panel.setGraphicsEffect(sombra)

        # Layout interno del panel
        layout_panel_interno = QVBoxLayout(contenedor_panel)
        
        # Título de la Ventana (igual que en vista_consulta)
        titulo = QLabel("Configuración")
        titulo.setStyleSheet(self.estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        layout_panel_interno.addWidget(titulo)

        # == Área de Contenido con Scroll ==
        # Scroll area para el contenido
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet(self.estilo["styles"]["scroll"])
        
        # Widget contenedor para el scroll
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(20, 15, 20, 15)
        self.scroll_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.scroll_widget)
        
        # Agregar scroll area al layout del panel
        layout_panel_interno.addWidget(self.scroll_area, 1)  # factor de expansión 1

        # Crear paneles de configuración
        self.crear_panel_interfaz()
        self.crear_panel_objetivos()
        self.crear_panel_direccion()
        self.crear_panel_jefaturas()
        self.crear_panel_gaceta()
        self.crear_panel_seguridad()
        self.crear_boton_guardar()
        
        # Spacer final para empujar contenido hacia arriba
        self.scroll_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Agregar panel contenedor al layout principal
        self.layout_principal.addWidget(contenedor_panel)
    
    def crear_panel_interfaz(self):
        # =Crear Interfaz de la Ventana=
        # Panel con estilo y sombra
        panel_interfaz = QFrame()
        panel_interfaz.setStyleSheet(self.estilo["styles"]["panel"])
        
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        panel_interfaz.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(panel_interfaz)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título del panel
        titulo_panel = QLabel("Configuración de Interfaz")
        titulo_panel.setStyleSheet(self.estilo["styles"]["header"])
        layout_panel.addWidget(titulo_panel)
        
        # Contenido del panel
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("background: transparent;")
        layout_contenido = QVBoxLayout(contenido_frame)
        layout_contenido.setContentsMargins(20, 20, 20, 20)
        layout_contenido.setSpacing(20)
        
        # Layout horizontal para los grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(30)
        
        # GRUPO TEMA - QGroupBox Tema de la Aplicación
        self.grupo_tema = QGroupBox("Tema de la aplicación")
        self.grupo_tema.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_tema = QVBoxLayout()
        layout_tema.setSpacing(15)
        self.grupo_tema.setLayout(layout_tema)
        
        # GRUPO TEMA - QRadio Tema
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
        
        # GRUPO FUENTE - GroupBox
        self.grupo_fuente = QGroupBox("Configuración de Fuente")
        self.grupo_fuente.setStyleSheet(self.estilo["styles"]["grupo"])
        
        # GRUPO FUENTE - Layout
        layout_fuente = QVBoxLayout()
        layout_fuente.setSpacing(15)
        self.grupo_fuente.setLayout(layout_fuente)
        
        # GRUPO FUENTE - Label Tipo de Fuente
        label_tipo = QLabel("Tipo de Letra")
        label_tipo.setStyleSheet(self.estilo["styles"]["title"])
        layout_fuente.addWidget(label_tipo)
        
        # GRUPO FUENTE - ComboBox Tipo de Fuente
        self.combo_fuente = QComboBox()
        self.combo_fuente.addItems(["Arial", "Segoe UI", "Verdana", "Tahoma", "Georgia"])
        self.combo_fuente.setStyleSheet(self.estilo["styles"]["input"])
        layout_fuente.addWidget(self.combo_fuente)
        
        # GRUPO FUENTE - Label Tamaño de Fuente
        label_tamano = QLabel("Tamaño de la fuente")
        label_tamano.setStyleSheet(self.estilo["styles"]["title"])
        layout_fuente.addWidget(label_tamano)
        
        # GRUPO FUENTE - SpinBox Tamaño de Fuente
        self.spin_tamano = QSpinBox()
        self.spin_tamano.setStyleSheet(self.estilo["styles"]["input"])
        self.spin_tamano.setMinimum(10)
        self.spin_tamano.setMaximum(18)
        self.spin_tamano.setValue(12)
        layout_fuente.addWidget(self.spin_tamano)
        
        # GRUPO FUENTE - Checkbox de BOLD en Fuente
        self.check_negrita = QCheckBox("Negrita en títulos")
        self.check_negrita.setStyleSheet(self.estilo["styles"]["checkbox"])
        layout_fuente.addWidget(self.check_negrita)
        layout_fuente.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Agregar grupos al layout horizontal
        layout_horizontal.addWidget(self.grupo_tema)
        layout_horizontal.addWidget(self.grupo_fuente)
        
        # Hacer que los grupos se expandan equitativamente
        layout_horizontal.setStretch(0, 1)
        layout_horizontal.setStretch(1, 1)
        
        # Agregar layout horizontal al contenido
        layout_contenido.addLayout(layout_horizontal)
        layout_panel.addWidget(contenido_frame)
        
        # Agregar panel al scroll layout
        self.scroll_layout.addWidget(panel_interfaz)
        
        # Guardar referencia para actualización de estilos
        self.panel_interfaz = panel_interfaz

    def crear_panel_objetivos(self):
        # ==Crea panel para los objetivos de actividades==
        panel_objetivos = QFrame()
        panel_objetivos.setStyleSheet(self.estilo["styles"]["panel"])
        
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        panel_objetivos.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(panel_objetivos)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título del panel
        titulo_panel = QLabel("Objetivos de Actividades")
        titulo_panel.setStyleSheet(self.estilo["styles"]["header"])
        layout_panel.addWidget(titulo_panel)
        
        # Contenido del panel
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("background: transparent;")
        layout_contenido = QVBoxLayout(contenido_frame)
        layout_contenido.setContentsMargins(20, 20, 20, 20)
        layout_contenido.setSpacing(20)
        
        # Layout horizontal para los dos grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(30)
        
        # ===== GRUPO OBJETIVOS A CORTO PLAZO =====
        grupo_corto_plazo = QGroupBox("Objetivos a Corto Plazo")
        grupo_corto_plazo.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_corto_plazo = QVBoxLayout()
        layout_corto_plazo.setSpacing(15)
        layout_corto_plazo.setContentsMargins(15, 20, 15, 20)
        grupo_corto_plazo.setLayout(layout_corto_plazo)
        
        # Objetivo Semanal
        self.label_semanal = QLabel("Semanal:")
        self.label_semanal.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_semanal = QLineEdit()
        self.entry_semanal.setStyleSheet(self.estilo["styles"]["input"])
        
        # Objetivo Mensual
        self.label_mensual = QLabel("Mensual:")
        self.label_mensual.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_mensual = QLineEdit()
        self.entry_mensual.setStyleSheet(self.estilo["styles"]["input"])
        
        layout_corto_plazo.addWidget(self.label_semanal)
        layout_corto_plazo.addWidget(self.entry_semanal)
        layout_corto_plazo.addWidget(self.label_mensual)
        layout_corto_plazo.addWidget(self.entry_mensual)
        layout_corto_plazo.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # ===== GRUPO OBJETIVOS A LARGO PLAZO =====
        grupo_largo_plazo = QGroupBox("Objetivos a Largo Plazo")
        grupo_largo_plazo.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_largo_plazo = QVBoxLayout()
        layout_largo_plazo.setSpacing(15)
        layout_largo_plazo.setContentsMargins(15, 20, 15, 20)
        grupo_largo_plazo.setLayout(layout_largo_plazo)
        
        # Objetivo Trimestral
        self.label_trimestral = QLabel("Trimestral:")
        self.label_trimestral.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_trimestral = QLineEdit()
        self.entry_trimestral.setStyleSheet(self.estilo["styles"]["input"])
        
        # Objetivo Anual
        self.label_anual = QLabel("Anual:")
        self.label_anual.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_anual = QLineEdit()
        self.entry_anual.setStyleSheet(self.estilo["styles"]["input"])
        
        layout_largo_plazo.addWidget(self.label_trimestral)
        layout_largo_plazo.addWidget(self.entry_trimestral)
        layout_largo_plazo.addWidget(self.label_anual)
        layout_largo_plazo.addWidget(self.entry_anual)
        layout_largo_plazo.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Agregar grupos al layout horizontal
        layout_horizontal.addWidget(grupo_corto_plazo)
        layout_horizontal.addWidget(grupo_largo_plazo)
        layout_horizontal.setStretch(0, 1)
        layout_horizontal.setStretch(1, 1)
        
        # Agregar layout horizontal al contenido
        layout_contenido.addLayout(layout_horizontal)
        layout_panel.addWidget(contenido_frame)
        
        # Agregar panel al scroll layout
        self.scroll_layout.addWidget(panel_objetivos)
        
        # Guardar referencia para actualización de estilos
        self.panel_objetivos = panel_objetivos

    def crear_panel_direccion(self):
        # ==Crea panel de datos de dirección==
        # Crear Datos de la Localidad
        panel_direccion = QFrame()
        panel_direccion.setStyleSheet(self.estilo["styles"]["panel"])
        
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        panel_direccion.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(panel_direccion)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título del panel
        titulo_panel = QLabel("Datos de Dirección")
        titulo_panel.setStyleSheet(self.estilo["styles"]["header"])
        layout_panel.addWidget(titulo_panel)
        
        # Contenido del panel
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("background: transparent;")
        layout_contenido = QVBoxLayout(contenido_frame)
        layout_contenido.setContentsMargins(20, 20, 20, 20)
        layout_contenido.setSpacing(20)
        
        # Layout Horizontal para los dos grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(30)
        
        # ===== GRUPO INFORMACIÓN BÁSICA =====
        grupo_basica = QGroupBox()
        grupo_basica.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_basica = QVBoxLayout()
        layout_basica.setSpacing(15)
        layout_basica.setContentsMargins(15, 20, 15, 20)
        grupo_basica.setLayout(layout_basica)
        
        # Estado
        self.label_estado = QLabel("Estado:")
        self.label_estado.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_estado = QLineEdit()
        self.entry_estado.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_estado.setPlaceholderText("Ingrese el estado")
        
        # Parroquia
        self.label_parroquia = QLabel("Parroquia:")
        self.label_parroquia.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_parroquia = QLineEdit()
        self.entry_parroquia.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_parroquia.setPlaceholderText("Ingrese la parroquia")
        
        layout_basica.addWidget(self.label_estado)
        layout_basica.addWidget(self.entry_estado)
        layout_basica.addWidget(self.label_parroquia)
        layout_basica.addWidget(self.entry_parroquia)
        layout_basica.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # ===== GRUPO INFORMACIÓN TERRITORIAL =====
        grupo_territorial = QGroupBox()
        grupo_territorial.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_territorial = QVBoxLayout()
        layout_territorial.setSpacing(15)
        layout_territorial.setContentsMargins(15, 20, 15, 20)
        grupo_territorial.setLayout(layout_territorial)
        
        # Municipio
        self.label_municipio = QLabel("Municipio:")
        self.label_municipio.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_municipio = QLineEdit()
        self.entry_municipio.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_municipio.setPlaceholderText("Ingrese el municipio")
        
        # Institución
        self.label_institucion = QLabel("Comunidad/Institución:")
        self.label_institucion.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_institucion = QLineEdit()
        self.entry_institucion.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_institucion.setPlaceholderText("Ingrese comunidad o institución")
        
        layout_territorial.addWidget(self.label_municipio)
        layout_territorial.addWidget(self.entry_municipio)
        layout_territorial.addWidget(self.label_institucion)
        layout_territorial.addWidget(self.entry_institucion)
        layout_territorial.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Agregar grupos al layout horizontal
        layout_horizontal.addWidget(grupo_basica)
        layout_horizontal.addWidget(grupo_territorial)
        layout_horizontal.setStretch(0, 1)
        layout_horizontal.setStretch(1, 1)
        
        # Agregar layout horizontal al contenido
        layout_contenido.addLayout(layout_horizontal)
        layout_panel.addWidget(contenido_frame)
        
        # Agregar panel al scroll layout
        self.scroll_layout.addWidget(panel_direccion)
        
        # Guardar referencia
        self.panel_direccion = panel_direccion
    
    # ========== PANEL JEFATURAS ==========
    
    def crear_panel_jefaturas(self):
        # ==Crear Panel de Datos de la Jefatura==
        panel_jefaturas = QFrame()
        panel_jefaturas.setStyleSheet(self.estilo["styles"]["panel"])
        
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        panel_jefaturas.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(panel_jefaturas)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título del panel
        titulo_panel = QLabel("Datos de Jefaturas")
        titulo_panel.setStyleSheet(self.estilo["styles"]["header"])
        layout_panel.addWidget(titulo_panel)
        
        # Contenido del panel
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("background: transparent;")
        layout_contenido = QVBoxLayout(contenido_frame)
        layout_contenido.setContentsMargins(20, 20, 20, 20)
        layout_contenido.setSpacing(20)
        
        # Layout horizontal para los dos grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(30)
        
        # Grupo Coordinación
        grupo_coordinacion = QGroupBox("Jefe de Coordinación")
        grupo_coordinacion.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_coordinacion = QVBoxLayout()
        layout_coordinacion.setSpacing(15)
        grupo_coordinacion.setLayout(layout_coordinacion)
        
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
        
        # Grupo Gobernación
        grupo_gobernacion = QGroupBox("Jefa de Gobernación")
        grupo_gobernacion.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_gobernacion = QVBoxLayout()
        layout_gobernacion.setSpacing(15)
        grupo_gobernacion.setLayout(layout_gobernacion)
        
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
        layout_horizontal.addWidget(grupo_coordinacion)
        layout_horizontal.addWidget(grupo_gobernacion)
        layout_horizontal.setStretch(0, 1)
        layout_horizontal.setStretch(1, 1)
        
        # Agregar layout horizontal al contenido
        layout_contenido.addLayout(layout_horizontal)
        layout_panel.addWidget(contenido_frame)
        
        # Agregar panel al scroll layout
        self.scroll_layout.addWidget(panel_jefaturas)
        
        # Guardar referencia
        self.panel_jefaturas = panel_jefaturas
    
    def crear_panel_gaceta(self):
        """Crea panel de datos de gaceta"""
        panel_gaceta = QFrame()
        panel_gaceta.setStyleSheet(self.estilo["styles"]["panel"])
        
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        panel_gaceta.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(panel_gaceta)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título del panel
        titulo_panel = QLabel("Gaceta Oficial")
        titulo_panel.setStyleSheet(self.estilo["styles"]["header"])
        layout_panel.addWidget(titulo_panel)
        
        # Contenido del panel
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("background: transparent;")
        layout_contenido = QVBoxLayout(contenido_frame)
        layout_contenido.setContentsMargins(20, 20, 20, 20)
        layout_contenido.setSpacing(20)
        
        # Grupo Gaceta
        grupo_gaceta = QGroupBox("Información de Gaceta")
        grupo_gaceta.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_gaceta = QVBoxLayout()
        layout_gaceta.setSpacing(15)
        grupo_gaceta.setLayout(layout_gaceta)
        
        self.label_decreto = QLabel("Decreto:")
        self.label_decreto.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_decreto = QLineEdit()
        self.entry_decreto.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_decreto.setPlaceholderText("Ingrese el número de decreto")
        
        self.label_fechaPublicacion = QLabel("Fecha de Publicación:")
        self.label_fechaPublicacion.setStyleSheet(self.estilo["styles"]["title"])
        self.entry_fechaPublicacion = QLineEdit()
        self.entry_fechaPublicacion.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_fechaPublicacion.setPlaceholderText("DD/MM/AAAA")
        
        layout_gaceta.addWidget(self.label_decreto)
        layout_gaceta.addWidget(self.entry_decreto)
        layout_gaceta.addWidget(self.label_fechaPublicacion)
        layout_gaceta.addWidget(self.entry_fechaPublicacion)
        
        # Agregar grupo al contenido
        layout_contenido.addWidget(grupo_gaceta)
        layout_panel.addWidget(contenido_frame)
        
        # Agregar panel al scroll layout
        self.scroll_layout.addWidget(panel_gaceta)
        
        # Guardar referencia
        self.panel_gaceta = panel_gaceta

    def crear_panel_seguridad(self):
        # ==Crear Panel de Preguntas y Respuestas de Seguridad==
        panel_preguntas = QFrame()
        panel_preguntas.setStyleSheet(self.estilo["styles"]["panel"])
        
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        panel_preguntas.setGraphicsEffect(sombra)
        
        # Layout del panel
        layout_panel = QVBoxLayout(panel_preguntas)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)
        
        # Título del panel
        titulo_panel = QLabel("Preguntas y Respuestas de Seguridad")
        titulo_panel.setStyleSheet(self.estilo["styles"]["header"])
        layout_panel.addWidget(titulo_panel)
        
        # Contenido del panel
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("background: transparent;")
        layout_contenido = QVBoxLayout(contenido_frame)
        layout_contenido.setContentsMargins(20, 20, 20, 20)
        layout_contenido.setSpacing(20)

        # Lista de preguntas disponibles
        self.lista_preguntas = [
            "¿Nombre de tu mascota?",
            "¿Ciudad de nacimiento?",
            "¿Nombre de tu abuela?",
            "¿Tu comida favorita?",
            "¿Tu película favorita?",
            "¿Nombre de tu mejor amigo?",
            "¿Tu deporte favorito?",
            "¿Color favorito?"
        ]

        # Crear lista para almacenar los combos de preguntas (para acceso desde el controlador)
        self.preguntas_seguridad = []
        self.respuestas_seguridad = []

        # ===== PREGUNTA DE SEGURIDAD 1 =====
        grupo_pregunta1 = QGroupBox("Pregunta de Seguridad 1")
        grupo_pregunta1.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_pregunta1 = QVBoxLayout()
        layout_pregunta1.setSpacing(10)
        layout_pregunta1.setContentsMargins(15, 20, 15, 20)
        grupo_pregunta1.setLayout(layout_pregunta1)
        
        # Combobox para seleccionar la pregunta
        self.combo_pregunta1 = QComboBox()
        self.combo_pregunta1.addItems(self.lista_preguntas)
        self.combo_pregunta1.setStyleSheet(self.estilo["styles"]["input"])
        self.combo_pregunta1.setMinimumHeight(35)
        self.combo_pregunta1.setEditable(False)
        self.combo_pregunta1.setFocusPolicy(Qt.StrongFocus)
        self.combo_pregunta1.setInsertPolicy(QComboBox.NoInsert)
        layout_pregunta1.addWidget(self.combo_pregunta1)
        self.preguntas_seguridad.append(self.combo_pregunta1)  # Agregar a la lista
        
        # Campo para respuesta
        label_respuesta1 = QLabel("Respuesta:")
        label_respuesta1.setStyleSheet(self.estilo["styles"]["title"])
        layout_pregunta1.addWidget(label_respuesta1)
        
        self.entry_respuesta1 = QLineEdit()
        self.entry_respuesta1.setPlaceholderText("Ingrese su respuesta")
        self.entry_respuesta1.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_respuesta1.setMinimumHeight(35)
        layout_pregunta1.addWidget(self.entry_respuesta1)
        self.respuestas_seguridad.append(self.entry_respuesta1)  # Agregar a la lista
        
        layout_contenido.addWidget(grupo_pregunta1)
        
        # ===== PREGUNTA DE SEGURIDAD 2 =====
        grupo_pregunta2 = QGroupBox("Pregunta de Seguridad 2")
        grupo_pregunta2.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_pregunta2 = QVBoxLayout()
        layout_pregunta2.setSpacing(10)
        layout_pregunta2.setContentsMargins(15, 20, 15, 20)
        grupo_pregunta2.setLayout(layout_pregunta2)
        
        # Combobox para seleccionar la pregunta
        self.combo_pregunta2 = QComboBox()
        self.combo_pregunta2.addItems(self.lista_preguntas)
        self.combo_pregunta2.setStyleSheet(self.estilo["styles"]["input"])
        self.combo_pregunta2.setMinimumHeight(35)
        self.combo_pregunta2.setEditable(False)
        self.combo_pregunta2.setFocusPolicy(Qt.StrongFocus)
        self.combo_pregunta2.setInsertPolicy(QComboBox.NoInsert)
        layout_pregunta2.addWidget(self.combo_pregunta2)
        self.preguntas_seguridad.append(self.combo_pregunta2)  # Agregar a la lista
        
        # Campo para respuesta
        label_respuesta2 = QLabel("Respuesta:")
        label_respuesta2.setStyleSheet(self.estilo["styles"]["title"])
        layout_pregunta2.addWidget(label_respuesta2)
        
        self.entry_respuesta2 = QLineEdit()
        self.entry_respuesta2.setPlaceholderText("Ingrese su respuesta")
        self.entry_respuesta2.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_respuesta2.setMinimumHeight(35)
        layout_pregunta2.addWidget(self.entry_respuesta2)
        self.respuestas_seguridad.append(self.entry_respuesta2)  # Agregar a la lista
        
        layout_contenido.addWidget(grupo_pregunta2)
        
        # ===== PREGUNTA DE SEGURIDAD 3 =====
        grupo_pregunta3 = QGroupBox("Pregunta de Seguridad 3")
        grupo_pregunta3.setStyleSheet(self.estilo["styles"]["grupo"])
        
        layout_pregunta3 = QVBoxLayout()
        layout_pregunta3.setSpacing(10)
        layout_pregunta3.setContentsMargins(15, 20, 15, 20)
        grupo_pregunta3.setLayout(layout_pregunta3)
        
        # Combobox para seleccionar la pregunta
        self.combo_pregunta3 = QComboBox()
        self.combo_pregunta3.addItems(self.lista_preguntas)
        self.combo_pregunta3.setStyleSheet(self.estilo["styles"]["input"])
        self.combo_pregunta3.setMinimumHeight(35)
        self.combo_pregunta3.setEditable(False)
        self.combo_pregunta3.setFocusPolicy(Qt.StrongFocus)
        self.combo_pregunta3.setInsertPolicy(QComboBox.NoInsert)
        layout_pregunta3.addWidget(self.combo_pregunta3)
        self.preguntas_seguridad.append(self.combo_pregunta3)  # Agregar a la lista
        
        # Campo para respuesta
        label_respuesta3 = QLabel("Respuesta:")
        label_respuesta3.setStyleSheet(self.estilo["styles"]["title"])
        layout_pregunta3.addWidget(label_respuesta3)
        
        self.entry_respuesta3 = QLineEdit()
        self.entry_respuesta3.setPlaceholderText("Ingrese su respuesta")
        self.entry_respuesta3.setStyleSheet(self.estilo["styles"]["input"])
        self.entry_respuesta3.setMinimumHeight(35)
        layout_pregunta3.addWidget(self.entry_respuesta3)
        self.respuestas_seguridad.append(self.entry_respuesta3)  # Agregar a la lista
        
        layout_contenido.addWidget(grupo_pregunta3)
        
        # Nota informativa
        nota_label = QLabel("Nota: Las respuestas distinguen entre mayúsculas y minúsculas")
        nota_label.setStyleSheet("color: #7f8c8d; font-size: 11px; font-style: italic; margin-top: 5px;")
        nota_label.setAlignment(Qt.AlignCenter)
        layout_contenido.addWidget(nota_label)
        
        # Agregar contenido al panel
        layout_panel.addWidget(contenido_frame)
        
        # Agregar panel al scroll layout
        self.scroll_layout.addWidget(panel_preguntas)
        
        # Guardar referencias
        self.panel_preguntas = panel_preguntas
    def crear_boton_guardar(self):
        # =Crear el botón para guardar=
        # Layout para centrar el botón
        layout_boton = QHBoxLayout()
        
        # Spacer izquierdo
        layout_boton.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Botón guardar
        self.boton_guardar = QPushButton("Guardar Cambios")
        self.boton_guardar.setStyleSheet(self.estilo["styles"]["boton"])
        self.boton_guardar.clicked.connect(self.guardar_clicked.emit)
        layout_boton.addWidget(self.boton_guardar)
        
        # Spacer derecho
        layout_boton.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Agregar al scroll layout
        self.scroll_layout.addLayout(layout_boton)

        # =Crear una QAction para guardar=
        self.tecla_guardar = QAction(self)
        self.tecla_guardar.setShortcut("Return")
        self.addAction(self.tecla_guardar)

    def actualizar_estilos(self):
        # Actualizar los estilo de la vista
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        
        # Aplicar fondo a la vista principal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar panel principal y sombra
        for widget in self.findChildren(QFrame):
            if hasattr(widget, 'graphicsEffect'):
                if widget.graphicsEffect():
                    effect = widget.graphicsEffect()
                    if isinstance(effect, QGraphicsDropShadowEffect):
                        effect.setColor(QColor(colores.get("shadow", Qt.gray)))
                widget.setStyleSheet(self.estilo["styles"]["panel"])
        
        # Actualizar título principal
        for widget in self.findChildren(QLabel):
            if widget.text() == "Configuración":
                widget.setStyleSheet(self.estilo["styles"]["header"])
        
        # Actualizar scroll area
        self.scroll_area.setStyleSheet(self.estilo["styles"]["scroll"])
        
        # Actualizar títulos de paneles
        for widget in self.findChildren(QLabel):
            if widget.text() in ["Configuración de Interfaz", "Objetivos de Actividades", "Datos de Dirección", 
                               "Datos de Jefaturas", "Gaceta Oficial", "Preguntas y Respuestas de Seguridad"]:
                widget.setStyleSheet(self.estilo["styles"]["header"])
        
        # Actualizar labels de campos
        for widget in self.findChildren(QLabel):
            if widget.text() not in ["Configuración", "Configuración de Interfaz", "Objetivos de Actividades",
                                   "Datos de Dirección", "Datos de Jefaturas", "Gaceta Oficial", "Preguntas y Respuestas de Seguridad"]:
                widget.setStyleSheet(self.estilo["styles"]["title"])
        
        # Actualizar inputs
        for widget in self.findChildren((QLineEdit, QComboBox, QSpinBox)):
            widget.setStyleSheet(self.estilo["styles"]["input"])
        
        # Actualizar botones de radio
        for widget in self.findChildren(QRadioButton):
            widget.setStyleSheet(self.estilo["styles"]["radio"])
        
        # Actualizar checkboxes
        for widget in self.findChildren(QCheckBox):
            widget.setStyleSheet(self.estilo["styles"]["checkbox"])
        
        # Actualizar grupos
        for widget in self.findChildren(QGroupBox):
            widget.setStyleSheet(self.estilo["styles"]["grupo"])

        # Actualizar botón guardar
        if hasattr(self, 'boton_guardar'):
            self.boton_guardar.setStyleSheet(self.estilo["styles"]["boton"])
