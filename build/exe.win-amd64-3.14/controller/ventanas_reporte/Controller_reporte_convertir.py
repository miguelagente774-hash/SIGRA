from view.ventanas_reporte.vista_reporte_convertir import Ventana_convertir_reporte
from models.models_reportes.modelo_reporte_convertir import Modelo_reporte
from comunicador import Comunicador_global

class controlador_reporte_convertir():
    def __init__(self):
        self.modelo = Modelo_reporte()
        self.vista_reporte_convertir = Ventana_convertir_reporte(self)

    def get_widget(self):
        return self.vista_reporte_convertir
    
    def Obtener_actividades(self):
        try:
            datos = self.modelo.Obtener_actividades()

        except Exception as e:
            self.vista_reporte_convertir.mensaje_error("Error", f"Error al obtener actividades: {str(e)}")
            datos = []
        return datos

    def Guardar_datos_reporte(self, nombre_reporte, actividades_ids):
        """Guarda un nuevo reporte con actividades seleccionadas"""
        try:
            # Llamar al modelo para guardar
            exito, mensaje = self.modelo.Guardar_datos_reporte(nombre_reporte, actividades_ids)
            
            if exito:
                self.vista_reporte_convertir.mensaje_informativo("Éxito", mensaje)
                # Limpiar selección y nombre después de guardar
                self.vista_reporte_convertir.campo_nombre_reporte.clear()
                self.limpiar_seleccion()
                Comunicador_global.Reporte_agregado.emit()
            else:
                self.vista_reporte_convertir.mensaje_error("Error", mensaje)
                
        except Exception as e:
            self.vista_reporte_convertir.mensaje_error("Error", f"Error inesperado: {str(e)}")

    def limpiar_seleccion(self):
        """Limpia todos los checkboxes seleccionados"""
        for fila in range(self.vista_reporte_convertir.tabla_actividades.rowCount()):
            checkbox = self.vista_reporte_convertir.tabla_actividades.cellWidget(fila, 0)
            if checkbox:
                checkbox.setChecked(False)