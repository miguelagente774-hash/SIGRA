from view.ventanas_reporte.vista_actividades_finalizadas import Ventana_reporte_finalizados
from models.models_reportes.Model_actividad_finalizadas import Modelo_actividades_finalizadas
from controller.ventanas_reporte.c_modal_actulizar_actividad import Controller_modal
from comunicador import Comunicador_global
import os


class controlador_reporte_finalizados():
    def __init__(self):
        self.Controller_modal = Controller_modal()
        self.modelo = Modelo_actividades_finalizadas()
        self.actividades_finalizadas = Ventana_reporte_finalizados(self)
        Comunicador_global.actividad_agregada.connect(self.actividades_finalizadas.actulizar_tabla)
    #funcion para que se muestre la vista en el programa
    def get_widget(self):
        return self.actividades_finalizadas
    
    #funciones del programa
    def Obtener_datos_tabla(self):
        try:
            datos = self.modelo.Obtener_datos()
            return datos
        
        except Exception as e:
           self.actividades_finalizadas.Mensaje_error("error", f"{e}")


    def Abrir_modal(self):
        id_actividad = None
        datos = None
        try:
            id_actividad = self.actividades_finalizadas.Obtener_indice_tabla()
        except:
                self.actividades_finalizadas.Mensaje_Warning("Advertencia", "Error al cargar el indice")

        if id_actividad != None:
            datos = self.modelo.Obtener_datos_actividad(id_actividad)
        else:
            self.actividades_finalizadas.Mensaje_Warning("Advertencia", "Por favor seleccione una fila")
            
        if datos != None:
            try:
                self.Controller_modal.Abrir_modal(datos)
                self.actividades_finalizadas.Limpiar_seleccion_fila()
            except:
                self.actividades_finalizadas.Mensaje_error("error", "Nose pudo abrir la ventana")
        
        
    
    def Eliminar_actividad(self, id_actividad):
        if id_actividad != None:
                #elimando images de la actividad a eliminar (para ahorrar memoria en el disco)
                try:
                    imagenes = self.modelo.Obtener_url_imagenes(id_actividad)
                    rutas = imagenes[0]
                    os.remove(rutas[0])
                    os.remove(rutas[1])
                except:
                    self.actividades_finalizadas.Mensaje_error("error", "Nose pudo eliminar la imagenes")
                #eliminando datos de la actividad de la base de datos
                self.modelo.Eliminar_datos(id_actividad)
                self.actividades_finalizadas.actulizar_tabla()
                Comunicador_global.actividad_agregada.emit()   
        else:
            self.actividades_finalizadas.Mensaje_Warning("Advertencia", "Por favor seleccione una fila")

            

    
    
    