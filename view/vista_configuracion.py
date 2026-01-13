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
    valor_cambiado = pyqtSignal(str, object)  # (campo, valor)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Configura solo la UI, sin lógica de negocio"""
        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.scroll_widget = QWidget()
        self.layout_main = QVBoxLayout(self.scroll_widget)
        self.layout_main.setContentsMargins(20, 15, 20, 15)
        self.layout_main.setSpacing(20)
        
        self.scroll_area.setWidget(self.scroll_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)
        
        # Crear widgets
        self.crear_panel_interfaz()
        self.crear_panel_direccion()
        self.crear_panel_jefaturas()
        self.crear_boton_guardar()
        
        self.layout_main.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    # ========== MÉTODOS PARA CREAR WIDGETS ==========
    
    def crear_panel_interfaz(self):
        """Crea widgets de interfaz"""
        # Frame principal
        self.frame_interfaz = QFrame()
        self.frame_interfaz.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        # Título
        self.label_titulo_interfaz = QLabel("Configuración de Interfaz")
        self.label_titulo_interfaz.setStyleSheet(self.get_header_style())
        
        # Widgets de tema
        self.radio_tema_claro = QRadioButton("Tema Claro")
        self.radio_tema_oscuro = QRadioButton("Tema Oscuro")
        self.tema_group = QButtonGroup()
        self.tema_group.addButton(self.radio_tema_claro)
        self.tema_group.addButton(self.radio_tema_oscuro)
        
        # Widgets de fuente
        self.combo_fuente = QComboBox()
        self.combo_fuente.addItems(["Arial", "Segoe UI", "Verdana", "Tahoma", "Georgia"])
        
        self.spin_tamano = QSpinBox()
        self.spin_tamano.setRange(8, 18)
        self.spin_tamano.setValue(12)
        
        self.check_negrita = QCheckBox("Negrita en títulos")
        
        # Layout
        layout_interfaz = QVBoxLayout(self.frame_interfaz)
        layout_interfaz.addWidget(self.label_titulo_interfaz)
        
        # Grupo tema
        grupo_tema = QGroupBox("Tema de la aplicación")
        layout_tema = QVBoxLayout()
        layout_tema.addWidget(self.radio_tema_claro)
        layout_tema.addWidget(self.radio_tema_oscuro)
        grupo_tema.setLayout(layout_tema)
        
        # Grupo fuente
        grupo_fuente = QGroupBox("Configuración de Fuente")
        layout_fuente = QVBoxLayout()
        layout_fuente.addWidget(QLabel("Tipo de Letra:"))
        layout_fuente.addWidget(self.combo_fuente)
        layout_fuente.addWidget(QLabel("Tamaño:"))
        layout_fuente.addWidget(self.spin_tamano)
        layout_fuente.addWidget(self.check_negrita)
        grupo_fuente.setLayout(layout_fuente)
        
        # Layout horizontal para grupos
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(grupo_tema)
        layout_horizontal.addWidget(grupo_fuente)
        
        layout_interfaz.addLayout(layout_horizontal)
        self.layout_main.addWidget(self.frame_interfaz)
    
    def crear_panel_direccion(self):
        """Crea widgets de dirección"""
        self.frame_direccion = QFrame()
        self.frame_direccion.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        # Título
        self.label_titulo_direccion = QLabel("Configuración de Datos de Dirección")
        self.label_titulo_direccion.setStyleSheet(self.get_header_style())
        
        # Campos de entrada
        self.entry_estado = QLineEdit()
        self.entry_estado.setPlaceholderText("Ingrese el estado")
        
        self.entry_municipio = QLineEdit()
        self.entry_municipio.setPlaceholderText("Ingrese el municipio")
        
        self.entry_parroquia = QLineEdit()
        self.entry_parroquia.setPlaceholderText("Ingrese la parroquia")
        
        self.entry_institucion = QLineEdit()
        self.entry_institucion.setPlaceholderText("Ingrese comunidad o institución")
        
        # Layout
        layout_direccion = QVBoxLayout(self.frame_direccion)
        layout_direccion.addWidget(self.label_titulo_direccion)
        
        grupo_direccion = QGroupBox("Configuración de Dirección")
        layout_grupo = QGridLayout()
        
        layout_grupo.addWidget(QLabel("Estado:"), 0, 0)
        layout_grupo.addWidget(self.entry_estado, 0, 1)
        layout_grupo.addWidget(QLabel("Municipio:"), 1, 0)
        layout_grupo.addWidget(self.entry_municipio, 1, 1)
        layout_grupo.addWidget(QLabel("Parroquia:"), 2, 0)
        layout_grupo.addWidget(self.entry_parroquia, 2, 1)
        layout_grupo.addWidget(QLabel("Institución:"), 3, 0)
        layout_grupo.addWidget(self.entry_institucion, 3, 1)
        
        grupo_direccion.setLayout(layout_grupo)
        layout_direccion.addWidget(grupo_direccion)
        self.layout_main.addWidget(self.frame_direccion)
    
    def crear_panel_jefaturas(self):
        """Crea widgets de jefaturas"""
        self.frame_jefaturas = QFrame()
        self.frame_jefaturas.setStyleSheet("""
            QFrame{
                background: rgba(255, 255, 255, 0.95);
                padding: 0;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        # Título
        self.label_titulo_jefaturas = QLabel("Datos de Jefaturas")
        self.label_titulo_jefaturas.setStyleSheet(self.get_header_style())
        
        # Campos coordinación
        self.entry_nombre_coord = QLineEdit()
        self.entry_nombre_coord.setPlaceholderText("Nombre completo")
        
        self.entry_cedula_coord = QLineEdit()
        self.entry_cedula_coord.setPlaceholderText("V-12345678")
        
        # Campos gobernación
        self.entry_nombre_gob = QLineEdit()
        self.entry_nombre_gob.setPlaceholderText("Nombre completo")
        
        self.entry_cedula_gob = QLineEdit()
        self.entry_cedula_gob.setPlaceholderText("V-12345678")
        
        # Layout
        layout_jefaturas = QVBoxLayout(self.frame_jefaturas)
        layout_jefaturas.addWidget(self.label_titulo_jefaturas)
        
        layout_horizontal = QHBoxLayout()
        
        # Grupo coordinación
        grupo_coord = QGroupBox("Jefe de Coordinación")
        layout_coord = QVBoxLayout()
        layout_coord.addWidget(QLabel("Nombre:"))
        layout_coord.addWidget(self.entry_nombre_coord)
        layout_coord.addWidget(QLabel("Cédula:"))
        layout_coord.addWidget(self.entry_cedula_coord)
        grupo_coord.setLayout(layout_coord)
        
        # Grupo gobernación
        grupo_gob = QGroupBox("Jefa de Gobernación")
        layout_gob = QVBoxLayout()
        layout_gob.addWidget(QLabel("Nombre:"))
        layout_gob.addWidget(self.entry_nombre_gob)
        layout_gob.addWidget(QLabel("Cédula:"))
        layout_gob.addWidget(self.entry_cedula_gob)
        grupo_gob.setLayout(layout_gob)
        
        layout_horizontal.addWidget(grupo_coord)
        layout_horizontal.addWidget(grupo_gob)
        layout_jefaturas.addLayout(layout_horizontal)
        self.layout_main.addWidget(self.frame_jefaturas)
    
    def crear_boton_guardar(self):
        """Crea botón de guardar"""
        self.boton_guardar = QPushButton("Guardar Cambios")
        self.boton_guardar.setStyleSheet(self.get_btn_style())
        self.boton_guardar.clicked.connect(self.guardar_clicked.emit)
        
        layout_boton = QHBoxLayout()
        layout_boton.addStretch()
        layout_boton.addWidget(self.boton_guardar)
        layout_boton.addStretch()
        
        self.layout_main.addLayout(layout_boton)
    
    # ========== MÉTODOS PÚBLICOS (GETTERS/SETTERS) ==========
    
    def obtener_valores(self):
        """Retorna todos los valores actuales de los widgets"""
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
        # Interfaz
        if datos.get("interfaz"):
            interfaz = datos["interfaz"]
            if interfaz.get("tema") == "Claro":
                self.radio_tema_claro.setChecked(True)
            else:
                self.radio_tema_oscuro.setChecked(True)
            
            index = self.combo_fuente.findText(interfaz.get("fuente", "Arial"))
            if index >= 0:
                self.combo_fuente.setCurrentIndex(index)
            
            self.spin_tamano.setValue(interfaz.get("tamaño", 12))
            self.check_negrita.setChecked(interfaz.get("negrita", False))
        
        # Dirección
        if datos.get("direccion"):
            direccion = datos["direccion"]
            self.entry_estado.setText(direccion.get("estado", ""))
            self.entry_municipio.setText(direccion.get("municipio", ""))
            self.entry_parroquia.setText(direccion.get("parroquia", ""))
            self.entry_institucion.setText(direccion.get("institucion", ""))
        
        # Jefaturas
        if datos.get("jefaturas"):
            jefaturas = datos["jefaturas"]
            self.entry_nombre_coord.setText(jefaturas.get("nombre_coordinacion", ""))
            self.entry_cedula_coord.setText(jefaturas.get("cedula_coordinacion", ""))
            self.entry_nombre_gob.setText(jefaturas.get("nombre_gobernacion", ""))
            self.entry_cedula_gob.setText(jefaturas.get("cedula_gobernacion", ""))
    
    def limpiar_campos(self):
        """Limpia todos los campos"""
        self.radio_tema_claro.setChecked(True)
        self.combo_fuente.setCurrentIndex(0)
        self.spin_tamano.setValue(12)
        self.check_negrita.setChecked(False)
        
        self.entry_estado.clear()
        self.entry_municipio.clear()
        self.entry_parroquia.clear()
        self.entry_institucion.clear()
        
        self.entry_nombre_coord.clear()
        self.entry_cedula_coord.clear()
        self.entry_nombre_gob.clear()
        self.entry_cedula_gob.clear()
    
    def mostrar_error(self, campo, mensaje):
        """Marca un campo con error"""
        # Puedes implementar marcado visual de errores aquí
        print(f"Error en {campo}: {mensaje}")
    
    def limpiar_errores(self):
        """Limpia todos los marcadores de error"""
        pass
    
    # ========== ESTILOS ==========
    
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
                border: none;
            }  
            QPushButton:hover{
                background: #007a94;
            }    
            QPushButton:pressed{
                background: #00485a;
            }
        """