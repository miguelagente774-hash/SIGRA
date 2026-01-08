from view.vista_consulta import Ventana_consulta
from models.Modelo_consulta import Modelo_consulta
from comunicador import Comunicador_global

class controlador_consulta():
    def __init__(self):
        
        self.modelo = Modelo_consulta()

    def get_widget(self):
        self.consulta = Ventana_consulta(self)
        Comunicador_global.Reporte_agregado.connect(self.consulta.actulizar_tabla)
        return self.consulta
    
    def Obtener_reportes(self):
        try:
            reportes = self.modelo.Obtener_reportes()
            print(reportes)
            return reportes
        except:
            self.consulta.mensaje_error("Error", "Error al Obtener Reporte")


    def Obtener_actividades(self):
        pass

    def Eliminar_reporte(self, id_reporte):
        if id_reporte != None:
            try:
                self.modelo.Eliminar_reporte(id_reporte)
                self.consulta.mensaje_informativo("Informacion", f"Reporte Nro {id_reporte} Eliminado ")
                self.consulta.actulizar_tabla()
            except:
                self.consulta.mensaje_error("Error", "Error al Eliminar Reporte")
        else:
            self.consulta.mensaje_advertencia("Advertencia", "Por favor seleccione un Reporte")