# controlador_estadistica.py
from models.Modelo_estadistica import Modelo_estadistica
from view.vista_estadistica import Ventana_principal, CustomPieChartWidget
from comunicador import Comunicador_global
from typing import Dict, List, Any


class ControladorEstadistica:
    def __init__(self):
        self.modelo = Modelo_estadistica()

    def get_widget(self):
        """Crea la vista de estadísticas y actualiza los gráficos con datos reales."""
        self.estadistica = Ventana_principal()

        # Obtener contadores desde el modelo
        contadores = self.modelo.obtener_contadores_periodos()

        # Objetivos mostrados en la vista (mismo orden que los charts)
        objetivos = [8, 20, 30, 120]
        periodos = ["semanal", "mensual", "trimestral", "anual"]

        # Buscar widgets de tipo CustomPieChartWidget dentro de la vista
        charts: List[CustomPieChartWidget] = self.estadistica.findChildren(CustomPieChartWidget)

        for i, periodo in enumerate(periodos):
            if i < len(charts):
                realizadas = contadores.get(periodo, 0)
                objetivo = objetivos[i]
                sin_hacer = max(0, objetivo - realizadas)

                chart = charts[i]
                chart.data = [realizadas, sin_hacer]
                chart.labels = ["Actividades Realizadas", "Actividades sin Hacer"]
                chart.update()

        # Conectar señales para actualizar automáticamente cuando cambien datos
        try:
            Comunicador_global.actividad_agregada.connect(self._on_datos_actualizados)
            Comunicador_global.Reporte_agregado.connect(self._on_datos_actualizados)
        except Exception:
            # Señales ya conectadas o PySignal no soporta double-connect de forma evidente
            pass

        return self.estadistica

    def _on_datos_actualizados(self):
        """Manejador para refrescar los charts cuando se agregue/modifique actividad o reportes."""
        contadores = self.modelo.obtener_contadores_periodos()
        objetivos = [8, 20, 30, 120]
        periodos = ["semanal", "mensual", "trimestral", "anual"]

        charts: List[CustomPieChartWidget] = self.estadistica.findChildren(CustomPieChartWidget)
        for i, periodo in enumerate(periodos):
            if i < len(charts):
                realizadas = contadores.get(periodo, 0)
                objetivo = objetivos[i]
                sin_hacer = max(0, objetivo - realizadas)

                chart = charts[i]
                chart.data = [realizadas, sin_hacer]
                chart.update()