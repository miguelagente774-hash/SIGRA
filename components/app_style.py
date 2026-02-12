from models.conexion_db import ConexionDB
from PyQt5.QtCore import QObject, pyqtSignal

# ==Clase para gestionar los estilos de toda la aplicación==
class AppStyle(QObject):
    # PyQtSignal para Estilos_Actualizados
    estilos_actualizados = pyqtSignal()
    vistas_registradas = []
    # Variables de clase para configuración global
    FONT_SIZE = 12
    FONT_BOLD = False
    THEME = "claro" 
    FONT_FAMILY = "Arial" 
    
    # Colores por tema
    THEME_COLORS = {
        "claro": {
            "bg_primary": "rgba(255, 255, 255, 0.95)",
            "bg_secondary": "#FAFAFA",
            "bg_fondo": "#E3EFF3",
            "bg_panel": "rgba(255, 255, 255, 0.9)",
            "primary": "#005a6e",
            "secondary": "#F44336",
            "text_primary": "#000000",
            "text_secondary": "#37474F",
            "text_label": "#333333",
            "border": "#005a6e",
            "border_light": "#E3F2FD",
            "border_input": "#005a6e",
            "shadow": "gray",
            "table_header": "#005a6e",
            "table_header_secondary": "#256d7e",
            "table_bg": "#FFFFFF",
            "card_bg": "white",
            "input_bg": "#FFFFFF",
            "scroll_bg": "#f0f0f0",
            "scroll_handle": "#c0c0c0",
            "boton": "#005a6e",
            "boton_hover": "#00485a",
            "boton_pressed": "#003441"
        },
        "oscuro": {
            "bg_primary": "rgba(40, 44, 52, 0.95)",
            "bg_secondary": "#2C313A",
            "bg_fondo": "#21252B",
            "bg_panel": "rgba(40, 44, 52, 0.9)",
            "primary": "#008faf",
            "secondary": "#FF6F64",
            "text_primary": "#FFFFFF",
            "text_secondary": "#ABB2BF",
            "text_label": "#D7D7D7",
            "border": "#005a6e",
            "border_light": "#4B5362",
            "border_input": "#5D6575",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "table_header": "#2C313A",
            "table_header_secondary": "#11c7f0",
            "table_bg": "#282C34",
            "card_bg": "#2C313A",
            "input_bg": "#2C313A",
            "scroll_bg": "#2C313A",
            "scroll_handle": "#4B5362",
            "boton": "#005a6e",
            "boton_hover": "#00485a",
            "boton_pressed": "#003441"
        }
    }

   
    
    def cargar_configuracion(self):
        """Carga la configuración desde la base de datos"""
        try:
            from models.Modelo_configuracion import Model_Configuraciones
            
            modelo = Model_Configuraciones()
            config = modelo.cargar_configuracion_interfaz()
            
            self.THEME = config["tema"].lower()
            self.FONT_FAMILY = config["fuente"]
            self.FONT_SIZE = config["tamaño"]
            self.FONT_BOLD = config["negrita"]
            
        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            # Valores por defecto
            self.FONT_FAMILY = "Arial"
            self.FONT_SIZE = 12
            self.FONT_BOLD = False
            self.THEME = "claro"
    
    def obtener_colores_tema(self):
        """Retorna los colores del tema actual"""
        return self.THEME_COLORS.get(self.THEME, self.THEME_COLORS["claro"])
    
    
    def obtener_estilo_boton(self):
        # Retornar estilo para los
        colores = self.obtener_colores_tema()
        font_weight = "bold" if self.FONT_BOLD else "normal"
        
        return f"""
        QPushButton{{
            background: {colores['boton']};
            color: White;
            font-weight: bold;
            font-size: {self.FONT_SIZE + 7}px;
            font-family: {self.FONT_FAMILY};
            padding: 15px;
            border-radius: 15px;
            border: none;
            text-align: left;
            margin: 10px 5px 20px 5px;
            min-width: 30px;
            min-height: 20px;
        }}  
        QPushButton:hover{{
            background: {colores['boton_hover']};
        }}
        QPushButton:focus{{
        outline: none;
        }}
        QPushButton:pressed{{
            background: {colores['boton_pressed']};
        }}  
        """
    
    
    def obtener_estilo_header(self):
        # Retorna el estilo para headers/etiquetas de sección"""
        colores = self.obtener_colores_tema()
        font_weight = "bold" if self.FONT_BOLD else "normal"
        
        return f"""
        QLabel{{
            font-family: {self.FONT_FAMILY};
            background: {colores["table_header"]};
            font-size: {self.FONT_SIZE + 15}px; 
            color: white;
            font-weight: {font_weight};
            padding: 10px 5px;
            margin: 0;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
            max-height: 50px;
        }}
        """
    
    
    def obtener_estilo_input(self):
        """Retorna el estilo CSS para campos de entrada"""
        colores = self.obtener_colores_tema()
        
        return f"""
        QLineEdit, QTextEdit, QComboBox{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 5}px;
            border: 1.5px solid {colores['border_light']};
            border-radius: 10px;
            padding: 14px 18px;
            min-width: {self.FONT_SIZE + 5}px;
            min-height: {self.FONT_SIZE + 10}px;
            margin-top: 10px;
            margin-bottom: 10px;
            margin-left: 5px;
            margin-right: 5px;
            background: {colores['input_bg']};
            color: {colores['text_primary']};
        }}
       QSpinBox{{
        font-family: {self.FONT_FAMILY};
        font-size: {self.FONT_SIZE + 5}px;
        border: 1.5px solid {colores['border_light']};
        border-radius: 10px;
        padding: 5px;
        min-height: 30px;
        min-width: 120px;
        margin-top: 5px;
        margin-bottom: 5px;
        margin-left: 5px;
        margin-right: 5px;
        background: {colores['input_bg']};
        color: {colores['text_primary']};
        }}

        QSpinBox::up-button, QSpinBox::down-button {{
            width: 25px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus{{
            border: 2px solid {colores['border_input']};
            background: {colores['input_bg']};
        }}
        QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QSpinBox:hover{{
            border: 2px solid {colores['border_input']};
            background: {colores['input_bg']};
        }}
        QLineEdit::placeholder, QTextEdit::placeholder{{
            color: {colores['text_secondary']};
        }}
        """
    
    
    def obtener_estilo_title(self):
        colores = self.obtener_colores_tema()
        font_weight = "bold" if self.FONT_BOLD else "normal"
        
        return f"""
        QLabel{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 3}px;
            color: {colores['text_label']};
            font-weight: bold;
            border: 0px;
            margin: 5px;
            padding: 5px;
            background: none;
        }}
        """

    def obtener_estilo_label(self):
        # Retorna el estilo de los Label para ser usado
        colores = self.obtener_colores_tema()
        font_weight = "bold" if self.FONT_BOLD else "normal"
        
        return f"""
        QLabel{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE}px;
            color: {colores['text_label']};
            font-weight: {font_weight};
            margin: 5px;
            padding: 2px;
            background: none;
        }}
        """
    
    
    def obtener_estilo_panel(self):
        # Retorna el estilo del Panel
        colores = self.obtener_colores_tema()
        
        return f"""
        QFrame{{
            background: {colores['bg_panel']};
            border-radius: 15px;
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border: 1px solid {colores['border']};
        }}
        """
    
    
    def obtener_estilo_tabla(self):
        # Retorna el estilo CSS para tablas
        colores = self.obtener_colores_tema()
        return f"""
        QTableWidget{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE +3}px;
            background-color: {colores['table_bg']};
            color: {colores['text_primary']};
            border: 1px solid {colores['border']};
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            gridline-color: {colores['border']};
            margin: 10px;
            border-radius: 8px;
        }}
        QHeaderView::section {{
            background-color: {colores["table_header"]};
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            color: white;
            font-size: {self.FONT_SIZE + 2}px;
            font-weight: bold;
            padding: 8px;
            border: 1px solid {colores['border']};
        }}
        QTableWidget::item {{
            padding: 6px;
        }}
        QTableWidget::item:selected {{
            background-color: {colores['boton_hover']};
            color: white;
        }}
        """
    
    
    def obtener_estilo_scroll(self):
        """Retorna el estilo CSS para scrollbars"""
        colores = self.obtener_colores_tema()
        
        return f"""
        QScrollArea {{
            border: none;
            background: transparent;
        }}
        QScrollBar:vertical {{
            background: {colores['scroll_bg']};
            width: 12px;
            margin: 0px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {colores['scroll_handle']};
            border-radius: 6px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {colores['primary']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        """
    
    def obtener_estilo_grupo(self):
        """Retorna el estilo CSS para grupos (QGroupBox)"""
        colores = self.obtener_colores_tema()
        font_weight = "bold" if self.FONT_BOLD else "normal"
        
        return f"""
        QGroupBox{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 2}px;
            font-weight: {font_weight};
            color: {colores['text_primary']};
            margin: 0;
            padding: 15px 12px;
            border: 2px solid {colores['border_light']};
            border-radius: 8px;
            background: {colores['bg_secondary']};
            min-width: 200px;
        }}
        QGroupBox::title{{
            font-size: {self.FONT_SIZE + 5}px;
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 6px 0 6px;
            color: {colores["text_primary"]};
        }}
        """

    def obtener_estilo_radio_checkbox(self):
        """Retorna el estilo CSS para radio buttons y checkboxes"""
        colores = self.obtener_colores_tema()
        
        radio_style = f"""
        QRadioButton{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 5}px;
            color: {colores['text_primary']};
            background-color: transparent;
            padding: 6px 5px;
            spacing: 8px;
            min-height: 20px;
        }}
        QRadioButton::indicator{{
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid {colores['border_input']};
        }}
        QRadioButton::indicator:checked{{
            background-color: {colores['boton']};
            border: 2px solid {colores['boton']};
        }}
        """
        
        checkbox_style = f"""
        QCheckBox{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 1}px;
            color: {colores['text_primary']};
            background-color: transparent;
            padding: 8px 0px;
            spacing: 8px;
        }}
        QCheckBox::indicator{{
            width: 16px;
            height: 16px;
            border: 2px solid {colores['border_input']};
            border-radius: 3px;
            background: {colores['input_bg']};
        }}
        QCheckBox::indicator:checked{{
            background-color: {colores['boton']};
            border: 2px solid {colores['boton']};
        }}
        """
        
        return radio_style, checkbox_style
    
    def obtener_fondo_aplicacion(self):
        """Retorna el estilo CSS para el fondo de la aplicación"""
        colores = self.obtener_colores_tema()
        return f"background: {colores['bg_primary']};"
    
    def obtener_estilo_card(self):
        """Retorna el estilo CSS para tarjetas"""
        colores = self.obtener_colores_tema()
        
        return f"""
        QFrame{{
            background: {colores['card_bg']};
            border-radius: 10px;
            border-left: 5px solid {colores['bg_primary']};
            padding: 15px;
            margin: 5px;
        }}
        """
    
    def obtener_estilo_date(self):
        colores = self.obtener_colores_tema()

        return f"""QDateEdit {{
        margin: 0 0 0 20px;
        border: 2px solid {colores['primary']};
        border-radius: 2px;
        padding: 10px;
        margin: 5px 2px 15px 20px;
        background-color: {colores['bg_primary']};
        color: {colores["text_primary"]};
        font-size: {self.FONT_SIZE}px;
        }}
        QDateEdit:hover {{
        border-color: {colores['primary']};
        }}

        QDateEdit:disabled {{
        background-color: {colores['bg_primary']};
        }}
        
        QCalendarWidget {{
        background-color: {colores['bg_primary']};
        border: 2px solid {colores['primary']}
        border-radius: 2px;
        }}
        
        QCalendarWidget QToolButton {{
        color: #005a6e;
        background-color: #f0f0f0;
        font-size: {self.FONT_SIZE}px;
        icon-size: 20px, 20px;
        }}
        
        QCalendarWidget QMenu {{
        background-color: white;
        color: {colores["text_primary"]};
        }}
        
        QCalendarWidget QSpinBox {{
        background-color: {colores['bg_primary']};
        color: {colores["text_primary"]};
        selection-background-color: {colores['primary']};
        selection-color: white;
        }}
        
        QCalendarWidget QWidget {{ alternate-background-color: #e6f7ff; }}
        
        QCalendarWidget QTableView {{
        selection-background-color: {colores['primary']};
        selection-color: {colores['bg_primary']};
        gridline-color: #ddd;
        }}
        
        QCalendarWidget QHeaderView::section {{
        background-color: #f8f9fa;
        color: {colores["text_primary"]};
        min-height: {self.FONT_SIZE +10}px;
        font-weight: bold;
        padding: 6px;
        border: 1px solid #ddd;
        }}
        """
    
    def obtener_estilo_frame(self):
        colores = self.obtener_colores_tema()
        return f"""background: {colores['bg_primary']}; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;"""
    
    def obtener_estilo_widget(self):
        colores = self.obtener_colores_tema()
        return f"""padding: 0; margin: 0; background: {colores['bg_primary']};"""
    def obtener_estilo_completo(self):
        # Retorna un diccionario con el estilo del programa
        self.cargar_configuracion()
        
        radio_style, checkbox_style = self.obtener_estilo_radio_checkbox()
        
        return {
            "font_family": self.FONT_FAMILY,
            "font_size": self.FONT_SIZE,
            "font_bold": self.FONT_BOLD,
            "theme": self.THEME,
            "colors": self.obtener_colores_tema(),
            "styles": {
                "boton": self.obtener_estilo_boton(),
                "header": self.obtener_estilo_header(),
                "input": self.obtener_estilo_input(),
                "label": self.obtener_estilo_label(),
                "title": self.obtener_estilo_title(),
                "panel": self.obtener_estilo_panel(),
                "tabla": self.obtener_estilo_tabla(),
                "scroll": self.obtener_estilo_scroll(),
                "grupo": self.obtener_estilo_grupo(),
                "radio": radio_style,
                "checkbox": checkbox_style,
                "fondo": self.obtener_fondo_aplicacion(),
                "card": self.obtener_estilo_card(),
                "date": self.obtener_estilo_date(),
                "frame": self.obtener_estilo_frame(),
                "widget": self.obtener_estilo_widget()
            }
        }

    def aplicar_estilo_vista(self, vista):
        # Aplica el estilo a una vista completa
        estilo = self.obtener_estilo_completo()
        
        # Aplicar fondo a la vista principal
        vista.setStyleSheet(estilo["styles"]["fondo"])
        
        return estilo
    
    def actualizar_configuracion(self, tema=None, fuente_familia=None, fuente_tamano=None, fuente_negrita=None):
        """Actualiza la configuración y notifica a toda la aplicación"""
        try:
            from models.Modelo_configuracion import Model_Configuraciones
            modelo = Model_Configuraciones()
            
            if tema:
                # Guardar en BD
                modelo.guardar_configuracion_interfaz(
                    tema=tema,
                    fuente=fuente_familia or self.FONT_FAMILY,
                    tamaño=fuente_tamano or self.FONT_SIZE,
                    negrita=fuente_negrita if fuente_negrita is not None else self.FONT_BOLD
                )
                self.THEME = tema.lower()
            
            if fuente_familia or fuente_tamano or fuente_negrita is not None:
                # Guardar en BD
                modelo.guardar_configuracion_interfaz(
                    tema=self.THEME,
                    fuente=fuente_familia or self.FONT_FAMILY,
                    tamaño=fuente_tamano or self.FONT_SIZE,
                    negrita=fuente_negrita if fuente_negrita is not None else self.FONT_BOLD
                )
                
                if fuente_familia:
                    self.FONT_FAMILY = fuente_familia
                if fuente_tamano:
                    self.FONT_SIZE = fuente_tamano
                if fuente_negrita is not None:
                    self.FONT_BOLD = fuente_negrita
            
            # Emitir señal para notificar a toda la aplicación
            self.notificar_cambio_estilos()
            
            return True
            
        except Exception as e:
            print(f"❌ Error al actualizar configuración: {e}")
            return False

    def registrar_vista(self, vista):
        # == Registrar una vista para recibir actualizaciones de estilo==
        if vista not in AppStyle.vistas_registradas:
            AppStyle.vistas_registradas.append(vista)

    def desregistrar_vista(self, vista):
        # ==Eliminar una vista de la lista de actualización==
        if vista in AppStyle.vistas_registradas:
            AppStyle.vistas_registradas.remove(vista)
    
    def notificar_cambio_estilos(self):
        # Actualizar la configuracion interna primero
        self.cargar_configuracion()

        # Emitir señal
        self.estilos_actualizados.emit()

        # Notificar a cada vista registrada
        for vista in AppStyle.vistas_registradas:
            try:
                if hasattr(vista, 'actualizar_estilos'):
                    vista.actualizar_estilos()
                
                elif hasattr(vista, 'actualizar_estilo_vista'):
                    vista.actualizar_estilo_vista
                else:
                    # Si no tiene algún método especifico, aplicar método general
                    self.aplicar_estilo_vista(vista)
            except Exception as e:
                print(f" Error actualizando {vista.__class__.__name__}: {e}")

    def actualizar_y_notificar(self, tema=None, fuente_familia=None, fuente_tamano=None, fuente_negrita=None):
        # =Actualizar la configuración y notifica a todas las vistas=
        success = self.actualizar_configuracion(tema, fuente_familia, fuente_tamano, fuente_negrita)
        if success:
            self.notificar_cambio_estilos()
        return success

# Instancia global para uso en toda la aplicación
estilo_app = AppStyle()