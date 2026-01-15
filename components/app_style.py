import hashlib
from typing import Optional, Tuple, Dict, Any
from models.conexion_db import ConexionDB
from PyQt5.QtCore import QSettings
import os

class AppStyle:
    # ==Clase para gestionar los estilos de toda la aplicación==
    
    # Variables de clase para configuración global
    FONT_FAMILY = "Arial" 
    FONT_SIZE = 12
    FONT_BOLD = False
    THEME = "claro" 
    COLOR_PRIMARIO = "#005a6e"
    COLOR_AZUL_HOVER = "#00485a"
    COLOR_SECUNDARIO = "#F44336"
    
    # Colores por tema
    THEME_COLORS = {
        "claro": {
            "bg_primary": "rgba(255, 255, 255, 0.95)",
            "bg_secondary": "#FAFAFA",
            "bg_fondo": "#E3EFF3",
            "bg_panel": "rgba(255, 255, 255, 0.9)",
            "text_primary": "#000000",
            "text_secondary": "#37474F",
            "text_label": "#333333",
            "border": "#E0E0E0",
            "border_light": "#E3F2FD",
            "border_input": "#BDBDBD",
            "shadow": "gray",
            "table_header": "#005a6e",
            "table_bg": "white",
            "card_bg": "white",
            "input_bg": "white",
            "scroll_bg": "#f0f0f0",
            "scroll_handle": "#c0c0c0"
        },
        "oscuro": {
            "bg_primary": "rgba(40, 44, 52, 0.95)",
            "bg_secondary": "#2C313A",
            "bg_fondo": "#21252B",
            "bg_panel": "rgba(40, 44, 52, 0.9)",
            "text_primary": "#FFFFFF",
            "text_secondary": "#ABB2BF",
            "text_label": "#D7D7D7",
            "border": "#3A3F4B",
            "border_light": "#4B5362",
            "border_input": "#5D6575",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "table_header": "#2C313A",
            "table_bg": "#282C34",
            "card_bg": "#2C313A",
            "input_bg": "#2C313A",
            "scroll_bg": "#2C313A",
            "scroll_handle": "#4B5362"
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
            background: {self.COLOR_PRIMARIO};
            color: White;
            font-weight: bold;
            font-size: {self.FONT_SIZE + 7}px;
            font-family: {self.FONT_FAMILY};
            padding: 15px;
            border-radius: 15px;
            border: none;
            text-align: left;
            margin: 25px 15px;
            min-width: 30px;
            min-height: 20px;
        }}  
        QPushButton:hover{{
            background: {self.COLOR_AZUL_HOVER};
        }}    
        QPushButton:pressed{{
            background: {self.COLOR_AZUL_HOVER.replace('a', '8')};
        }}  
        """
    
    
    def obtener_estilo_header(self):
        # Retorna el estilo para headers/etiquetas de sección"""
        colores = self.obtener_colores_tema()
        font_weight = "bold" if self.FONT_BOLD else "normal"
        
        return f"""
        QLabel{{
            font-family: {self.FONT_FAMILY};
            background: {self.COLOR_PRIMARIO};
            font-size: {self.FONT_SIZE + 15}px; 
            color: white;
            font-weight: {font_weight};
            padding: 10px 5px;
            margin: 0;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 0px;
        }}
        """
    
    
    def obtener_estilo_input(self):
        """Retorna el estilo CSS para campos de entrada"""
        colores = self.obtener_colores_tema()
        
        return f"""
        QLineEdit, QTextEdit, QComboBox, QSpinBox{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 5}px;
            padding: 10px;
            margin: 5px;
            border: 2px solid {colores['border_input']};
            border-radius: 8px;
            min-width: {self.FONT_SIZE + 5}px;
            background: {colores['input_bg']};
            color: {colores['text_primary']};
        }}
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus{{
            border: 2px solid {self.COLOR_PRIMARIO};
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
            font-size: {self.FONT_SIZE + 10}px;
            color: {colores['text_label']};
            font-weight: {font_weight};
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
        """Retorna el estilo CSS para paneles"""
        colores = self.obtener_colores_tema()
        
        return f"""
        QFrame{{
            background: {colores['bg_panel']};
            border-radius: 15px;
            border: 1px solid {colores['border']};
            padding: 0;
            margin: 20px;
        }}
        """
    
    
    def obtener_estilo_tabla(self):
        # Retorna el estilo CSS para tablas
        colores = self.obtener_colores_tema()
        return f"""
        QTableWidget{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE +5}px;
            background-color: {colores['table_bg']};
            color: {colores['text_primary']};
            border: 1px solid {colores['border']};
            gridline-color: {colores['border']};
            margin: 10px;
            border-radius: 8px;
        }}
        QHeaderView::section {{
            background-color: {self.COLOR_PRIMARIO};
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
            background-color: {self.COLOR_AZUL_HOVER};
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
            background: {self.COLOR_PRIMARIO};
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
            color: {colores['text_secondary']};
            margin: 0;
            padding: 15px 12px;
            border: 2px solid {colores['border_light']};
            border-radius: 8px;
            background: {colores['bg_secondary']};
            min-width: 200px;
        }}
        QGroupBox::title{{
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 6px 0 6px;
            color: {self.COLOR_PRIMARIO};
        }}
        """

    def obtener_estilo_radio_checkbox(self):
        """Retorna el estilo CSS para radio buttons y checkboxes"""
        colores = self.obtener_colores_tema()
        
        radio_style = f"""
        QRadioButton{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 1}px;
            color: {colores['text_secondary']};
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
            background-color: {self.COLOR_PRIMARIO};
            border: 2px solid {self.COLOR_PRIMARIO};
        }}
        """
        
        checkbox_style = f"""
        QCheckBox{{
            font-family: {self.FONT_FAMILY};
            font-size: {self.FONT_SIZE + 1}px;
            color: {colores['text_secondary']};
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
            background-color: {self.COLOR_PRIMARIO};
            border: 2px solid {self.COLOR_PRIMARIO};
        }}
        """
        
        return radio_style, checkbox_style
    
    def obtener_fondo_aplicacion(self):
        """Retorna el estilo CSS para el fondo de la aplicación"""
        colores = self.obtener_colores_tema()
        return f"background: {colores['bg_fondo']};"
    
    def obtener_estilo_card(self):
        """Retorna el estilo CSS para tarjetas"""
        colores = self.obtener_colores_tema()
        
        return f"""
        QFrame{{
            background: {colores['card_bg']};
            border-radius: 10px;
            border-left: 5px solid {self.COLOR_PRIMARIO};
            padding: 15px;
            margin: 5px;
        }}
        """
    
    def obtener_estilo_completo(self):
        """Retorna un diccionario con todos los estilos"""
        self.cargar_configuracion()
        
        radio_style, checkbox_style = self.obtener_estilo_radio_checkbox()
        
        return {
            "font_family": self.FONT_FAMILY,
            "font_size": self.FONT_SIZE,
            "font_bold": self.FONT_BOLD,
            "theme": self.THEME,
            "color_primario": self.COLOR_PRIMARIO,
            "color_secundario": self.COLOR_SECUNDARIO,
            "color_hover": self.COLOR_AZUL_HOVER,
            "colors": self.obtener_colores_tema(),
            "styles": {
                "boton": self.obtener_estilo_boton(),
                "header": self.obtener_estilo_header(),
                "input": self.obtener_estilo_input(),
                "title": self.obtener_estilo_title(),
                "label": self.obtener_estilo_label(),
                "panel": self.obtener_estilo_panel(),
                "tabla": self.obtener_estilo_tabla(),
                "scroll": self.obtener_estilo_scroll(),
                "grupo": self.obtener_estilo_grupo(),
                "radio": radio_style,
                "checkbox": checkbox_style,
                "fondo": self.obtener_fondo_aplicacion(),
                "card": self.obtener_estilo_card()
            }
        }

    def aplicar_estilo_vista(self, vista):
        """Aplica el estilo a una vista completa"""
        estilo = self.obtener_estilo_completo()
        
        # Aplicar fondo a la vista principal
        vista.setStyleSheet(estilo["styles"]["fondo"])
        
        return estilo

    def actualizar_configuracion(self, tema=None, fuente_familia=None, fuente_tamano=None, fuente_negrita=None):
        """Actualiza la configuración en la base de datos y en memoria"""
        db = ConexionDB()
        
        if tema:
            db.cursor.execute("UPDATE Tema SET tema = ? WHERE id_tema = 1", (tema,))
            self.THEME = tema
        
        if fuente_familia or fuente_tamano or fuente_negrita:
            # Actualizar configuración de fuente
            font_value = "bold" if fuente_negrita else "normal"
            db.cursor.execute("""
                UPDATE Fuente 
                SET tamano = COALESCE(?, tamano),
                    famila = COALESCE(?, famila),
                    font = COALESCE(?, font)
                WHERE id_fuente = 1
            """, (fuente_tamano, fuente_familia, font_value))
            
            if fuente_tamano:
                self.FONT_SIZE = fuente_tamano
            if fuente_familia:
                self.FONT_FAMILY = fuente_familia
            if fuente_negrita is not None:
                self.FONT_BOLD = fuente_negrita
        
        db.conexion.commit()
        db.Cerrar()

# Instancia global para uso en toda la aplicación
estilo_app = AppStyle()