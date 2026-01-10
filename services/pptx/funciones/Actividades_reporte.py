from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def Actividad_reporte(pptx, imagen1, imagen2, descripcion):

    diapositiva1 = pptx.slides.add_slide(pptx.slide_layouts[0])

    imagen = diapositiva1.shapes[0]
    posionleft = imagen.left
    posiontop = imagen.top
    width = imagen.width
    heigth = imagen.height

    contenedor_v = imagen._element
    contenedor_v.getparent().remove(contenedor_v)

    diapositiva1.shapes.add_picture(imagen1, posionleft, posiontop, width, heigth)

    imagen = diapositiva1.shapes[0]
    dposionleft = imagen.left
    dposiontop = imagen.top
    dwidth = imagen.width
    dheigth = imagen.height

    contenedor_v2 = imagen._element
    contenedor_v2.getparent().remove(contenedor_v2)

    diapositiva1.shapes.add_picture(imagen2, dposionleft, dposiontop, dwidth, dheigth)

    texto = diapositiva1.shapes[0]
    tposionleft = texto.left
    tposiontop = texto.top
    twidth = texto.width
    theigth = texto.height

    #eliminado el texto
    texto_v = texto._element
    texto_v.getparent().remove(texto_v)

    #creando contenedor del texto
    contenedor_text = diapositiva1.shapes.add_textbox(tposionleft, tposiontop, twidth, theigth)
    texto = contenedor_text.text_frame #modificando el contenedor ya creado

    texto.text = descripcion #texto a mostrar

    texto.paragraphs[0].runs[0].font.name = "Arial"
    texto.paragraphs[0].runs[0].font.size = Pt(12) #controla el tamano de la letra
    texto.paragraphs[0].runs[0].font.bold = False # le da formato negrita
    texto.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0) #controla el color de fuente
    texto.paragraphs[0].alignment = PP_ALIGN.CENTER #alinea al centro el texto
    texto.vertical_anchor = MSO_ANCHOR.MIDDLE #alinea verticalmente el texto



