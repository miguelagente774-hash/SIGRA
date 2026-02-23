# controlador_estadistica.py
from models.Modelo_estadistica import Modelo_estadistica
from view.vista_estadistica import Ventana_estadística
from comunicador import Comunicador_global  # Asegúrate que esta línea esté así
from typing import List
from PyQt5.QtCore import QTimer

class ControladorEstadistica:
    def __init__(self):
        self.modelo = Modelo_estadistica()
        self.vista = None
        self._conectado = False
        
    def get_widget(self):
        """Crea la vista de estadísticas y actualiza los gráficos con datos reales."""
        self.vista = Ventana_estadística()
        
        # Actualizar todos los gráficos con datos reales
        self.actualizar_todos_graficos()
        
        # Conectar señales para actualización automática
        if not self._conectado:
            try:
                # Conectar las señales de PyQt5
                Comunicador_global.actividad_agregada.connect(self._on_datos_actualizados)
                print("✅ Conectada señal actividad_agregada")
                
                Comunicador_global.Reporte_agregado.connect(self._on_datos_actualizados)
                print("✅ Conectada señal Reporte_agregado")
                
                self._conectado = True
            except Exception as e:
                print(f"❌ Error al conectar señales: {e}")
            
        return self.vista
    
    def actualizar_todos_graficos(self):
        """Actualiza todos los gráficos con los datos más recientes"""
        if not self.vista:
            print("⚠️ Vista no disponible para actualizar")
            return
            
        print("🔄 Actualizando gráficos con datos de BD...")
        
        # Obtener datos del modelo
        contadores = self.modelo.obtener_contadores_periodos()
        objetivos_data = self.modelo.cargar_datos_objetivos()
        
        print("📊 DATOS OBTENIDOS:")
        print(f"   Contadores: {contadores}")
        print(f"   Objetivos: {objetivos_data}")
        
        periodos = ["semanal", "mensual", "trimestral", "anual"]
        nombres_periodos = ["Semanal", "Mensual", "Trimestral", "Anual"]
        
        if not hasattr(self.vista, 'widgets_graficos') or not self.vista.widgets_graficos:
            print("⚠️ No hay widgets de gráficos disponibles")
            return
            
        charts: List = self.vista.widgets_graficos
        print(f"📊 Encontrados {len(charts)} gráficos")
        
        for i, periodo in enumerate(periodos):
            if i < len(charts):
                realizadas = contadores.get(periodo, 0)
                
                if periodo == "semanal":
                    objetivo = int(objetivos_data.get('objetivo_semanal', 0) or 0)
                elif periodo == "mensual":
                    objetivo = int(objetivos_data.get('objetivo_mensual', 0) or 0)
                elif periodo == "trimestral":
                    objetivo = int(objetivos_data.get('objetivo_trimestral', 0) or 0)
                else:
                    objetivo = int(objetivos_data.get('objetivo_anual', 0) or 0)
                
                sin_hacer = max(0, objetivo - realizadas)
                
                print(f"📈 Gráfico {nombres_periodos[i]}:")
                print(f"   Realizadas: {realizadas}")
                print(f"   Objetivo: {objetivo}")
                print(f"   Sin hacer: {sin_hacer}")
                print(f"   Data: [{realizadas}, {sin_hacer}]")
                
                chart = charts[i]
                chart.data = [realizadas, sin_hacer]
                chart.title = f"{nombres_periodos[i]} (Objetivo: {objetivo})"
                chart.update()
                chart.repaint()
        
        print("✅ Gráficos actualizados")
    
    def _on_datos_actualizados(self):
        """Manejador para refrescar los charts cuando se agregue/modifique actividad"""
        print("📢 Señal recibida: datos actualizados")
        QTimer.singleShot(100, self.actualizar_todos_graficos)