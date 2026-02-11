from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

#ejemplo
#ponderacion = [28, 15, 1, 1, 4]

def Actividad_por_mes(pptx, mes, año, ponderacion):
    # =============================================================================
    # CONFIGURACIÓN INICIAL - PRESENTACIÓN
    # =============================================================================
    mes = mes.upper()

    # Agregar una diapositiva en blanco (layout 6 es diapositiva en blanco)
    slide_layout = pptx.slide_layouts[2]
    diapositiva = pptx.slides.add_slide(slide_layout)
    
    # =============================================================================
    # CONFIGURACIÓN MANUAL DEL TÍTULO
    # =============================================================================
    
    # Definir posición y tamaño del título
    titulo_x = Inches(1)           # Posición horizontal
    titulo_y = Inches(0.6)         # Posición vertical
    titulo_ancho = Inches(8)       # Ancho del cuadro de título
    titulo_alto = Inches(0.5)        # Alto del cuadro de título
    
    # Crear cuadro de texto para el título
    titulo_shape = diapositiva.shapes.add_textbox(titulo_x, titulo_y, titulo_ancho, titulo_alto)
    titulo_frame = titulo_shape.text_frame
    
    # Configurar el texto del título
    titulo_frame.text = f"ACTIVIDADES DE {mes} {año}"
    
    # Configurar propiedades del texto del título
    paragraph = titulo_frame.paragraphs[0]
    run = paragraph.runs[0]
    
    # PROPIEDADES DEL TÍTULO - MODIFICAR SEGÚN NECESIDAD
    run.font.size = Pt(18)                     # Tamaño de fuente
    run.font.bold = True                       # Negrita (True/False)
    run.font.color.rgb = RGBColor(0, 0, 0)   # Color RGB (azul oscuro)
    run.font.name = "calibri"                    # Tipo de fuente
    
    # Alineación del título
    paragraph.alignment = PP_ALIGN.CENTER      # CENTER, LEFT, RIGHT
    titulo_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # =============================================================================
    # CONFIGURACIÓN MANUAL DE LA TABLA
    # =============================================================================
    
    # Definir posición y tamaño de la tabla
    tabla_x = Inches(0.5)          # Posición horizontal
    tabla_y = Inches(1.2)          # Posición vertical (debajo del título)
    tabla_ancho = Inches(9)        # Ancho total de la tabla
    tabla_alto = Inches(5.5)         # Alto total de la tabla
    
    # Definir estructura de la tabla
    filas = 6                     # Número total de filas
    columnas = 3                   # Número total de columnas
    
    # Crear la tabla
    tabla_shape = diapositiva.shapes.add_table(filas, columnas, tabla_x, tabla_y, tabla_ancho, tabla_alto)
    tabla = tabla_shape.table
    
    # =============================================================================
    # CONFIGURACIÓN MANUAL DEL CONTENIDO DE LA TABLA
    # =============================================================================
    
    # ENCABEZADOS (Fila 0)

    tabla.cell(0, 0).text = "OBJETIVO ESPECIFICO"       # Columna 2  
    tabla.cell(0, 1).text = "OBJETIVO OPERACIONAL" # Columna 3
    tabla.cell(0, 2).text = "PONDERACION"      # Columna 4
    
    tabla.cell(1, 0).merge(tabla.cell(5, 0))

    tabla.cell(1, 0).text = """Garantizar el funcionamiento y operatividad de las instalaciones del palacio 
    de gobierno que genere un clima organizacional Idóneo que permita la 
    efectividad 
    de los funcionarios públicos.
    \n 
    Metas a cumplir en actividades (60)-(100%)"""

    # DATOS - Fila 1
    tabla.cell(1, 1).text = "Asegurar el plan de mantenimiento preventivo de todas la instalaciones de la gobernación del estado Monagas para un optimo funcionamiento"
    tabla.cell(1, 2).text = str(ponderacion[0])
    
    # DATOS - Fila 2
    tabla.cell(2, 1).text = "Definir y planificar la política de mantenimiento, con el objetivo de mejorar el modelo preventivo y establecer metodología preventivas de mantenimiento de manera racional"
    tabla.cell(2, 2).text = str(ponderacion[1])
    
    # DATOS - Fila 3
    tabla.cell(3, 1).text = "Crear y mantener actualizado los manuales de mantenimiento preventivo"
    tabla.cell(3, 2).text = str(ponderacion[2])
    
    # DATOS - Fila 4
    tabla.cell(4, 1).text = "Verificar el cumplimiento de los planes, programas , políticas , normas y procedimiento, con la finalidad de optimizar el plan de gobierno regional"
    tabla.cell(4, 2).text = str(ponderacion[3])

    #total de las actividades
    total = sum(int(valores) for valores in ponderacion)

    tabla.cell(5, 1).text = "Asignar el trabajo de mantenimiento, encargándose de la dirección, gestión, y motivación de los equipos de mantenimiento "
    tabla.cell(5, 2).text = f"{str(ponderacion[4])}\nResultado final: {str(total)}"
    
    # =============================================================================
    # FORMATO PERSONALIZADO DE LA TABLA
    # =============================================================================
    
    # FORMATO DE ENCABEZADOS (Fila 0)
    for col in range(columnas):
        celda = tabla.cell(0, col)
        celda.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        # Color de fondo del encabezado
        #celda.fill.solid()
        #celda.fill.fore_color.rgb = RGBColor(59, 89, 152)  # Azul corporativo
        
        # Formato del texto del encabezado
        for paragraph in celda.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)  # Texto blanco
                run.font.bold = True
                run.font.size = Pt(12)
                run.font.name = "Arial"
                
    
    # FORMATO DE CELDAS DE DATOS (Filas 1-4)
    for fila in range(1, filas):
        for col in range(columnas):
            celda = tabla.cell(fila, col)
            
            # Color de fondo alternado para mejor legibilidad
            if fila % 2 == 0:
                celda.fill.solid()
                celda.fill.fore_color.rgb = RGBColor(240, 240, 240)  # Gris claro
            
            # Formato del texto de datos
            for paragraph in celda.text_frame.paragraphs:
                if col in [0, 5]:  # Columnas numéricas alineadas a la derecha
                    paragraph.alignment = PP_ALIGN.CENTER
                    celda.vertical_anchor = MSO_ANCHOR.MIDDLE
                else:  # Columnas de texto alineadas a la izquierda
                    paragraph.alignment = PP_ALIGN.CENTER
                    celda.vertical_anchor = MSO_ANCHOR.MIDDLE
                
                for run in paragraph.runs:
                    run.font.size = Pt(9)
                    run.font.name = "Arial"
                    run.font.color.rgb = RGBColor(0, 0, 0)  # Texto negro
                    run.font.bold = True
    
    # =============================================================================
    # AJUSTES ADICIONALES OPCIONALES
    # =============================================================================
    
    # Ajustar ancho de columnas (opcional)
    # tabla.columns[0].width = Inches(1)   # Columna ID más estrecha
    # tabla.columns[1].width = Inches(3)   # Columna Nombre más ancha
    # tabla.columns[2].width = Inches(2.5) # Columna Departamento
    # tabla.columns[3].width = Inches(2)   # Columna Salario
    #for i in range(1, 5):
    #    tabla.rows[i].height = Inches(0.5)

    

