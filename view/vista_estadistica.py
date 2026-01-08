import sys
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFrame, QLabel, QGraphicsDropShadowEffect,
    QSizePolicy, QWidget, QGridLayout, QApplication
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont

# Variables globales para consistencia
FONT_FAMILY = "Arial"
COLOR_PRIMARIO = "#005a6e" 
COLOR_AZUL_HOVER = "#00485a"
COLOR_SECUNDARIO = "#F44336"
BG_COLOR_PANEL = "rgba(255, 255, 255, 0.9)"
BG_COLOR_FONDO = "#E3EFF3"
SHADOW_RADIUS_L = 25
SHADOW_RADIUS_S = 15

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
    frame.setStyleSheet(f"""
        background: white;
        border-radius: 10px;
        border-left: 5px solid {border_color};
        padding: 0;""")
    frame.setLayout(layout)
    frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    frame.setGraphicsEffect(get_shadow_effect(SHADOW_RADIUS_S, QColor(0, 0, 0, 50)))

    # Título
    title_label = QLabel(title)
    title_label.setStyleSheet("margin: 0; background: none; border: none; font-size: 14px; color: #555555; font-weight: bold;")
    layout.addWidget(title_label)

    # Cantidad
    amount_label = QLabel(amount)
    amount_label.setStyleSheet(f"margin: 0; background: none; border: none; font-size: 28px; color: {border_color}; font-weight: bold;")
    layout.addWidget(amount_label)

    layout.addStretch(1)
    return frame

# --- Clase para el Widget del Gráfico Circular Nativo (QPainter) ---
class CustomPieChartWidget(QFrame):
    """Un QFrame que dibuja un gráfico circular simple usando QPainter."""

    def __init__(self, title, chart_data=None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self.setStyleSheet("background: white; border-radius: 15px;")

        # Data Configuration
        data_default = [70, 30]
        labels_default = ["Realizadas", "Sin Hacer"]
        
        self.data = chart_data.get('data', data_default) if chart_data else data_default
        self.labels = chart_data.get('labels', labels_default) if chart_data else labels_default
        self.colors = [QColor(COLOR_PRIMARIO), QColor(COLOR_SECUNDARIO)]
        
        # Sombra
        self.setGraphicsEffect(get_shadow_effect(SHADOW_RADIUS_S))

        # Layout y Título
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        chart_title = QLabel(title)
        chart_title.setStyleSheet(f"font-family: {FONT_FAMILY}; font-size: 12px; font-weight: bold; color: black; background: none; qproperty-alignment: 'AlignRight';")
        chart_title.setWordWrap(True)

        main_layout.addWidget(chart_title)
        main_layout.addStretch(1)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.contentsRect()
        TITLE_HEIGHT = 20
        TEXT_ICON_SIZE = 7
        TEXT_MARGIN_LEFT = 3
        LEGEND_SPACING = 15
        
        chart_area = QRectF(rect.left() + 5, rect.top() + TITLE_HEIGHT, rect.width() - 10, rect.height() - TITLE_HEIGHT - 5)
        
        # Dimensiones del Gráfico
        PIE_WIDTH_RATIO = 0.35
        pie_area_width = chart_area.width() * PIE_WIDTH_RATIO
        diameter = min(pie_area_width, chart_area.height()) - 5
        center_x = chart_area.left() + pie_area_width / 2
        center_y = chart_area.top() + chart_area.height() / 2
        pie_rect = QRectF(center_x - diameter / 2, center_y - diameter / 2, diameter, diameter)

        total = sum(self.data)
        start_angle = 90 * 16 # Start from top (90 deg)
        
        # Posición inicial de la Leyenda
        legend_x = chart_area.left() + pie_area_width + 5
        total_items = len(self.data) if self.data else 1
        chart_area_center_y = chart_area.top() + chart_area.height() / 2
        # Calcula el punto de inicio para centrar la leyenda verticalmente
        legend_y = chart_area_center_y - (((total_items - 1) * LEGEND_SPACING) / 2) - 3.5
        
        painter.setFont(QFont(FONT_FAMILY, 7))

        if total > 0 and self.data:
            for i, value in enumerate(self.data):
                percentage = (value / total)
                span_angle = round(percentage * 360 * 16)
                color = self.colors[i % len(self.colors)]

                # a) Dibujar la porción del pastel
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(Qt.white, 1))
                painter.drawPie(pie_rect, start_angle, span_angle)

                # b) Dibujar la Leyenda
                current_item_y_pos = legend_y + (i * LEGEND_SPACING)
                painter.setPen(QPen(Qt.black))
                painter.setBrush(QBrush(color))
                painter.drawRect(int(legend_x), int(current_item_y_pos), TEXT_ICON_SIZE, TEXT_ICON_SIZE)
                
                label_text = f"{self.labels[i]} ({percentage*100:.1f}%)"
                
                text_rect = QRectF(
                    int(legend_x) + TEXT_ICON_SIZE + TEXT_MARGIN_LEFT,
                    int(current_item_y_pos),
                    chart_area.right() - (int(legend_x) + TEXT_ICON_SIZE + TEXT_MARGIN_LEFT) - 5,
                    LEGEND_SPACING
                )
                painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, label_text)

                start_angle += span_angle
        else:
            painter.setPen(QPen(Qt.darkGray))
            painter.drawText(chart_area.toRect(), Qt.AlignCenter, "Sin Datos")


