from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

año = 2025
#datos de la gaceta
nombre_apellido = "ANYI YILIBETH ZURITA ISLANDA"
decreto = "Según Decreto N° G-00075-2023 de fecha 1 de Julio de 2023."
f_publicacion = "Publicado en la Gaceta Oficial N° Extraordinario de fecha 1 de julio de 2023"

def Inf_coordinador(pptx, año, nombre_apellido, decreto, f_publicacion):
    nombre_apellido = nombre_apellido.upper()

    diapositiva = pptx.slides.add_slide(pptx.slide_layouts[2])

    columna = 1
    fila = 2
    posicion_x = Inches(0.4)
    posicion_y = Inches(1.8)
    ancho = Inches(9.4)
    alto = Inches(7.2)

    tabla_dimensiones = diapositiva.shapes.add_table(fila, columna, posicion_x, posicion_y, ancho, alto)

    tabla = tabla_dimensiones.table

    titulo = tabla.cell(0, 0)
    tabla.rows[0].height = Inches(0.08)

    titulo.text = f"Proyección del año {año}"

    text = titulo.text_frame
    text.paragraphs[0].alignment = PP_ALIGN.CENTER
    text.vertical_anchor = MSO_ANCHOR.MIDDLE
    text.paragraphs[0].runs[0].font.size = Pt(14)
    text.paragraphs[0].runs[0].font.name = "Arial"
    text.paragraphs[0].runs[0].font.bold = True

    text_1 = tabla.cell(1, 0)
    text = text_1.text_frame

    # Limpiar el texto existente
    text.clear()

    # Lista de textos (sin las líneas vacías adicionales)
    textos = [
        "COORDINACIÓN DE MANTENIMIENTO ADSCRITO DE LA DIRECCIÓN DE DESPACHO DE GOBIERNO",
        "",
        "✅ RESPONSABLE",
        "",
        nombre_apellido,
        "Coordinadora de Mantenimiento",
        decreto,
        f_publicacion
    ]

    # Crear párrafos con formato uniforme
    for texto in textos:
        p = text.add_paragraph()
        p.text = texto
        p.alignment = PP_ALIGN.CENTER  # Todo centrado
        if texto:  # Solo aplicar formato de fuente si el texto no está vacío
            run = p.runs[0]
            run.font.color.rgb = RGBColor(0, 0, 0)
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.name = "Arial"

    # Configurar anchor vertical
    text.vertical_anchor = MSO_ANCHOR.BOTTOM
