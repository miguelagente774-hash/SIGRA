from PyQt5.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QTextEdit, QWidget, 
                             QPushButton, QLineEdit, QSizePolicy, QFileDialog,
                             QMessageBox, QDateEdit)
from PyQt5.QtCore import Qt, QSize, QDate, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QFont
import os

FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"


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
        self.setFixedSize(300, 180)  # Tamaño fijo para mantener consistencia
        
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
                background: #ffffff;
                border: 2px dashed #d1d5db;
                border-radius: 12px;
                /* **CAMBIO 2: Quitar min/max width/height ya que usamos fixedSize */
            }}
            ImageFrame:hover {{
                border-color: #4FC3F7;
                background: #f8fdff;
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
                padding: 0px;
            }
            QPushButton:hover {
                background: #f1f1f1;
            }
        """)
        # **CAMBIO 6: Tamaño fijo para el botón igual que el label**
        button.setFixedSize(170, 120)
        
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
                color: #9ca3af;
                background: transparent;
                border: none;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Texto del botón
        text_label = QLabel(f"Imagen {self.numero_imagen}")
        text_label.setStyleSheet(f"""
            QLabel {{
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: #6b7280;
                font-weight: normal;
                background: transparent;
                border: none;
                margin-top: 5px;
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
        button.setStyleSheet("""
            QPushButton {
                background: #ef4444;
                color: white;
                border: none;
                border-radius: 50%;
                font-size: 12px;
                font-weight: bold;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
            }
            QPushButton:hover {
                background: #dc2626;
            }
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
            # **CAMBIO 9: Cambiar borde de punteado a sólido cuando hay imagen**
            self.setStyleSheet(f"""
                ImageFrame {{
                    background: #ffffff;
                    border: 2px solid #d1d5db;
                    border-radius: 12px;
                }}
            """)
        else:
            self.image_label.hide()
            self.load_button.show()
            self.remove_button.setVisible(False)
            # **CAMBIO 10: Volver a borde punteado cuando no hay imagen**
            self.setStyleSheet(f"""
                ImageFrame {{
                    background: #ffffff;
                    border: 2px dashed #d1d5db;
                    border-radius: 12px;
                }}
                ImageFrame:hover {{
                    border-color: #4FC3F7;
                    background: #f8fdff;
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
        # **SOLUCIÓN 4: Limpiar ambas variables para consistencia**
        self.image_path = None
        self.file_path = None
        
        self.update_visibility(show_image=False)
        self.imageRemoved.emit(self.numero_imagen)
        
    def set_imagen(self, file_path):
        """Establece una imagen desde código externo"""
        if file_path and self.mostrar_imagen(file_path):
            self.imageLoaded.emit(self.numero_imagen, file_path)
            
    def get_imagen_path(self):
        """Devuelve la ruta de la imagen actual"""
        # **SOLUCIÓN 5: Siempre devolver self.file_path que es la fuente de verdad**
        return self.file_path
        
    def clear(self):
        """Limpia el frame (elimina imagen si existe)"""
        if self.image_path:
            self.eliminar_imagen()
            
    def has_imagen(self):
        """Verifica si el frame tiene una imagen cargada"""
        return self.file_path is not None and self.image_label.pixmap() is not None