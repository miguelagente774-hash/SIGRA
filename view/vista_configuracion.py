from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout,
                             QGraphicsDropShadowEffect, QGroupBox, QRadioButton,
                             QSizePolicy, QSpacerItem, QSpinBox, QComboBox, QCheckBox,
                             QGridLayout, QLineEdit, QButtonGroup, QPushButton, 
                             QScrollArea, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"

HEADER_STYLE = f"""
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

BTN_STYLE = """
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
        }"""


class Ventana_configuracion(QFrame):
    def __init__(self):
        super().__init__()
        
        # Crear scroll area
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
        
        # Contador para seguimiento de cambios de tamaño
        self.current_width = self.width()
        
        self.Panel_configuracion_interfaz()
        self.Panel_configuracion_datos_direccion()
        self.Panel_configuracion_jefes()  # Nuevo panel para jefes
        self.crear_boton_guardar()  # Botón guardar

        mover_arriba = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout_main.addItem(mover_arriba)

    def Panel_configuracion_interfaz(self):
        # Layout principal del panel
        layout_panel = QVBoxLayout()
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)

        # Frame contenedor responsivo
        Panel_configuracion = QFrame()
        Panel_configuracion.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                min-width: 300px;
            }
        """)
        Panel_configuracion.setLayout(layout_panel)
        
        # Sombra adaptable
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        Panel_configuracion.setGraphicsEffect(sombra)

        # Título responsivo
        titulo = QLabel("Configuración de Interfaz")
        titulo.setStyleSheet(HEADER_STYLE)
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout_panel.addWidget(titulo)

        # Contenedor del contenido responsivo
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        self.layout_contenido_interfaz = QVBoxLayout()
        self.layout_contenido_interfaz.setContentsMargins(15, 20, 15, 20)
        self.layout_contenido_interfaz.setSpacing(20)
        contenido_frame.setLayout(self.layout_contenido_interfaz)
        layout_panel.addWidget(contenido_frame)

        # Layout horizontal responsivo
        self.layout_horizontal_interfaz = QHBoxLayout()
        self.layout_horizontal_interfaz.setSpacing(20)
        self.layout_contenido_interfaz.addLayout(self.layout_horizontal_interfaz)

        # Área de tema responsiva
        self.crear_area_tema()
        
        # Área de fuentes responsiva
        self.crear_area_fuentes()

        self.layout_main.addWidget(Panel_configuracion)

    def crear_area_tema(self):
        """Crear área de tema de forma responsiva"""
        layout_tema = QVBoxLayout()
        layout_tema.setSpacing(12)
        self.area_tema = QGroupBox("Tema de la aplicación")
        self.area_tema.setLayout(layout_tema)
        self.area_tema.setMinimumWidth(200)
        
        # Estilo base que se adaptará
        self.area_tema.setStyleSheet("""
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
        
        # Grupo de botones para tema
        self.tema_group = QButtonGroup()
        radius_claro = QRadioButton("Tema Claro")
        radius_Oscuro = QRadioButton("Tema Oscuro")
        
        # Estilos responsivos para radio buttons
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
        radius_claro.setStyleSheet(radio_style)
        radius_Oscuro.setStyleSheet(radio_style)
        
        self.tema_group.addButton(radius_claro)
        self.tema_group.addButton(radius_Oscuro)
        
        layout_tema.addWidget(radius_claro)
        layout_tema.addWidget(radius_Oscuro)
        
        # Spacer flexible
        layout_tema.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.layout_horizontal_interfaz.addWidget(self.area_tema)

    def crear_area_fuentes(self):
        """Crear área de fuentes de forma responsiva"""
        layout_fuente = QVBoxLayout()
        layout_fuente.setSpacing(15)
        self.fuente = QGroupBox("Configuración de Fuente")
        self.fuente.setLayout(layout_fuente)
        self.fuente.setMinimumWidth(200)
        
        self.fuente.setStyleSheet("""
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

        # Tipo de letra
        tipo_letra = QLabel("Tipo de Letra")
        tipo_letra.setStyleSheet("""
            QLabel{
                font-size: 12px; 
                margin: 0; 
                background: none; 
                font-weight: bold;
                color: #37474F;
            }
        """)
        layout_fuente.addWidget(tipo_letra)

        elementos = ["Arial", "Segoe UI", "Verdana", "Tahoma", "Georgia"]
        self.tipo_letras = QComboBox()
        self.tipo_letras.setStyleSheet("""
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
        self.tipo_letras.addItems(elementos)
        layout_fuente.addWidget(self.tipo_letras)

        # Tamaño de fuente
        titulo_tamaño_fuente = QLabel("Tamaño de la fuente")
        titulo_tamaño_fuente.setStyleSheet("""
            QLabel{
                font-size: 12px; 
                margin: 0; 
                background: none; 
                font-weight: bold;
                color: #37474F;
            }
        """)
        layout_fuente.addWidget(titulo_tamaño_fuente) 
        
        self.tamaño_fuente = QSpinBox()
        self.tamaño_fuente.setStyleSheet("""
            QSpinBox{
                padding: 6px 10px;
                border: 1px solid #BDBDBD;
                border-radius: 6px;
                background: white;
                font-size: 12px;
                min-width: 80px;
            }
        """)
        self.tamaño_fuente.setMinimum(8)
        self.tamaño_fuente.setMaximum(18)
        self.tamaño_fuente.setValue(12)
        layout_fuente.addWidget(self.tamaño_fuente)
        
        # Checkbox de negrita
        self.fuente_negrita = QCheckBox("Negrita en títulos")
        self.fuente_negrita.setStyleSheet("""
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
        layout_fuente.addWidget(self.fuente_negrita)

        # Spacer flexible
        layout_fuente.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.layout_horizontal_interfaz.addWidget(self.fuente)

    def Panel_configuracion_datos_direccion(self):
        layout_datos = QVBoxLayout()
        layout_datos.setSpacing(0)
        self.panel_datos = QFrame()
        self.panel_datos.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                min-width: 300px;
            }
        """)
        self.panel_datos.setLayout(layout_datos)

        # Título responsivo
        titulo = QLabel("Configuración de Datos de Dirección")
        titulo.setStyleSheet(HEADER_STYLE)
        titulo.setMinimumHeight(50)
        layout_datos.addWidget(titulo)

        # Contenedor del contenido responsivo
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        self.layout_contenido_datos = QVBoxLayout()
        self.layout_contenido_datos.setContentsMargins(15, 20, 15, 20)
        contenido_frame.setLayout(self.layout_contenido_datos)
        layout_datos.addWidget(contenido_frame)

        # Área de dirección responsiva
        self.crear_area_direccion()

        self.layout_main.addWidget(self.panel_datos)

    def crear_area_direccion(self):
        """Crear área de dirección de forma responsiva"""
        self.direccion = QGroupBox("Configuración de Dirección")
        self.direccion.setStyleSheet("""
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
        
        self.layout_direccion = QGridLayout()
        self.layout_direccion.setVerticalSpacing(12)
        self.layout_direccion.setHorizontalSpacing(15)
        self.direccion.setLayout(self.layout_direccion)

        # Estilos responsivos
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

        # Crear campos de formulario
        self.crear_campo_formulario(0, "Estado:", "Ingrese el estado", label_style, entry_style)
        self.crear_campo_formulario(1, "Municipio:", "Ingrese el municipio", label_style, entry_style)
        self.crear_campo_formulario(2, "Parroquia:", "Ingrese la parroquia", label_style, entry_style)
        self.crear_campo_formulario(3, "Comunidad/Institución:", "Ingrese comunidad o institución", label_style, entry_style)

        self.layout_contenido_datos.addWidget(self.direccion)

    def crear_campo_formulario(self, fila, texto_label, placeholder, label_style, entry_style):
        """Crear campo de formulario responsivo"""
        label = QLabel(texto_label)
        label.setStyleSheet(label_style)
        
        entry = QLineEdit()
        entry.setStyleSheet(entry_style)
        entry.setPlaceholderText(placeholder)
        
        # Distribución responsiva en grid
        if fila % 2 == 0:
            # Campos en columnas pares (izquierda)
            self.layout_direccion.addWidget(label, fila, 0)
            self.layout_direccion.addWidget(entry, fila + 1, 0)
        else:
            # Campos en columnas impares (derecha)
            self.layout_direccion.addWidget(label, fila - 1, 1)
            self.layout_direccion.addWidget(entry, fila, 1)

    def Panel_configuracion_jefes(self):
        """Nuevo panel para datos de jefes de coordinación y gobernación"""
        layout_jefes = QVBoxLayout()
        layout_jefes.setSpacing(0)
        
        panel_jefes = QFrame()
        panel_jefes.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                min-width: 300px;
            }
        """)
        panel_jefes.setLayout(layout_jefes)
        
        # Sombra
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.gray)
        sombra.setOffset(1, 1)
        panel_jefes.setGraphicsEffect(sombra)

        # Título del panel
        titulo = QLabel("Datos de Jefaturas")
        titulo.setStyleSheet(HEADER_STYLE)
        titulo.setMinimumHeight(50)
        layout_jefes.addWidget(titulo)

        # Contenedor del contenido
        contenido_frame = QFrame()
        contenido_frame.setStyleSheet("QFrame{ background: transparent; margin: 0; padding: 0; }")
        layout_contenido = QVBoxLayout()
        layout_contenido.setContentsMargins(15, 20, 15, 20)
        layout_contenido.setSpacing(25)
        contenido_frame.setLayout(layout_contenido)
        layout_jefes.addWidget(contenido_frame)

        # Layout horizontal para los dos grupos de jefaturas
        layout_horizontal_jefes = QHBoxLayout()
        layout_horizontal_jefes.setSpacing(20)
        layout_contenido.addLayout(layout_horizontal_jefes)

        # Grupo para Jefe de Coordinación
        grupo_coordinacion = QGroupBox("Jefe de Coordinación")
        grupo_coordinacion.setStyleSheet("""
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
        grupo_coordinacion.setLayout(layout_coordinacion)

        # Campos para Jefe de Coordinación
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

        # Nombre Jefe Coordinación
        label_nombre_coord = QLabel("Nombre completo:")
        label_nombre_coord.setStyleSheet(label_style)
        layout_coordinacion.addWidget(label_nombre_coord)
        
        self.entry_nombre_coord = QLineEdit()
        self.entry_nombre_coord.setStyleSheet(entry_style)
        self.entry_nombre_coord.setPlaceholderText("Ingrese nombre completo")
        layout_coordinacion.addWidget(self.entry_nombre_coord)

        # Cédula Jefe Coordinación
        label_cedula_coord = QLabel("Cédula de identidad:")
        label_cedula_coord.setStyleSheet(label_style)
        layout_coordinacion.addWidget(label_cedula_coord)
        
        self.entry_cedula_coord = QLineEdit()
        self.entry_cedula_coord.setStyleSheet(entry_style)
        self.entry_cedula_coord.setPlaceholderText("Ej: V-12345678")
        layout_coordinacion.addWidget(self.entry_cedula_coord)

        # Grupo para Jefa de Gobernación
        grupo_gobernacion = QGroupBox("Jefa de Gobernación")
        grupo_gobernacion.setStyleSheet("""
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
        grupo_gobernacion.setLayout(layout_gobernacion)

        # Campos para Jefa de Gobernación
        label_nombre_gob = QLabel("Nombre completo:")
        label_nombre_gob.setStyleSheet(label_style)
        layout_gobernacion.addWidget(label_nombre_gob)
        
        self.entry_nombre_gob = QLineEdit()
        self.entry_nombre_gob.setStyleSheet(entry_style)
        self.entry_nombre_gob.setPlaceholderText("Ingrese nombre completo")
        layout_gobernacion.addWidget(self.entry_nombre_gob)

        label_cedula_gob = QLabel("Cédula de identidad:")
        label_cedula_gob.setStyleSheet(label_style)
        layout_gobernacion.addWidget(label_cedula_gob)
        
        self.entry_cedula_gob = QLineEdit()
        self.entry_cedula_gob.setStyleSheet(entry_style)
        self.entry_cedula_gob.setPlaceholderText("Ej: V-12345678")
        layout_gobernacion.addWidget(self.entry_cedula_gob)

        # Agregar ambos grupos al layout horizontal
        layout_horizontal_jefes.addWidget(grupo_coordinacion)
        layout_horizontal_jefes.addWidget(grupo_gobernacion)

        # Hacer que los grupos se expandan equitativamente
        layout_horizontal_jefes.setStretch(0, 1)
        layout_horizontal_jefes.setStretch(1, 1)

        self.layout_main.addWidget(panel_jefes)

    def crear_boton_guardar(self):
        """Crear botón de guardar cambios"""
        layout_boton = QHBoxLayout()
        
        # Spacer izquierdo
        layout_boton.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Botón guardar
        self.boton_guardar = QPushButton("Guardar Cambios")
        self.boton_guardar.setStyleSheet(BTN_STYLE)
        self.boton_guardar.clicked.connect(self.guardar_cambios)
        layout_boton.addWidget(self.boton_guardar)
        
        # Spacer derecho
        layout_boton.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.layout_main.addLayout(layout_boton)

    def guardar_cambios(self):
        """Función para guardar todos los cambios"""
        print("Guardando cambios...")
        
        # Aquí puedes agregar la lógica para guardar los datos
        # Por ejemplo:
        
        # Datos de dirección
        print("Datos de dirección guardados")
        
        # Datos de jefaturas
        nombre_coord = self.entry_nombre_coord.text()
        cedula_coord = self.entry_cedula_coord.text()
        nombre_gob = self.entry_nombre_gob.text()
        cedula_gob = self.entry_cedula_gob.text()
        
        print(f"Jefe Coordinación: {nombre_coord} - {cedula_coord}")
        print(f"Jefa Gobernación: {nombre_gob} - {cedula_gob}")
        
        # Configuración de interfaz
        print("Configuración de interfaz guardada")
        
        # Aquí puedes agregar la lógica para guardar en base de datos o archivos

    def ajustar_layout_responsive(self):
        """Ajustar layout según el tamaño actual"""
        ancho = self.width()
        
        if hasattr(self, 'layout_horizontal_interfaz'):
            if ancho <= 600:
                self.cambiar_a_vertical()
            elif ancho <= 900:
                self.cambiar_a_horizontal()
                self.layout_horizontal_interfaz.setSpacing(15)
            else:
                self.cambiar_a_horizontal()
                self.layout_horizontal_interfaz.setSpacing(25)

    def cambiar_a_vertical(self):
        """Cambiar disposición a vertical para móviles"""
        if hasattr(self, 'layout_horizontal_interfaz') and self.layout_horizontal_interfaz.count() > 0:
            widgets = []
            for i in reversed(range(self.layout_horizontal_interfaz.count())):
                item = self.layout_horizontal_interfaz.itemAt(i)
                if item.widget():
                    widgets.append(item.widget())
                    self.layout_horizontal_interfaz.removeWidget(item.widget())
            
            for widget in widgets:
                self.layout_contenido_interfaz.addWidget(widget)

    def cambiar_a_horizontal(self):
        """Cambiar disposición a horizontal para tablets y desktop"""
        if hasattr(self, 'layout_horizontal_interfaz'):
            for i in reversed(range(self.layout_horizontal_interfaz.count())):
                item = self.layout_horizontal_interfaz.itemAt(i)
                if item.widget():
                    self.layout_horizontal_interfaz.removeWidget(item.widget())
            
            if hasattr(self, 'area_tema'):
                self.layout_horizontal_interfaz.addWidget(self.area_tema)
            if hasattr(self, 'fuente'):
                self.layout_horizontal_interfaz.addWidget(self.fuente)