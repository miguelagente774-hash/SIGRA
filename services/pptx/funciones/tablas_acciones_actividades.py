from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

"""
argumentos de la funcion
pptx = presentacion para añadir las diapositivas
data = informacion de las actividades para cargar en la tabla
"""

def Tabla_acciones_actividades(pptx, data):
    # Crear presentación y diapositiva
    blank_slide_layout = pptx.slide_layouts[1]
    diapositiva = pptx.slides.add_slide(blank_slide_layout)

    # Ajustar el ancho de la tabla desde el inicio
    left = Inches(0.5)
    top = Inches(1)
    width = Inches(9)  # Este es el ancho TOTAL de la tabla
    height = Inches(3.0)

    # 5 filas, 5 columnas

    rows = len(data) + 2
    cols = 5 
    shape = diapositiva.shapes.add_table(rows, cols, left, top, width, height)
    table = shape.table

    # --- 1. Combinar celdas de la primera fila para el título horizontal ---
    table.cell(0, 0).merge(table.cell(0, 4))
    merged_cell = table.cell(0, 0)

    # --- 2. Añadir y formatear el título horizontal ---
    text_frame = merged_cell.text_frame
    text_frame.clear()
    p = text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "ACTIVIDADES O ACCIONES"

    # Propiedades del texto para el título principal
    p.alignment = PP_ALIGN.CENTER
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    run.font.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.name = 'Arial'



    # --- 3. Definir los títulos del header para las columnas ---
    header_titles = ["MUNICIPIO", "PARROQUIA", "COMUNIDAD/INSTITUCIÓN", "FECHA", "DESCRIPCION"]

    for col_idx, title in enumerate(header_titles):
        cell = table.cell(1, col_idx)
        text_frame = cell.text_frame
        text_frame.clear()
        p = text_frame.paragraphs[0]
        run = p.add_run()
        run.text = title
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.font.name = 'Arial'
        text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(200, 200, 200)

    # --- 4. Llenar el resto de los datos --- ejemplo de la variable data
    #data = [
    #    ["MATURIN", "SAN SIMON", "GOBERNACION (PALACIO)", "23/07/2024", "ANEXO"],
    #    ["MATURIN", "SAN SIMON", "GOBERNACION (PALACIO)", "23/07/2024", "ANEXO"],
    #    ["MATURIN", "SAN SIMON", "GOBERNACION (PALACIO)", "23/07/2024", "ANEXO"]
    #]

    for row_idx, row_data in enumerate(data, start=2):
        for col_idx, cell_data in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            text_frame = cell.text_frame
            text_frame.clear()
            p = text_frame.paragraphs[0]
            run = p.add_run()
            run.text = cell_data
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(50, 50, 50)
            run.font.name = 'Calibri'
            run.font.bold = False
            
            # Color de fondo alternado
            if row_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(245, 245, 245)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            
            text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p.alignment = PP_ALIGN.CENTER

    # --- 5. Ajustar alturas de filas ---
    table.rows[0].height = Inches(0.6)  # Título
    table.rows[1].height = Inches(0.5)  # Encabezados
    for i in range(2, rows):
        table.rows[i].height = Inches(0.4)  # Datos