# ---------------------------------------

class Ventana_principal(QFrame):
    def __init__(self):
        super().__init__()
        self.layout_main = QVBoxLayout(self)
        self.setStyleSheet(f"background: {BG_COLOR_FONDO};")
        self.setup_panel()
        self.setup_charts_panel()
        # Asegurar que el último layout tenga el stretch
        self.layout_main.addStretch(1) 

    # ----- Panel de Tarjetas de resumen (Dashboard) ---------
    def setup_panel(self):
        layout_content = QVBoxLayout()
        layout_h_cards = QHBoxLayout()

        # Contenedor Principal (Marco Estilizado)
        Contenedor_panel = QFrame()
        Contenedor_panel.setMinimumHeight(250)
        Contenedor_panel.setMaximumHeight(300)
        Contenedor_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        Contenedor_panel.setStyleSheet(f"background: {BG_COLOR_PANEL}; margin: 20px 40px; border-radius: 20px; font-family: {FONT_FAMILY};")
        Contenedor_panel.setGraphicsEffect(get_shadow_effect(SHADOW_RADIUS_L))
        
        Contenedor_panel.setLayout(layout_content)
        layout_content.setContentsMargins(30, 0, 30, 0)
        layout_content.setSpacing(0) # Eliminar espacio vertical entre el título y las tarjetas

        # Titulo Principal
        titulo = QLabel("Bienvenido al Sistema de Gestión")
        titulo.setStyleSheet("background: none; font-size: 30px; color: black; font-weight: bold; margin: 0; padding: 5px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_content.addWidget(titulo)

        # Titulo de Resumen
        #titulo2 = QLabel("Resumen de Reportes Creados")
        #titulo2.setStyleSheet("background: none; font-size: 16px; color: black; font-weight: bold; padding: 5px; margin: 0 10px;") # Se ajusta el margen inferior para el espaciado
        #titulo2.setAlignment(Qt.AlignCenter)
        #layout_content.addWidget(titulo2)

        # Crear y agregar tarjetas
        #layout_h_cards.addWidget(create_card("Creados Hoy", "42", "#21BCFF"))
        #layout_h_cards.addWidget(create_card("Creados Último Mes", "785", "#FFC107"))
        #layout_h_cards.addWidget(create_card("Total Histórico", "3450", "#4CAF50"))
        #layout_h_cards.setSpacing(20)
        
        #layout_content.addLayout(layout_h_cards)
        #layout_content.addStretch(1)

        self.layout_main.addWidget(Contenedor_panel, 0, alignment=Qt.AlignTop)

    # --------- IMPLEMENTACIÓN DE LOS GRÁFICOS (NATIVO QPainter) -------------
    def setup_charts_panel(self):
        layout_estadistica = QVBoxLayout()
        layout_estadistica.setSpacing(3) # Espacio entre el título de sección y la cuadrícula de gráficos
        
        frame_Estadistica = QFrame()
        frame_Estadistica.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            background: {BG_COLOR_PANEL};
            margin: 20px;
            margin-top: 0px; 
            margin-bottom: 0px;
            border-radius: 20px;""")
        frame_Estadistica.setLayout(layout_estadistica)
        frame_Estadistica.setGraphicsEffect(get_shadow_effect(SHADOW_RADIUS_S))

        # Titulo general de la sección
        titulo = QLabel("Control de Reportes")
        titulo.setStyleSheet("font-size: 22px; color: black; font-weight: bold; margin: 0;; padding: 5px 0;")
        titulo.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout_estadistica.addWidget(titulo)

        # Contenedor y Layout de rejilla (GridLayout) para los 4 gráficos
        layout_charts = QGridLayout()
        layout_charts.setContentsMargins(15, 15, 15, 15)
        layout_charts.setSpacing(15)
        
        charts_container = QFrame()
        charts_container.setLayout(layout_charts)
        
        # Configuración y Creación de Gráficos
        common_labels = ['Actividades Realizadas', 'Actividades sin Hacer']
        
        data = [
            {'title': "Semanal (Objetivo: 8)", 'data': [7, 1], 'labels': common_labels},
            {'title': "Mensual (Objetivo: 20)", 'data': [16, 4], 'labels': common_labels},
            {'title': "Trimestral (Objetivo: 30)", 'data': [25, 5], 'labels': common_labels},
            {'title': "Anual (Objetivo: 120)", 'data': [100, 20], 'labels': common_labels},
        ]

        # Agregar los gráficos a la cuadrícula (2x2)
        for i, chart_data in enumerate(data):
            row, col = divmod(i, 2)
            chart = CustomPieChartWidget(chart_data['title'], chart_data)
            layout_charts.addWidget(chart, row, col)
            
        layout_estadistica.addWidget(charts_container)
        self.layout_main.addWidget(frame_Estadistica)
