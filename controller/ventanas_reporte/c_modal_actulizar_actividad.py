from view.ventanas_reporte.v_modal_actulizar_actividad import Modal_actulizar_actividades
from models.models_reportes.m_modal_actulizar_actividad import Modelo_actualizar
from comunicador import Comunicador_global
import os
from services.gestor_imgenes import Gestor_imagenes

class Controller_modal():
    def __init__(self):
        self.modelos = Modelo_actualizar()

    
    def Abrir_modal(self, datos):
        valores_actividad = datos[0]
        
        id_actividad = valores_actividad[0]
        titulo = valores_actividad[1]
        descripcion = valores_actividad[2]
        ruta1 = valores_actividad[3]
        ruta2 = valores_actividad[4]
        fecha = valores_actividad[5]
        
        self.vista = Modal_actulizar_actividades(id_actividad, titulo, descripcion, ruta1, ruta2, fecha, self)
        self.vista.exec_()


    def Actulizar_actividad(self, id_actividad, titulo, descripcion, ruta1, ruta2, fecha, imagen_vieja1, imagen_vieja2):
        try:
            #respaldando la imagen en el programa
            imagenes_guardar = Gestor_imagenes(ruta1, ruta2)

            #creando carpeta
            try:
                imagenes_guardar.Crear_carpeta()
            except:
                self.vista.mensaje_advertencia("Info", "Error al Crear Carpeta")
                
                # obteniendo imagen con un nuevo nombre
            try:
                rutas = imagenes_guardar.Copiar_con_nombre_unico()
                imagenes_guardada1 = rutas[0]
                imagenes_guardada2 = rutas[1]
                
            except:
                self.vista.mensaje_advertencia("Info", "No se pudo guardar las imagenes")

            self.modelos.Actulizar_actividad(id_actividad, titulo, descripcion, imagenes_guardada1, imagenes_guardada2, fecha)
            self.eliminar_imagenes_anteriores(imagen_vieja1, imagen_vieja2)
            
        except Exception as e:
            self.vista.mensaje_error("error", f"{e}")
        
        Comunicador_global.actividad_agregada.emit()
        self.vista.close()
    
    def eliminar_imagenes_anteriores(self, imagen_vieja1, imagen_vieja2):
        #removiendo(eliminado) imagenes anteriores de la carpeta
        os.remove(imagen_vieja1)
        os.remove(imagen_vieja2)