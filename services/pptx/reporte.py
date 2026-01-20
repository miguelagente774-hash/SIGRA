from pptx import Presentation
from .funciones.Portada import Portada
from .funciones.tablas_acciones_actividades import Tabla_acciones_actividades
from .funciones.tabla_resumen import Tabla_resumen
from .funciones.actividades_por_mes import Actividad_por_mes
from .funciones.Actividades_reporte import Actividad_reporte
from .funciones.Proyecion import Proyeccion
from .funciones.inf_coordinador import Inf_coordinador
from datetime import datetime

def Reporte(Nombre_reporte, directora, fecha, lista_meses, lista_ponderaciones, actividades, datos_coordinador, direccion):
    logo = "services/pptx/funciones/logo.jpg"
    pptx = Presentation("services/pptx/Plantilla.pptx")

    actividad_sin_ordenar = []

    for diccionarios in actividades:
         actividad_sin_ordenar.append(diccionarios)

    actividad = sorted(actividad_sin_ordenar, key=lambda x: datetime.strptime(x['fecha'], '%d-%m-%Y'))

    # Portada de la presentación
    mes1 = fecha["mes1"]
    mes2 = fecha["mes2"]
    mes3 = fecha["mes3"]
    año = fecha["año"]
    porcentaje_total = fecha["porcentaje"]
    meses = [mes1, mes2, mes3, año]
    Portada(pptx, directora, meses, logo)
    
    # Tabla actividades
    datos_actividades = []
    tablas_creadas = 0

    # Procesar actividades en grupos de 10
    for i in range(0, len(actividad), 10):
        # Tomar un grupo de máximo 10 actividades
        grupo_actividades = actividad[i:i+10]
        
        # Limpiar la lista para el nuevo grupo
        datos_actividades = []
        
        # Procesar cada actividad del grupo actual
        for actividades_solas in grupo_actividades:
            datos_actividades.append([
                direccion['municipio'], 
                direccion['parroquia'], 
                direccion['instituto'], 
                actividades_solas["fecha"], 
                actividades_solas["tipo_actividad"]
            ])
        
        # Crear tabla con el grupo actual (máximo 10 actividades)
        Tabla_acciones_actividades(pptx, datos_actividades)
        tablas_creadas += 1
        
        print(f"Tabla {tablas_creadas} creada con {len(grupo_actividades)} actividades")


    # Tabla actividad por mes
    for mes, ponderacion in zip(lista_meses, lista_ponderaciones):
        Actividad_por_mes(pptx, mes, fecha["año"], ponderacion)

    #tabla resumen
    #argumentos(pptx, total_actividades, total_cumplido, año)
    total_actividades = len(datos_actividades)
    tabla_resumen = Tabla_resumen(pptx, total_actividades, porcentaje_total, fecha["año"])

    # Evidencia fotográfica
    evidencia = pptx.slides.add_slide(pptx.slide_layouts[4])

    
        
    for actividades_solas1 in actividad:
            Actividad_reporte(pptx, actividades_solas1["imagen1"], actividades_solas1["imagen2"], actividades_solas1["descripcion"])

    # Proyección de la presentación
    Proyeccion(pptx, directora, fecha["año"], logo)

    # Información del coordinador de mantenimiento
    Nombre_apellido = datos_coordinador.get("nombre_apellido", "")
    decreto = datos_coordinador.get("decreto", "")
    f_publicacion = datos_coordinador.get("fecha_publicacion", "")

    Inf_coordinador(pptx, fecha["año"], Nombre_apellido, decreto, f_publicacion)

    # CORREGIDO: Usar comillas simples dentro de f-string
    nombre_archivo = f"{Nombre_reporte} {fecha['año']}.pptx"
    pptx.save(nombre_archivo)