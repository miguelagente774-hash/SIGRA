# controller/Controller_main.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout
from controller.Controller_estadisticas import ControladorEstadistica 
from controller.Controller_consulta import controlador_consulta
from controller.Controller_configuraciones import controlador_configuraciones
from controller.ventanas_reporte.Controller_reporte_convertir import controlador_reporte_convertir
from controller.ventanas_reporte.Controller_actividad_crear import controlador_reporte_crear
from controller.ventanas_reporte.Controller_actividades_finalizadas import controlador_reporte_finalizados
from components.menu import Menu
from components.app_style import estilo_app
from comunicador import Comunicador_global

class Controlador_principal(QWidget):
    def __init__(self, ventana):
        super().__init__()
        
        # Configuración inicial
        self.ventana = ventana
        self.layout_principal = QHBoxLayout()
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        self.setLayout(self.layout_principal)

        # Instanciar controladores
        self.estadistica = ControladorEstadistica()
        self.reporte_crear = controlador_reporte_crear()
        self.reporte_finalizados = controlador_reporte_finalizados()
        self.reporte_convertir = controlador_reporte_convertir()
        self.consulta = controlador_consulta()
        self.configuracion = controlador_configuraciones()

        # Registrar vistas para actualización de estilos
        self.registrar_vistas()

        # Crear menú y contenedor de ventanas
        self.crear_menu()
        self.crear_contenedor_ventanas()

        # Conectar señales
        self.conectar_senales()

        # Actualizar estilos iniciales
        self.actualizar_vistas()

    def registrar_vistas(self):
        """Registra todas las vistas para actualización automática de estilos"""
        vistas = [
            self.estadistica.get_widget(),
            self.reporte_crear.get_widget(),
            self.reporte_finalizados.get_widget(),
            self.reporte_convertir.get_widget(),
            self.consulta.get_widget(),
            self.configuracion.get_widget()
        ]
        
        for vista in vistas:
            if vista:
                estilo_app.registrar_vista(vista)
                print(f"✅ Vista registrada: {vista.__class__.__name__}")

    def conectar_senales(self):
        """Conecta todas las señales de la aplicación"""
        
        # 1. Conectar señal de actividad creada desde el controlador
        if hasattr(self.reporte_crear, 'actividad_creada'):
            self.reporte_crear.actividad_creada.connect(
                self.actualizar_estadisticas
            )
            print("✅ Conectada señal actividad_creada del controlador")
        
        # 2. Conectar señal del comunicador global
        Comunicador_global.actividad_agregada.connect(
            self.actualizar_estadisticas
        )
        print("✅ Conectada señal actividad_agregada del comunicador")
        
        # 3. Conectar señal de reporte agregado (opcional)
        Comunicador_global.Reporte_agregado.connect(
            self.actualizar_estadisticas
        )
        print("✅ Conectada señal Reporte_agregado del comunicador")
        
        # 4. Conectar señal de configuración guardada
        if hasattr(self.configuracion, 'Actualizar_Vista'):
            self.configuracion.Actualizar_Vista.connect(
                self.on_config_guardada
            )
            print("✅ Conectada señal de configuración")

    def actualizar_estadisticas(self):
        """Actualiza los gráficos de estadísticas"""
        print("🔄 Actualizando estadísticas...")
        
        if hasattr(self.estadistica, 'actualizar_todos_graficos'):
            self.estadistica.actualizar_todos_graficos()
            print("✅ Estadísticas actualizadas")
        else:
            print("⚠️ No se pudo actualizar estadísticas")

    def crear_menu(self):
        """Crea el menú lateral"""
        self.menu = Menu(self.ventana)
        self.layout_principal.addWidget(self.menu, 1)

    def crear_contenedor_ventanas(self):
        """Crea el contenedor con las ventanas"""
        self.layout_ventanas = QStackedLayout()
        
        # Agregar ventanas al stacked layout
        self.menu.funcion_ventanas(
            self.layout_ventanas,
            self.estadistica.get_widget(),          # Índice 0
            self.reporte_crear.get_widget(),        # Índice 1
            self.reporte_finalizados.get_widget(),  # Índice 2
            self.reporte_convertir.get_widget(),    # Índice 3
            self.consulta.get_widget(),             # Índice 4
            self.configuracion.get_widget()         # Índice 5
        )
        
        self.layout_principal.addLayout(self.layout_ventanas, 3)

    def on_config_guardada(self):
        """Manejador cuando se guarda la configuración"""
        print("⚙️ Configuración guardada, actualizando vistas...")
        self.actualizar_vistas()

    def actualizar_vistas(self):
        """Actualiza todas las vistas con los nuevos estilos"""
        estilo_app.notificar_cambio_estilos()
        print("🎨 Estilos actualizados en todas las vistas")
    
    def mostrar_ventana_principal(self):
        """Muestra la ventana principal después del login"""
        self.layout_ventanas.setCurrentIndex(0)  # Mostrar estadísticas
        self.menu.show()
        print("🏠 Ventana principal mostrada")