from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout,
                             QGraphicsDropShadowEffect, QGroupBox, QRadioButton,
                             QSizePolicy, QSpacerItem, QSpinBox, QComboBox, QCheckBox,
                             QGridLayout, QLineEdit, QButtonGroup, QPushButton, 
                             QScrollArea, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class Ventana_configuracion(QFrame):
    # Señales simplificadas
    guardar_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la UI con el diseño original completo"""
        # Scroll area con estilo original
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
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
        self.crear_panel_interfaz_con_estilo()
        self.crear_panel_direccion_con_estilo()
        self.crear_panel_jefaturas_con_estilo()
        self.crear_boton_guardar_con_estilo()
        
        # Spacer final
        self.layout_main.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    # ========== PANEL INTERFAZ CON ESTILO ORIGINAL ==========
    
    def crear_panel_interfaz_con_estilo(self):
        """Crea panel de interfaz con el diseño original"""
        # Frame principal con sombra y bordes redondeados
        self.panel_interfaz = QFrame()
        self.panel_interfaz.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                min-width: 300px;
            }
        """)
        
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
        titulo.setStyleSheet(self.get_header_style())
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
        self.grupo_tema.setStyleSheet("""
            QGroupBox{
                font-size: 14px;
                font-weight: bold;
                color: #37474F;
                margin: 0;
                padding: 15px 12px;
                border: 2px solid #E3F2FD;
                border-radius: 8px;
                background: #FAFAFA;
                min-width: 200px;
            }
            QGroupBox::title{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                color: #1565C0;
            }
        """)
        
        layout_tema = QVBoxLayout()
        layout_tema.setSpacing(12)
        self.grupo_tema.setLayout(layout_tema)
        
        # Botones de radio con estilo
        self.tema_group = QButtonGroup()
        self.radio_tema_claro = QRadioButton("Tema Claro")
        self.radio_tema_oscuro = QRadioButton("Tema Oscuro")
        
        radio_style = """
            QRadioButton{
                font-size: 13px;
                color: #455A64;
                padding: 6px 5px;
                spacing: 8px;
                min-height: 20px;
            }
            QRadioButton::indicator{
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #90A4AE;
            }
            QRadioButton::indicator:checked{
                background-color: #4FC3F7;
                border: 2px solid #29B6F6;
            }
        """
        self.radio_tema_claro.setStyleSheet(radio_style)
        self.radio_tema_oscuro.setStyleSheet(radio_style)
        
        self.tema_group.addButton(self.radio_tema_claro)
        self.tema_group.addButton(self.radio_tema_oscuro)
        
        layout_tema.addWidget(self.radio_tema_claro)
        layout_tema.addWidget(self.radio_tema_oscuro)
        layout_tema.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # ===== GRUPO FUENTE CON ESTILO ORIGINAL =====
        self.grupo_fuente = QGroupBox("Configuración de Fuente")
        self.grupo_fuente.setMinimumWidth(200)
        self.grupo_fuente.setStyleSheet("""
            QGroupBox{
                font-size: 14px;
                font-weight: bold;
                color: #37474F;
                margin: 0;
                padding: 15px 12px;
                border: 2px solid #E3F2FD;
                border-radius: 8px;
                background: #FAFAFA;
                min-width: 200px;
            }
            QGroupBox::title{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                color: #1565C0;
            }
        """)
        
        layout_fuente = QVBoxLayout()
        layout_fuente.setSpacing(15)
        self.grupo_fuente.setLayout(layout_fuente)
        
        # Combobox de fuentes
        label_tipo = QLabel("Tipo de Letra")
        label_tipo.setStyleSheet("""
            QLabel{
                font-size: 12px; 
                margin: 0; 
                background: none; 
                font-weight: bold;
                color: #37474F;
            }
        """)
        layout_fuente.addWidget(label_tipo)
        
        self.combo_fuente = QComboBox()
        self.combo_fuente.addItems(["Arial", "Segoe UI", "Verdana", "Tahoma", "Georgia"])
        self.combo_fuente.setStyleSheet("""
            QComboBox{
                padding: 6px 10px;
                border: 1px solid #BDBDBD;
                border-radius: 6px;
                background: white;
                font-size: 12px;
                min-height: 12px;
                min-width: 120px;
            }
            QComboBox::drop-down{
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #757575;
            }
        """)
        layout_fuente.addWidget(self.combo_fuente)
        
        # Tamaño de fuente
        label_tamano = QLabel("Tamaño de la fuente")
        label_tamano.setStyleSheet("""
            QLabel{
                font-size: 12px; 
                margin: 0; 
                background: none; 
                font-weight: bold;
                color: #37474F;
            }
        """)
        layout_fuente.addWidget(label_tamano)
        
        self.spin_tamano = QSpinBox()
        self.spin_tamano.setStyleSheet("""
            QSpinBox{
                padding: 6px 10px;
                border: 1px solid #BDBDBD;
                border-radius: 6px;
                background: white;
                font-size: 12px;
                min-width: 80px;
            }
        """)
        self.spin_tamano.setMinimum(8)
        self.spin_tamano.setMaximum(18)
        self.spin_tamano.setValue(12)
        layout_fuente.addWidget(self.spin_tamano)
        
        # Checkbox de negrita
        self.check_negrita = QCheckBox("Negrita en títulos")
        self.check_negrita.setStyleSheet("""
            QCheckBox{
                font-size: 12px;
                color: #455A64;
                padding: 8px 0px;
                spacing: 8px;
            }
            QCheckBox::indicator{
                width: 16px;
                height: 16px;
                border: 2px solid #90A4AE;
                border-radius: 3px;
                background: white;
            }
            QCheckBox::indicator:checked{
                background-color: #4FC3F7;
                border: 2px solid #29B6F6;
            }
        """)
        layout_fuente.addWidget(self.check_negrita)
        layout_fuente.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Agregar grupos al layout horizontal
        layout_horizontal.addWidget(self.grupo_tema)
        layout_horizontal.addWidget(self.grupo_fuente)
        
        # Agregar panel al layout principal
        self.layout_main.addWidget(self.panel_interfaz)
    
    # ========== PANEL DIRECCIÓN CON ESTILO ORIGINAL ==========
    
    def crear_panel_direccion_con_estilo(self):
        """Crea panel de dirección con el diseño original"""
        # Frame principal
        self.panel_direccion = QFrame()
        self.panel_direccion.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                min-width: 300px;
            }
        """)
        
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
        titulo.setStyleSheet(self.get_header_style())
        titulo.setMinimumHeight(50)
        layout_panel.addWidget(titulo)
        
        # Contenedor del contenido
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(15, 20, 15, 20)
        contenido_frame.setLayout(layout_contenido)
        layout_panel.addWidget(contenido_frame)
        
        # ===== GRUPO DIRECCIÓN CON ESTILO ORIGINAL =====
        self.grupo_direccion = QGroupBox("Configuración de Dirección")
        self.grupo_direccion.setStyleSheet("""
            QGroupBox{
                font-size: 14px;
                font-weight: bold;
                color: #37474F;
                margin: 0;
                padding: 20px 15px;
                border: 2px solid #E3F2FD;
                border-radius: 8px;
                background: #FAFAFA;
                min-width: 250px;
            }
            QGroupBox::title{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                color: #1565C0;
            }
        """)
        
        # Layout grid para campos (diseño original en 2 columnas)
        layout_grid = QGridLayout()
        layout_grid.setVerticalSpacing(12)
        layout_grid.setHorizontalSpacing(15)
        self.grupo_direccion.setLayout(layout_grid)
        
        # Estilos para labels y entries
        label_style = """
            QLabel{
                font-size: 12px;
                font-weight: bold;
                color: #37474F;
                padding: 2px 0px;
            }
        """
        
        entry_style = """
            QLineEdit{
                padding: 8px 10px;
                border: 1px solid #BDBDBD;
                border-radius: 6px;
                background: white;
                font-size: 12px;
                min-width: 150px;
            }
            QLineEdit:focus{
                border: 1px solid #4FC3F7;
                background: #F5FDFF;
            }
        """
        
        # Crear campos
        self.entry_estado = QLineEdit()
        self.entry_estado.setStyleSheet(entry_style)
        self.entry_estado.setPlaceholderText("Ingrese el estado")
        
        self.entry_municipio = QLineEdit()
        self.entry_municipio.setStyleSheet(entry_style)
        self.entry_municipio.setPlaceholderText("Ingrese el municipio")
        
        self.entry_parroquia = QLineEdit()
        self.entry_parroquia.setStyleSheet(entry_style)
        self.entry_parroquia.setPlaceholderText("Ingrese la parroquia")
        
        self.entry_institucion = QLineEdit()
        self.entry_institucion.setStyleSheet(entry_style)
        self.entry_institucion.setPlaceholderText("Ingrese comunidad o institución")
        
        # Agregar al grid (diseño original: 2 columnas)
        layout_grid.addWidget(QLabel("Estado:"), 0, 0)
        layout_grid.addWidget(self.entry_estado, 0, 1)
        layout_grid.addWidget(QLabel("Municipio:"), 1, 0)
        layout_grid.addWidget(self.entry_municipio, 1, 1)
        layout_grid.addWidget(QLabel("Parroquia:"), 2, 0)
        layout_grid.addWidget(self.entry_parroquia, 2, 1)
        layout_grid.addWidget(QLabel("Comunidad/Institución:"), 3, 0)
        layout_grid.addWidget(self.entry_institucion, 3, 1)
        
        layout_contenido.addWidget(self.grupo_direccion)
        self.layout_main.addWidget(self.panel_direccion)
    
    # ========== PANEL JEFATURAS CON ESTILO ORIGINAL ==========
    
    def crear_panel_jefaturas_con_estilo(self):
        """Crea panel de jefaturas con el diseño original"""
        # Frame principal
        self.panel_jefaturas = QFrame()
        self.panel_jefaturas.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                min-width: 300px;
            }
        """)
        
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
        titulo.setStyleSheet(self.get_header_style())
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
        self.grupo_coordinacion.setStyleSheet("""
            QGroupBox{
                font-size: 14px;
                font-weight: bold;
                color: #37474F;
                margin: 0;
                padding: 20px 15px;
                border: 2px solid #E3F2FD;
                border-radius: 8px;
                background: #FAFAFA;
                min-width: 250px;
            }
            QGroupBox::title{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                color: #1565C0;
            }
        """)
        
        layout_coordinacion = QVBoxLayout()
        layout_coordinacion.setSpacing(15)
        self.grupo_coordinacion.setLayout(layout_coordinacion)
        
        # Campos coordinación
        label_style = """
            QLabel{
                font-size: 12px;
                font-weight: bold;
                color: #37474F;
                padding: 2px 0px;
            }
        """
        
        entry_style = """
            QLineEdit{
                padding: 8px 10px;
                border: 1px solid #BDBDBD;
                border-radius: 6px;
                background: white;
                font-size: 12px;
            }
            QLineEdit:focus{
                border: 1px solid #4FC3F7;
                background: #F5FDFF;
            }
        """
        
        self.label_nombre_coord = QLabel("Nombre completo:")
        self.label_nombre_coord.setStyleSheet(label_style)
        self.entry_nombre_coord = QLineEdit()
        self.entry_nombre_coord.setStyleSheet(entry_style)
        self.entry_nombre_coord.setPlaceholderText("Ingrese nombre completo")
        
        self.label_cedula_coord = QLabel("Cédula de identidad:")
        self.label_cedula_coord.setStyleSheet(label_style)
        self.entry_cedula_coord = QLineEdit()
        self.entry_cedula_coord.setStyleSheet(entry_style)
        self.entry_cedula_coord.setPlaceholderText("Ej: V-12345678")
        
        layout_coordinacion.addWidget(self.label_nombre_coord)
        layout_coordinacion.addWidget(self.entry_nombre_coord)
        layout_coordinacion.addWidget(self.label_cedula_coord)
        layout_coordinacion.addWidget(self.entry_cedula_coord)
        
        # ===== GRUPO GOBERNACIÓN CON ESTILO ORIGINAL =====
        self.grupo_gobernacion = QGroupBox("Jefa de Gobernación")
        self.grupo_gobernacion.setStyleSheet("""
            QGroupBox{
                font-size: 14px;
                font-weight: bold;
                color: #37474F;
                margin: 0;
                padding: 20px 15px;
                border: 2px solid #E3F2FD;
                border-radius: 8px;
                background: #FAFAFA;
                min-width: 250px;
            }
            QGroupBox::title{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px 0 6px;
                color: #1565C0;
            }
        """)
        
        layout_gobernacion = QVBoxLayout()
        layout_gobernacion.setSpacing(15)
        self.grupo_gobernacion.setLayout(layout_gobernacion)
        
        self.label_nombre_gob = QLabel("Nombre completo:")
        self.label_nombre_gob.setStyleSheet(label_style)
        self.entry_nombre_gob = QLineEdit()
        self.entry_nombre_gob.setStyleSheet(entry_style)
        self.entry_nombre_gob.setPlaceholderText("Ingrese nombre completo")
        
        self.label_cedula_gob = QLabel("Cédula de identidad:")
        self.label_cedula_gob.setStyleSheet(label_style)
        self.entry_cedula_gob = QLineEdit()
        self.entry_cedula_gob.setStyleSheet(entry_style)
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
    
    # ========== BOTÓN GUARDAR CON ESTILO ORIGINAL ==========
    
    def crear_boton_guardar_con_estilo(self):
        """Crea botón de guardar con el diseño original"""
        layout_boton = QHBoxLayout()
        
        # Spacer izquierdo
        layout_boton.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Botón guardar con estilo original
        self.boton_guardar = QPushButton("Guardar Cambios")
        self.boton_guardar.setStyleSheet(self.get_btn_style())
        self.boton_guardar.clicked.connect(self.guardar_clicked.emit)
        layout_boton.addWidget(self.boton_guardar)
        
        # Spacer derecho
        layout_boton.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.layout_main.addLayout(layout_boton)
    
    # ========== MÉTODOS PÚBLICOS PARA EL CONTROLADOR ==========
    
    def obtener_valores(self):
        """Retorna todos los valores de los widgets"""
        return {
            "interfaz": {
                "tema": "Claro" if self.radio_tema_claro.isChecked() else "Oscuro",
                "fuente": self.combo_fuente.currentText(),
                "tamaño": self.spin_tamano.value(),
                "negrita": self.check_negrita.isChecked()
            },
            "direccion": {
                "estado": self.entry_estado.text(),
                "municipio": self.entry_municipio.text(),
                "parroquia": self.entry_parroquia.text(),
                "institucion": self.entry_institucion.text()
            },
            "jefaturas": {
                "nombre_coordinacion": self.entry_nombre_coord.text(),
                "cedula_coordinacion": self.entry_cedula_coord.text(),
                "nombre_gobernacion": self.entry_nombre_gob.text(),
                "cedula_gobernacion": self.entry_cedula_gob.text()
            }
        }
    
    def establecer_valores(self, datos):
        """Establece valores en los widgets"""
        if not datos:
            return
            
        # Interfaz
        if "interfaz" in datos:
            interfaz = datos["interfaz"]
            
            # Tema
            if interfaz.get("tema") == "Claro":
                self.radio_tema_claro.setChecked(True)
            else:
                self.radio_tema_oscuro.setChecked(True)
            
            # Fuente
            fuente = interfaz.get("fuente", "Arial")
            index = self.combo_fuente.findText(fuente)
            if index >= 0:
                self.combo_fuente.setCurrentIndex(index)
            
            # Tamaño
            self.spin_tamano.setValue(interfaz.get("tamaño", 12))
            
            # Negrita
            self.check_negrita.setChecked(interfaz.get("negrita", False))
        
        # Dirección
        if "direccion" in datos:
            direccion = datos["direccion"]
            self.entry_estado.setText(direccion.get("estado", ""))
            self.entry_municipio.setText(direccion.get("municipio", ""))
            self.entry_parroquia.setText(direccion.get("parroquia", ""))
            self.entry_institucion.setText(direccion.get("institucion", ""))
        
        # Jefaturas
        if "jefaturas" in datos:
            jefaturas = datos["jefaturas"]
            self.entry_nombre_coord.setText(jefaturas.get("nombre_coordinacion", ""))
            self.entry_cedula_coord.setText(jefaturas.get("cedula_coordinacion", ""))
            self.entry_nombre_gob.setText(jefaturas.get("nombre_gobernacion", ""))
            self.entry_cedula_gob.setText(jefaturas.get("cedula_gobernacion", ""))
    
    def limpiar_campos(self):
        """Limpia todos los campos"""
        # Interfaz
        self.radio_tema_claro.setChecked(True)
        self.combo_fuente.setCurrentIndex(0)
        self.spin_tamano.setValue(12)
        self.check_negrita.setChecked(False)
        
        # Dirección
        self.entry_estado.clear()
        self.entry_municipio.clear()
        self.entry_parroquia.clear()
        self.entry_institucion.clear()
        
        # Jefaturas
        self.entry_nombre_coord.clear()
        self.entry_cedula_coord.clear()
        self.entry_nombre_gob.clear()
        self.entry_cedula_gob.clear()
    
    # ========== MÉTODOS DE ESTILO ==========
    
    def get_header_style(self):
        COLOR_PRIMARIO = "#005a6e"
        return f"""
            QLabel{{
                font-size: 16px; 
                font-weight: bold; 
                background: {COLOR_PRIMARIO};
                color: white;
                padding: 15px 15px;
                margin: 0;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
        """
    
    def get_btn_style(self):
        return """
            QPushButton{
                background: #005a6e;
                color: White;
                font-weight: bold;
                font-size: 18px;
                min-width: 100px;
                padding: 15px;
                border-radius: 15px;
                text-align: left;
                border: none;
            }  
            QPushButton:hover{
                background: #007a94;
            }    
            QPushButton:pressed{
                background: #00485a;
            }
        """