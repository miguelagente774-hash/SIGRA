from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def eliminar_objeto(objeto):
    objeto1 = objeto._element
    objeto1.getparent().remove(objeto1)

def Proyeccion(pptx, directora, año, logo):

    diapositiva = pptx.slides.add_slide(pptx.slide_layouts[6])

    #configurando el logo
    imagen = diapositiva.shapes[0]
    posicion_x = imagen.left
    posicion_y = imagen.top
    ancho = imagen.width
    alto = imagen.height

    eliminar_objeto(imagen)

    contenedor_imagen = diapositiva.shapes.add_picture(logo ,posicion_x, posicion_y, ancho, alto)

    #configurando el titulo
    titulo = diapositiva.shapes[0]
    posicion_x = titulo.left
    posicion_y = titulo.top
    ancho = titulo.width
    alto = titulo.height

    eliminar_objeto(titulo)

    contenedor_titulo = diapositiva.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    titulo_edit = contenedor_titulo.text_frame

    titulo_edit.text = "Proyección"
    titulo_edit.paragraphs[0].alignment = PP_ALIGN.CENTER
    titulo_edit.vertical_anchor = MSO_ANCHOR.BOTTOM

    titulo_edit.paragraphs[0].runs[0].font.color.rgb = RGBColor(18, 119, 185)
    titulo_edit.paragraphs[0].runs[0].font.size = Pt(48)
    titulo_edit.paragraphs[0].runs[0].font.name = "Arial"
    titulo_edit.paragraphs[0].runs[0].font.bold = True

    forma = diapositiva.shapes[0]

    posicion_x = forma.left
    posicion_y = forma.top
    ancho = forma.width
    alto = forma.height

    eliminar_objeto(forma)

    contenedor = diapositiva.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    texto_coordinacion = contenedor.text_frame

    texto_coordinacion.text = f"Proyección del {año}:\nGarantizar el funcionamiento y operatividad de las instalaciones del palacio de gobierno que genere un clima organizacional Idóneo que permita la efectividad de los funcionarios públicos"

    texto_coordinacion.paragraphs[0].alignment = PP_ALIGN.CENTER
    texto_coordinacion.vertical_anchor = MSO_ANCHOR.MIDDLE

    texto_coordinacion.paragraphs[0].runs[0].font.size = Pt(18)
    texto_coordinacion.paragraphs[0].runs[0].font.name = "Arial"
    texto_coordinacion.paragraphs[0].runs[0].font.bold = True

    texto_coordinacion.word_wrap = True  # Ajuste de líneas
    texto_coordinacion.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE  # Ajusta texto al contenedor

    texto_coordinacion.paragraphs[1].alignment = PP_ALIGN.CENTER
    texto_coordinacion.paragraphs[1].runs[0].font.italic = True
    texto_coordinacion.paragraphs[1].runs[0].font.name = "Arial"

    #crando titulo de direccion de despacho
    forma = diapositiva.shapes[0]

    posicion_x = forma.left
    posicion_y = forma.top
    ancho = forma.width
    alto = forma.height

    eliminar_objeto(forma)

    contenedor = diapositiva.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    texto_coordinacion = contenedor.text_frame

    texto_coordinacion.text = "DIRECCIÓN DEL DESPACHO"

    texto_coordinacion.paragraphs[0].alignment = PP_ALIGN.CENTER
    texto_coordinacion.vertical_anchor = MSO_ANCHOR.MIDDLE

    #background
    fill_titulo = contenedor.fill
    fill_titulo.solid()
    fill_titulo.fore_color.rgb = RGBColor(24, 144, 70)
    texto_coordinacion.paragraphs[0].runs[0].font.size = Pt(18)
    texto_coordinacion.paragraphs[0].runs[0].font.name = "Arial"
    texto_coordinacion.paragraphs[0].runs[0].font.bold = True
    texto_coordinacion.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    #configurando el titulo y el nombre de la directora
    forma2 = diapositiva.shapes[0]
    posicion_x = forma2.left
    posicion_y = forma2.top
    ancho = forma2.width
    alto = forma2.height

    eliminar_objeto(forma2)

    contenedor_text = diapositiva.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    texto_m = contenedor_text.text_frame

    texto_m.text = f"Directora: {directora}"
    texto_m.paragraphs[0].alignment = PP_ALIGN.CENTER
    texto_m.vertical_anchor = MSO_ANCHOR.MIDDLE

    texto_m.paragraphs[0].runs[0].font.size = Pt(14)
    texto_m.paragraphs[0].runs[0].font.name = "Arial"
    texto_m.paragraphs[0].runs[0].font.bold = True
