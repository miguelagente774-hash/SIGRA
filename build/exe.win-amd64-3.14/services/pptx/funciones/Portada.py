from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def eliminar_objeto(objeto):
    objeto1 = objeto._element
    objeto1.getparent().remove(objeto1)

"""
argumentos de la funcion
pptx = presentacion para añadir las diapositivas
directora = directora de la institucion actualmente
fecha = se refiere a al trimestre al que pertenece el informe o reporte
"""
def Portada(pptx, directora, fecha, logo):

    diapositiva1 = pptx.slides.add_slide(pptx.slide_layouts[5])

    #configurando el logo
    imagen = diapositiva1.shapes[0]
    posicion_x = imagen.left
    posicion_y = imagen.top
    ancho = imagen.width
    alto = imagen.height

    eliminar_objeto(imagen)

    contenedor_imagen = diapositiva1.shapes.add_picture(logo, posicion_x, posicion_y, ancho, alto)

    #configurando el titulo
    titulo = diapositiva1.shapes[0]
    posicion_x = titulo.left
    posicion_y = titulo.top
    ancho = titulo.width
    alto = titulo.height

    eliminar_objeto(titulo)

    contenedor_titulo = diapositiva1.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    titulo_edit = contenedor_titulo.text_frame

    titulo_edit.text = "BALANCE TRIMESTRAL"
    titulo_edit.paragraphs[0].alignment = PP_ALIGN.CENTER
    titulo_edit.vertical_anchor = MSO_ANCHOR.MIDDLE

    titulo_edit.paragraphs[0].runs[0].font.color.rgb = RGBColor(18, 119, 185)
    titulo_edit.paragraphs[0].runs[0].font.size = Pt(48)
    titulo_edit.paragraphs[0].runs[0].font.name = "Arial"
    titulo_edit.paragraphs[0].runs[0].font.bold = True

    # coordinacion de mantenimiento subtitulo
    forma = diapositiva1.shapes[0]
    posicion_x = forma.left
    posicion_y = forma.top
    ancho = forma.width
    alto = forma.height

    eliminar_objeto(forma)

    contenedor = diapositiva1.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    texto_coordinacion = contenedor.text_frame

    texto_coordinacion.text = "COORDINACION DE MANTENIMIENTO"

    texto_coordinacion.paragraphs[0].alignment = PP_ALIGN.CENTER
    texto_coordinacion.vertical_anchor = MSO_ANCHOR.MIDDLE

    texto_coordinacion.paragraphs[0].runs[0].font.size = Pt(20)
    texto_coordinacion.paragraphs[0].runs[0].font.name = "calibri"
    texto_coordinacion.paragraphs[0].runs[0].font.bold = True

    # informe con sus meses del trimestre
    forma1 = diapositiva1.shapes[0]

    posicion_x = forma1.left
    posicion_y = forma1.top
    ancho = forma1.width
    alto = forma1.height

    eliminar_objeto(forma1)

    contenedor_text = diapositiva1.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    texto_m = contenedor_text.text_frame

    texto_m.text = f"Informe-{fecha[0]}-{fecha[1]}-{fecha[2]}-{fecha[3]}"
    texto_m.paragraphs[0].alignment = PP_ALIGN.CENTER
    texto_m.vertical_anchor = MSO_ANCHOR.MIDDLE


    texto_m.paragraphs[0].runs[0].font.size = Pt(24)
    texto_m.paragraphs[0].runs[0].font.name = "Agency FB"
    texto_m.paragraphs[0].runs[0].font.bold = True

    #crando titulo de direccion de despacho
    forma = diapositiva1.shapes[0]

    posicion_x = forma.left
    posicion_y = forma.top
    ancho = forma.width
    alto = forma.height

    eliminar_objeto(forma)

    contenedor = diapositiva1.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
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
    forma2 = diapositiva1.shapes[0]
    posicion_x = forma2.left
    posicion_y = forma2.top
    ancho = forma2.width
    alto = forma2.height

    eliminar_objeto(forma2)

    contenedor_text = diapositiva1.shapes.add_textbox(posicion_x, posicion_y, ancho, alto)
    texto_m = contenedor_text.text_frame

    texto_m.text = f"Directora: {directora}"
    texto_m.paragraphs[0].alignment = PP_ALIGN.CENTER
    texto_m.vertical_anchor = MSO_ANCHOR.MIDDLE

    texto_m.paragraphs[0].runs[0].font.size = Pt(14)
    texto_m.paragraphs[0].runs[0].font.name = "Arial"
    texto_m.paragraphs[0].runs[0].font.bold = True

