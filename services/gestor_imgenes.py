import os
import shutil
from datetime import datetime

class Gestor_imagenes:
    def __init__(self, imagen_ruta1, imagen_ruta2):
        self.ruta1 = imagen_ruta1
        self.ruta2 = imagen_ruta2
        
        self.Crear_carpeta()

    def Crear_carpeta(self):   
        #creando carpeta para las imagenes de las actividades
        Carpeta_imagenes = "Actividades_imagenes" # nombre de la carpeta
        os.makedirs(Carpeta_imagenes, exist_ok=True)

    def Copiar_con_nombre_unico(self):
        #obteniendo nombre de la imagen sin su ruta completa
        nombre_imagen1 = os.path.basename(self.ruta1)
        nombre_imagen2 = os.path.basename(self.ruta2)

        #separamos nombre de la imagen con su extencion
        nombre_base1, extension1 = os.path.splitext(nombre_imagen1)
        nombre_base2, extension2 = os.path.splitext(nombre_imagen2)

        #creamos nombre unico con la fecha actual
        #obtenemos la hora primero
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_unico1 = f"imagen1_{fecha}_{extension1}"
        nombre_unico2 = f"imagen2_{fecha}_{extension2}"

        destino_completo1 = os.path.join("Actividades_imagenes", nombre_unico1)
        destino_completo2 = os.path.join("Actividades_imagenes", nombre_unico2)

        nueva_ruta1 = f"Actividades_imagenes/{nombre_unico1}"
        nueva_ruta2 = f"Actividades_imagenes/{nombre_unico2}"

        rutas = [nueva_ruta1, nueva_ruta2]

        shutil.copy2(self.ruta1, destino_completo1)
        shutil.copy2(self.ruta2, destino_completo2)

        return rutas