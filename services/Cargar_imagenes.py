from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTextEdit, QWidget, 
                             QPushButton, QLineEdit, QSizePolicy, QFileDialog,
                             QMessageBox, QDateEdit)
from PyQt5.QtCore import Qt, QSize, QDate, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QFont
import os
from components.app_style import estilo_app

FONT_FAMILY = estilo_app.obtener_estilo_completo()["font_family"]
FONT_SIZE = estilo_app.obtener_estilo_completo()["font_size"]
FONT_COLOR = "#FFFFFF"
COLOR_PRIMARIO = estilo_app.obtener_colores_tema()["primary"]
COLOR_PRIMARIO_HOVER = estilo_app.obtener_colores_tema()["boton_hover"]
BACKGROUND = estilo_app.obtener_colores_tema()["bg_primary"]
BACKGROUND_HOVER = estilo_app.obtener_colores_tema()["bg_fondo"]
BORDER = estilo_app.obtener_colores_tema()["border"]
BORDER_LIGHT = estilo_app.obtener_colores_tema()["border_light"]


class ImageFrame(QFrame):
    """Frame para cargar y mostrar imágenes con opción de eliminación"""
    
    # Señales para notificar cambios al padre
    imageLoaded = pyqtSignal(int, str)  # (número_imagen, ruta)
    imageRemoved = pyqtSignal(int)      # (número_imagen)
    
    def __init__(self, numero_imagen, ruta_imagen=None, parent=None):
        super().__init__(parent)
        self.numero_imagen = numero_imagen
        self.image_path = None
        self.file_path = ruta_imagen
        
        # **CAMBIO 1: Definir tamaño fijo para el contenedor**
        #self.setFixedSize(300, 180)
        self.setMinimumSize(300, 100)
        self.setMaximumSize(400, 300)  # Tamaño fijo para mantener consistencia
        
        self.setup_ui()
        

        # Cargar imagen solo si se proporcionó una ruta válida
        if self.file_path and isinstance(self.file_path, str):
            if self.verificar_imagen_valida(self.file_path):
                self.mostrar_imagen(self.file_path)
                # **SOLUCIÓN 1: Actualizar image_path también cuando se carga desde el constructor**
                self.image_path = self.file_path
        
    def setup_ui(self):
        """Configura la interfaz del frame de imagen"""
        self.setStyleSheet(f"""
            ImageFrame {{
                background: {BACKGROUND};
                border: 2px dashed {BORDER_LIGHT};
                border-radius: 12px;
                /* **CAMBIO 2: Quitar min/max width/height ya que usamos fixedSize */
            }}
            ImageFrame:hover {{
                border-color: {COLOR_PRIMARIO};
                background: {BACKGROUND};
            }}
        """)
        
        # **CAMBIO 3: Usar Fixed en lugar de Expanding**
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignCenter)
        
        # Label para mostrar la imagen
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                border-radius: 8px;
                /* **CAMBIO 4: Tamaño fijo para el QLabel también */
            }
        """)
        # **CAMBIO 5: Tamaño fijo más pequeño para el label de imagen**
        self.image_label.setFixedSize(170, 120)  # Un poco más pequeño que el contenedor
        self.image_label.hide()
        
        # Botón para cargar imagen
        self.load_button = self.create_load_button()
        self.load_button.clicked.connect(self.cargar_imagen)
        
        # Botón para eliminar imagen
        self.remove_button = self.create_remove_button()
        self.remove_button.setVisible(False)
        self.remove_button.clicked.connect(self.eliminar_imagen)
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.remove_button, alignment=Qt.AlignTop | Qt.AlignRight)
        
    def create_load_button(self):
        """Crea el botón para cargar imágenes"""
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton:hover {
                background: #f1f1f1;
            }
        """)
        # **CAMBIO 6: Tamaño fijo para el botón igual que el label**
        button.setMinimumSize(280, 150)
        button.setMaximumSize(400, 250)
        
        # Layout interno para el botón
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignCenter)
        
        # Icono de añadir
        icon_label = QLabel("+")
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-family: {FONT_FAMILY};
                font-size: 32px;
                color: {FONT_COLOR};
                background: transparent;
                border: none;
                margin-top: 5px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Texto del botón
        text_label = QLabel(f"Imagen {self.numero_imagen}")
        text_label.setStyleSheet(f"""
            QLabel {{
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {FONT_COLOR};
                font-weight: normal;
                background: transparent;
                border: none;
                margin-bottom: 10px;
                padding: 5px 15px;
            }}
        """)
        text_label.setAlignment(Qt.AlignCenter)
        
        button_layout.addWidget(icon_label)
        button_layout.addWidget(text_label)
        button.setLayout(button_layout)
        
        return button
        
    def create_remove_button(self):
        """Crea el botón para eliminar imágenes"""
        button = QPushButton("✕")
        button.setStyleSheet(f"""
            QPushButton {{
                background: #ef4444;
                color: {FONT_COLOR};
                border: none;
                border-radius: 50%;
                font-size: {FONT_SIZE};
                font-weight: bold;
                min-width: 28px;
                max-width: 28px;
                min-height: 28px;
                max-height: 28px;
            }}
            QPushButton:hover {{
                background: #dc2626;
            }}
        """)
        button.setCursor(Qt.PointingHandCursor)
        return button
        
    def scale_pixmap(self, pixmap):
        """Escala el pixmap manteniendo la relación de aspecto"""
        # **CAMBIO 7: Usar el tamaño del label como referencia**
        label_width = self.image_label.width() - 10  # Un poco de margen
        label_height = self.image_label.height() - 10
        
        # Escalar manteniendo la relación de aspecto
        scaled_pixmap = pixmap.scaled(
            label_width, label_height,
            Qt.KeepAspectRatio,  # Mantiene proporción
            Qt.SmoothTransformation  # Suavizado
        )
        
        return scaled_pixmap
        
    def mostrar_imagen(self, file_path):
        """Muestra la imagen en el frame"""
        try:
            pixmap = QPixmap(file_path)
            
            if pixmap.isNull():
                QMessageBox.warning(self, "Error", "No se pudo cargar la imagen seleccionada.")
                return False
                
            # **CAMBIO 8: Escalar la imagen al tamaño del contenedor**
            scaled_pixmap = self.scale_pixmap(pixmap)
            
            self.image_label.setPixmap(scaled_pixmap)
            # **SOLUCIÓN 2: Actualizar ambas variables para consistencia**
            self.image_path = file_path
            self.file_path = file_path
            
            # Actualizar visibilidad de elementos
            self.update_visibility(show_image=True)
            
            return True
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar la imagen: {str(e)}")
            return False
            
    def update_visibility(self, show_image=False):
        """Actualiza la visibilidad de los elementos según el estado"""
        if show_image:
            self.image_label.show()
            self.load_button.hide()
            self.remove_button.setVisible(True)
            # Cambiar borde de punteado a sólido cuando hay imagen
            self.setStyleSheet(f"""
                ImageFrame {{
                    background: {BACKGROUND};
                    border: 2px solid {BORDER};
                    border-radius: 12px;
                }}
            """)
        else:
            self.image_label.hide()
            self.load_button.show()
            self.remove_button.setVisible(False)
            self.setStyleSheet(f"""
                ImageFrame {{
                background: {BACKGROUND};
                border: 2px dashed {BORDER_LIGHT};
                border-radius: 12px;
                }}
                ImageFrame:hover {{
                    border-color: {COLOR_PRIMARIO};
                    background: {BACKGROUND};
                }}
            """)
    
    def cargar_imagen(self):
        """Abre diálogo para seleccionar imagen"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Seleccionar Imagen {self.numero_imagen}",
            "",
            "Archivos de imagen (*.png *.jpg *.jpeg *.bmp *.gif *.webp *.svg);;Todos los archivos (*)"
        )
        
        if file_path:
            # **SOLUCIÓN 3: Usar set_imagen que ya emite la señal y actualiza variables**
            self.set_imagen(file_path)
        
    
    def verificar_imagen_valida(self, file_path):
        """Verifica si la ruta contiene una imagen válida"""
        try:
            if not isinstance(file_path, str):
                return False
                
            if not os.path.exists(file_path):
                return False
                
            pixmap = QPixmap(file_path)
            return not pixmap.isNull()
            
        except Exception:
            return False
    
    def eliminar_imagen(self):
        """Elimina la imagen actual"""
        self.image_label.clear()
        self.image_path = None
        self.file_path = None
        
        self.update_visibility(show_image=False)
        self.imageRemoved.emit(self.numero_imagen)
        
    def set_imagen(self, file_path):
        """Establece una imagen desde código externo"""
        if file_path and self.mostrar_imagen(file_path):
            self.imageLoaded.emit(self.numero_imagen, file_path)
            
    def get_imagen_path(self):
        # Devuelve la Ruta de la Imágen Actual
        return self.file_path
        
    def clear(self):
        # Limpiar el Frame si hay alguna imagen
        if self.image_path:
            self.eliminar_imagen()
            
    def has_imagen(self):
        # Verifica si el frame tiene una imagen cargada
        return self.file_path is not None and self.image_label.pixmap() is not None
    
    def actualizar_estilos(self):
        """Actualiza los estilos del frame de imagen"""
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        
        # Actualizar estilo del frame
        self.setStyleSheet(f"""
            ImageFrame {{
                background: {BACKGROUND};
                border: 2px dashed {BORDER_LIGHT};
                border-radius: 12px;
                /* **CAMBIO 2: Quitar min/max width/height ya que usamos fixedSize */
            }}
            ImageFrame:hover {{
                border-color: {COLOR_PRIMARIO};
                background: {BACKGROUND};
            }}
        """)
        
        # Actualizar botón si existe
        if hasattr(self, 'btn_cargar_imagen'):
            self.btn_cargar_imagen.setStyleSheet(self.estilo["styles"]["boton"])