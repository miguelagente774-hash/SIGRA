from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect,
    QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont
from components.app_style import estilo_app

estilo = estilo_app.obtener_estilo_completo()

# --- Funciones de Utilidad ---
def get_shadow_effect(radius, color=Qt.gray, offset_x=1, offset_y=1):
    """Crea y configura un efecto de sombra."""
    sombra = QGraphicsDropShadowEffect()
    sombra.setBlurRadius(radius)
    sombra.setColor(color)
    sombra.setOffset(offset_x, offset_y)
    return sombra

def create_card(title, amount, border_color):
    """Crea una tarjeta de resumen estilizada."""
    layout = QVBoxLayout()
    layout.setContentsMargins(15, 5, 15, 5)

    frame = QFrame()
    frame.setStyleSheet(estilo["styles"]["panel"])
    frame.setLayout(layout)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    frame.setGraphicsEffect(get_shadow_effect(15, QColor(0, 0, 0, 50)))

    # Título
    title_label = QLabel(title)
    title_label.setStyleSheet(estilo["styles"]["label"])
    layout.addWidget(title_label)

    # Cantidad
    amount_label = QLabel(amount)
    amount_label.setStyleSheet(estilo["styles"]["label"])
    layout.addWidget(amount_label)

    layout.addStretch(1)
    return frame

