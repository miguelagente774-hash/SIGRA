from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def Tabla_resumen(pptx, total_actividades, porcentaje_meta, año):
    #creando las presentacion y la diapositiva
    diapositiva1 = pptx.slides.add_slide(pptx.slide_layouts[3])

    #deifiniendo las dimensiones de la tabla
    posicion_x = Inches(0.8)
    posicion_y = Inches(1)
    ancho = Inches(8.5)
    alto = Inches(5.8)

    #definiendo las filas y columnas de la tabla
    fila = 4
    columnas = 2

    #creando la tabla para configurarla
    tabla_configuracion = diapositiva1.shapes.add_table(fila, columnas, posicion_x, posicion_y, ancho, alto)

    tabla = tabla_configuracion.table

    #TITULO DE LA TABLA
    tabla.cell(0, 0).merge(tabla.cell(0, 1))
    titulo = tabla.cell(0, 0)

    #darle estilo al texto de las filas
    texto = titulo.text_frame
    texto.clear()
    p = texto.paragraphs[0]
    run = p.add_run()
    run.text = f"RESUMEN DE META CUMPLIDA {año}"

    tabla.rows[0].height = Inches(0.7)

    #estylos
    #alineando texto
    p.alignment = PP_ALIGN.CENTER
    titulo.vertical_anchor = MSO_ANCHOR.MIDDLE
    #estylos de fuente
    run.font.bold = True
    run.font.size = Pt(18)

    data = [
        ["Direccion", "Maturín San Simón \nGobernación palacio"],
        ["Actividad realizada\nTOTAL", f"{total_actividades}"],
        ["Meta cumplida", f"{porcentaje_meta}"]
    ]

    #configurando las filas de la tablas
    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, cell_data in enumerate(row_data):
            cell = tabla.cell(row_idx, col_idx)
            text_frame = cell.text_frame
            text_frame.clear()
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = text_frame.paragraphs[0]
            run = p.add_run()
            p.alignment = PP_ALIGN.CENTER
            run.text = cell_data
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(50, 50, 50)
            run.font.name = 'Arial'
            run.font.bold = False