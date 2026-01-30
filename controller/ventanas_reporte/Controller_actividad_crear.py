from view.ventanas_reporte.vista_actividad_crear import Ventana_reporte_crear
from models.models_reportes.Model_actividad_crear import Guardar_actividad, Actividad
from services.gestor_imgenes import Gestor_imagenes

from comunicador import Comunicador_global

class controlador_reporte_crear():

    def __init__(self):
        self.modelo = Guardar_actividad()
        self.vista = Ventana_reporte_crear(self)
        self.vista.guardar.connect(self.Guardar_datos_actividad)
        self.vista.limpiar.connect(self.limpiar_formulario)

    def get_widget(self):
        return self.vista
    
    def Guardar_actividad(self, titulo, imagen1, imagen2, descripcion, fecha, tipo_actividad):

        try: 
            actividad = Actividad(titulo, imagen1, imagen2, descripcion, fecha, tipo_actividad)
            error = actividad.Validar_datos()

            if error == None:
                datos = Guardar_actividad()
                imagenes_guardar = Gestor_imagenes(imagen1, imagen2)
                
                #creando carpeta
                try:
                    imagenes_guardar.Crear_carpeta()
                except:
                    self.reporte_crear.mensaje_advertencia("Info", "Error al Crear Carpeta")

                # obteniendo imagen con un nuevo nombre
                try:
                    rutas = imagenes_guardar.Copiar_con_nombre_unico()
                    actividad.imagen1 = rutas[0]
                    actividad.imagen2 = rutas[1]
                except:
                    self.reporte_crear.mensaje_advertencia("Info", "No se pudo guardar las imagenes")
                
                datos.Guardar_datos(actividad)
                self.reporte_crear.mensaje_informativo("Info", "Registro Exitoso")
                self.reporte_crear.limpiar_formulario()
                Comunicador_global.actividad_agregada.emit()
                
            else:
                self.reporte_crear.mensaje_advertencia("Info", error)

        except Exception as e:
            self.reporte_crear.mensaje_advertencia("informacion", f"fallo al guardar datos ({e})" )


            
    def Guardar_datos_actividad(self):
        """Retorna todos los datos de la actividad"""
        titulo = self.vista.titulo_actividad.text()
        imagen1 = self.vista.frame_imagen1.get_imagen_path()
        imagen2 = self.vista.frame_imagen2.get_imagen_path()
        descripcion = self.vista.input_reporte.toPlainText()
        fecha = self.vista.fecha.date()
        fecha = fecha.toString("dd-MM-yyyy")
        tipo_actividad = "Anexo"

        self.Guardar_actividad(titulo, imagen1, imagen2, descripcion, fecha, tipo_actividad)

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.vista.titulo_actividad.clear()
        self.vista.input_reporte.clear()
        
        # Restablecer imágenes
        self.imagen1_path = None
        self.imagen2_path = None
        
        # Limpiar frames de imágenes
        self.vista.frame_imagen1.eliminar_imagen()
        self.vista.frame_imagen2.eliminar_imagen()
    