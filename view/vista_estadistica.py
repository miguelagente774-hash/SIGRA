from PyQt5.QtWidgets import (
    QVBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect,
    QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont
from components.app_style import estilo_app

estilo = estilo_app.obtener_estilo_completo()

def get_shadow_effect(radius, color=Qt.gray, offset_x=1, offset_y=1):
    """Crea y configura un efecto de sombra."""
    sombra = QGraphicsDropShadowEffect()
    sombra.setBlurRadius(radius)
    sombra.setColor(color)
    sombra.setOffset(offset_x, offset_y)
    return sombra

# Clase para el Widget de Gráfica
class Widget_Graficos(QFrame):
    def __init__(self, title, chart_data=None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(160)
        self.setStyleSheet("background: transparent; border: none;")
        
        # Data Configuration
        data_default = [70, 30]
        labels_default = ["Actividades Realizadas", "Actividades sin Hacer"]
        
        self.data = chart_data.get('data', data_default) if chart_data else data_default
        self.labels = chart_data.get('labels', labels_default) if chart_data else labels_default
        self.title = title
        self.colors = [
            QColor(estilo_app.obtener_colores_tema()['primary']), 
            QColor(estilo_app.obtener_colores_tema()['secondary'])
        ]
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sombra suave
        self.setGraphicsEffect(get_shadow_effect(5, QColor(0, 0, 0, 20)))

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.contentsRect()
        
        # ===== 1. PINTAR EL TÍTULO =====
        title_height = 30
        title_rect = QRectF(rect.left(), rect.top(), rect.width(), title_height)
        
        label_style = estilo["styles"]["label"]
        
        # Fondo para el título
        painter.setBrush(QBrush(QColor(estilo_app.obtener_colores_tema()['bg_secondary'])))
        painter.setPen(Qt.NoPen)
        painter.drawRect(title_rect)
        
        # Texto del título
        painter.setPen(QPen(QColor(estilo_app.obtener_colores_tema()['text_primary'])))
        title_font = QFont(estilo_app.FONT_FAMILY, estilo_app.FONT_SIZE + 5, QFont.Bold)
        painter.setFont(title_font)
        
        # Ajustar texto si es muy largo
        display_title = self.title
        if len(self.title) > 30:
            if "Objetivo:" in self.title:
                parts = self.title.split("Objetivo:")
                if len(parts) > 1:
                    display_title = f"{parts[0].strip()}... Objetivo:{parts[1]}"
            else:
                display_title = self.title[:27] + "..."
        
        painter.drawText(title_rect, Qt.AlignCenter | Qt.AlignVCenter, display_title)
        
        # ===== 2. PINTAR EL GRÁFICO =====
        chart_area = QRectF(
            rect.left() + 5, 
            rect.top() + title_height + 5,
            rect.width() - 10, 
            rect.height() - title_height - 10
        )
        
        scale_factor = rect.width() / 250
        DYN_FONT_SIZE = max(7, int(8 * scale_factor))
        DYN_ICON_SIZE = max(5, int(5 * scale_factor))
        DYN_LEGEND_SPACING = max(10, int(12 * scale_factor))
        
        TEXT_MARGIN_LEFT = 3
        
        PIE_WIDTH_RATIO = 0.35
        pie_area_width = chart_area.width() * PIE_WIDTH_RATIO
        diameter = min(pie_area_width, chart_area.height()) - 10
        center_x = chart_area.left() + pie_area_width / 2
        center_y = chart_area.top() + chart_area.height() / 2
        pie_rect = QRectF(center_x - diameter / 2, center_y - diameter / 2, diameter, diameter)

        total = sum(self.data)
        start_angle = 90 * 16 
        
        legend_x = chart_area.left() + pie_area_width + 10
        total_items = len(self.data) if self.data else 1
        legend_y = center_y - (((total_items - 1) * DYN_LEGEND_SPACING) / 2) - (DYN_ICON_SIZE / 2)
        
        legend_font = QFont(estilo_app.FONT_FAMILY, DYN_FONT_SIZE)
        painter.setFont(legend_font)

        if total > 0 and self.data:
            for i, value in enumerate(self.data):
                percentage = (value / total)
                span_angle = round(percentage * 360 * 16)
                color = self.colors[i % len(self.colors)]

                painter.setBrush(QBrush(color))
                painter.setPen(QPen(Qt.white, 1))
                painter.drawPie(pie_rect, start_angle, span_angle)

                current_item_y_pos = legend_y + (i * DYN_LEGEND_SPACING)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawRect(int(legend_x), int(current_item_y_pos), DYN_ICON_SIZE, DYN_ICON_SIZE)
                
                text_color = estilo_app.obtener_colores_tema()['text_primary']
                painter.setPen(QPen(QColor(text_color)))
                
                label_name = self.labels[i]
                if len(label_name) > 20:
                    label_name = label_name[:18] + "..."
                
                label_text = f"{label_name} ({percentage*100:.1f}%)"
                
                text_rect = QRectF(
                    int(legend_x) + DYN_ICON_SIZE + TEXT_MARGIN_LEFT,
                    int(current_item_y_pos),
                    chart_area.right() - (int(legend_x) + DYN_ICON_SIZE + TEXT_MARGIN_LEFT) - 5,
                    DYN_LEGEND_SPACING
                )
                painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, label_text)

                start_angle += span_angle

            hole_factor = 0.65 
            hole_size = diameter * hole_factor
            hole_rect = QRectF(center_x - hole_size / 2, center_y - hole_size / 2, hole_size, hole_size)
            painter.setBrush(QBrush(QColor("white")))
            painter.setPen(QPen(Qt.white, 1))
            painter.drawEllipse(hole_rect)

        else:
            text_color = estilo_app.obtener_colores_tema()['text_secondary']
            painter.setPen(QPen(QColor(text_color)))
            painter.drawText(chart_area.toRect(), Qt.AlignCenter, "Sin Datos")
        
        painter.setPen(QPen(QColor(estilo_app.obtener_colores_tema()['border_light']), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 5, 5)


# ---------------------------------------

# Clase: Ventana Estadística
class Ventana_estadística(QFrame):
    def __init__(self):
        super().__init__()
        # Inicializar Estilo
        self.estilo = estilo_app.obtener_estilo_completo()
        
        # Establecer el Tema del Fondo
        self.setStyleSheet(estilo["styles"]["fondo"])
        
        # Registrar esta vista para actualización automática
        estilo_app.registrar_vista(self)
        
        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)

        # Lista para almacenar los gráficos
        self.widgets_graficos = []

        # Inicialización de los Métodos
        self.setup_panel()
        self.setup_charts_panel()

    def setup_panel(self):
        # Layout Principal
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(10, 10, 10, 10)

        # Título de la Ventana
        self.titulo = QLabel("Bienvenido al Sistema de Gestión")
        self.titulo.setStyleSheet(estilo["styles"]["header"])
        self.titulo.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(self.titulo)

    def setup_charts_panel(self):
        # Contenedor principal de estadísticas
        frame_Estadistica = QFrame()
        frame_Estadistica.setStyleSheet(estilo["styles"]["panel"])
        frame_Estadistica.setGraphicsEffect(get_shadow_effect(15))
        
        layout_estadistica = QVBoxLayout(frame_Estadistica)
        layout_estadistica.setSpacing(10)

        titulo = QLabel("Control de Reportes")
        titulo.setStyleSheet(estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout_estadistica.addWidget(titulo)

        # Layout para los gráficos (Grid 2x2)
        layout_charts = QGridLayout()
        layout_charts.setContentsMargins(15, 0, 15, 15)
        layout_charts.setSpacing(15)
        
        # Crear los 4 gráficos con títulos iniciales
        titulos_iniciales = [
            "Semanal (Objetivo: 0)",
            "Mensual (Objetivo: 0)",
            "Trimestral (Objetivo: 0)",
            "Anual (Objetivo: 0)"
        ]
        
        # Posiciones en el grid: (fila, columna)
        posiciones = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for i, titulo in enumerate(titulos_iniciales):
            chart_data = {
                'data': [0, 0],
                'labels': ['Actividades Realizadas', 'Actividades sin Hacer']
            }
            chart = Widget_Graficos(titulo, chart_data)
            chart.setMinimumHeight(200)
            layout_charts.addWidget(chart, posiciones[i][0], posiciones[i][1])
            self.widgets_graficos.append(chart)

        layout_estadistica.addLayout(layout_charts)
        self.layout_principal.addWidget(frame_Estadistica)

    def actualizar_estilos(self):
        # Actualizar los estilo de la vista
        self.estilo = estilo_app.obtener_estilo_completo()
        colores = self.estilo["colors"]
        
        # Aplicar fondo a la vista principal
        self.setStyleSheet(self.estilo["styles"]["fondo"])
        
        # Actualizar todos los paneles con sombra
        for widget in self.findChildren(QFrame):
            if widget.graphicsEffect():
                widget.setStyleSheet(self.estilo["styles"]["panel"])
                effect = widget.graphicsEffect()
                if isinstance(effect, QGraphicsDropShadowEffect):
                    effect.setColor(QColor(colores.get("shadow", Qt.gray)))
        
        # Actualizar títulos
        for widget in self.findChildren(QLabel):
            text = widget.text()
            if text in ["Bienvenido al Sistema de Gestión", "Control de Reportes"]:
                widget.setStyleSheet(self.estilo["styles"]["header"])
            else:
                widget.setStyleSheet(self.estilo["styles"]["label"])
        
        # Actualizar gráficos circulares
        for widget in self.findChildren(Widget_Graficos):
            widget.repaint()