# --- Clase para el Widget del Gráfico Circular Nativo (QPainter) ---
# --- Clase para el Widget del Gráfico Circular Nativo (QPainter) ---
class CustomPieChartWidget(QFrame):
    """Un QFrame que dibuja un gráfico circular simple usando QPainter."""

    def __init__(self, title, chart_data=None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(160)  # Aumentado para espacio del título
        self.setStyleSheet("background: transparent; border: none;")
        
        # Data Configuration
        data_default = [70, 30]
        labels_default = ["Actividades Realizadas", "Actividades sin Hacer"]
        
        self.data = chart_data.get('data', data_default) if chart_data else data_default
        self.labels = chart_data.get('labels', labels_default) if chart_data else labels_default
        self.title = title
        self.colors = [
            QColor(estilo_app.obtener_colores_tema()['primary']), 
            QColor(estilo_app.obtener_colores_tema()['text_secondary'])
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
        title_height = 30  # Altura reservada para el título
        title_rect = QRectF(rect.left(), rect.top(), rect.width(), title_height)
        
        label_style = estilo["styles"]["label"]
        
        # Fondo para el título (opcional, puedes quitarlo si quieres)
        painter.setBrush(QBrush(QColor(estilo_app.obtener_colores_tema()['bg_secondary'])))
        painter.setPen(Qt.NoPen)
        painter.drawRect(title_rect)
        
        # Texto del título
        painter.setPen(QPen(QColor(estilo_app.obtener_colores_tema()['text_primary'])))
        title_font = QFont(estilo_app.FONT_FAMILY, estilo_app.FONT_SIZE + 5, QFont.Bold)
        painter.setFont(title_font)
        
        # Ajustar texto si es muy largo
        display_title = self.title
        if len(self.title) > 30:  # Si el título es muy largo
            # Intentar cortar inteligentemente
            if "Objetivo:" in self.title:
                # Mantener la primera parte y el objetivo
                parts = self.title.split("Objetivo:")
                if len(parts) > 1:
                    display_title = f"{parts[0].strip()}... Objetivo:{parts[1]}"
            else:
                display_title = self.title[:27] + "..."
        
        painter.drawText(title_rect, Qt.AlignCenter | Qt.AlignVCenter, display_title)
        
        # ===== 2. PINTAR EL GRÁFICO =====
        # Área para el gráfico (dejando espacio para el título)
        chart_area = QRectF(
            rect.left() + 5, 
            rect.top() + title_height + 5,  # +5 para separación
            rect.width() - 10, 
            rect.height() - title_height - 10
        )
        
        # Factor de escala para responsividad
        scale_factor = rect.width() / 250
        DYN_FONT_SIZE = max(7, int(8 * scale_factor))  # Aumentado para mejor legibilidad
        DYN_ICON_SIZE = max(5, int(5 * scale_factor))
        DYN_LEGEND_SPACING = max(10, int(12 * scale_factor))
        
        TEXT_MARGIN_LEFT = 3
        
        # Dimensiones del Gráfico
        PIE_WIDTH_RATIO = 0.35
        pie_area_width = chart_area.width() * PIE_WIDTH_RATIO
        diameter = min(pie_area_width, chart_area.height()) - 10
        center_x = chart_area.left() + pie_area_width / 2
        center_y = chart_area.top() + chart_area.height() / 2
        pie_rect = QRectF(center_x - diameter / 2, center_y - diameter / 2, diameter, diameter)

        total = sum(self.data)
        start_angle = 90 * 16 
        
        # Posición de la Leyenda
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

                # Dibujar la porción del pastel
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(Qt.white, 1))
                painter.drawPie(pie_rect, start_angle, span_angle)

                # Dibujar la Leyenda
                current_item_y_pos = legend_y + (i * DYN_LEGEND_SPACING)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawRect(int(legend_x), int(current_item_y_pos), DYN_ICON_SIZE, DYN_ICON_SIZE)
                
                # Texto de leyenda
                text_color = estilo_app.obtener_colores_tema()['text_primary']
                painter.setPen(QPen(QColor(text_color)))
                
                # Acortar texto si es necesario
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

            # Centro blanco para efecto dona
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
        
        # ===== 3. BORDE SUAVE ALREDEDOR DEL WIDGET =====
        painter.setPen(QPen(QColor(estilo_app.obtener_colores_tema()['border_light']), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 5, 5)


# ---------------------------------------

class Ventana_principal(QFrame):
    def __init__(self):
        super().__init__()
        self.layout_main = QVBoxLayout(self)
        self.setStyleSheet(estilo["styles"]["fondo"])
        self.setup_panel()
        self.setup_charts_panel()
        self.layout_main.addStretch(1) 

         # Registrar esta vista para actualización automática
        estilo_app.registrar_vista(self)
        
        # Conectar señal de actualización
        estilo_app.estilos_actualizados.connect(self.actualizar_estilos)

    def setup_panel(self):
        layout_content = QVBoxLayout()

        Contenedor_panel = QFrame()
        Contenedor_panel.setMinimumHeight(250)
        Contenedor_panel.setMaximumHeight(300)
        Contenedor_panel.setStyleSheet(estilo["styles"]["panel"])
        Contenedor_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        Contenedor_panel.setGraphicsEffect(get_shadow_effect(25))
        
        Contenedor_panel.setLayout(layout_content)
        layout_content.setContentsMargins(30, 0, 30, 0)
        layout_content.setSpacing(0) 

        titulo = QLabel("Bienvenido al Sistema de Gestión")
        titulo.setStyleSheet(estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignCenter)
        layout_content.addWidget(titulo)

        self.layout_main.addWidget(Contenedor_panel, 0, alignment=Qt.AlignTop)

    def setup_charts_panel(self):
        layout_estadistica = QVBoxLayout()
        layout_estadistica.setSpacing(3) 
        
        frame_Estadistica = QFrame()
        frame_Estadistica.setStyleSheet(estilo["styles"]["panel"])
        frame_Estadistica.setLayout(layout_estadistica)
        frame_Estadistica.setGraphicsEffect(get_shadow_effect(15))

        titulo = QLabel("Control de Reportes")
        titulo.setStyleSheet(estilo["styles"]["header"])
        titulo.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout_estadistica.addWidget(titulo)

        layout_charts = QGridLayout()
        layout_charts.setContentsMargins(15, 15, 15, 15)
        layout_charts.setSpacing(15)
        
        charts_container = QFrame()
        charts_container.setLayout(layout_charts)
        
        common_labels = ['Actividades Realizadas', 'Actividades sin Hacer']
        
        data = [
            {'title': "Semanal (Objetivo: 8)", 'data': [7, 1], 'labels': common_labels},
            {'title': "Mensual (Objetivo: 20)", 'data': [16, 4], 'labels': common_labels},
            {'title': "Trimestral (Objetivo: 30)", 'data': [25, 5], 'labels': common_labels},
            {'title': "Anual (Objetivo: 120)", 'data': [100, 20], 'labels': common_labels},
        ]

        for i, chart_data in enumerate(data):
            row, col = divmod(i, 2)
            chart = CustomPieChartWidget(chart_data['title'], chart_data)
            layout_charts.addWidget(chart, row, col)
            
        layout_estadistica.addWidget(charts_container)
        self.layout_main.addWidget(frame_Estadistica)

    def actualizar_estilos(self):
        """Actualiza los estilos de esta vista"""
        # Obtener nuevo estilo
        estilo = estilo_app.obtener_estilo_completo()
        
        # Aplica los estilos a tus componentes
        self.setStyleSheet(estilo["styles"]["fondo"])
        
        # Actualizar paneles
        if hasattr(self, 'panel_interfaz'):
            self.panel_interfaz.setStyleSheet(estilo["styles"]["panel"])
            
        # Actualizar labels con estilo de título
        for widget in self.findChildren(QLabel):
            if widget.text() in ["Bienvenido al Sistema de Gestión", "Control de Reportes"]:
                widget.setStyleSheet(estilo["styles"]["header"])
            else:
                widget.setStyleSheet(estilo["styles"]["title"])
        
        print(f"🔄 {self.__class__.__name__} actualizada")