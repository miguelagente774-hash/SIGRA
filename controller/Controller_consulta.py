from view.vista_consulta import Ventana_consulta
from models.Modelo_consulta import Modelo_consulta
from comunicador import Comunicador_global
from components.modal_reporte import Modal_exportar_Reporte
from PyQt5.QtWidgets import QDialog, QFileDialog
import tempfile
import shutil
import os
from services.pptx.convert import pptx_to_pdf
from datetime import datetime
from services.pptx.reporte import Reporte
from pathlib import Path

class controlador_consulta():
    def __init__(self):
        
        self.modelo = Modelo_consulta()

    def get_widget(self):
        self.consulta = Ventana_consulta(self)
        Comunicador_global.Reporte_agregado.connect(self.consulta.actulizar_tabla)
        return self.consulta
    
    def Obtener_reportes(self):
        try:
            reportes = self.modelo.Obtener_reportes()
            return reportes
        except:
            self.consulta.mensaje_error("Error", "Error al Obtener Reporte")

    def abrir_modal(self, Nombre_reporte):
        try:
            modal = Modal_exportar_Reporte(Nombre_reporte, self)
            if modal.exec_() == QDialog.Accepted:
                self.datos_meses = modal.obtener_lista_simple()
                #Obtener ruta de donde guardar el archivo
                directorio = QFileDialog.getExistingDirectory(None, "Selecciona la carpeta de destino")
                if directorio:
                # Uniendo ruta con el nombre del archivo
                    ruta_final = Path(directorio) / Nombre_reporte
                
                #exportanto reporte
                self.Crear_Reporte(self.datos_meses, ruta_final)
        except Exception as e:
            self.consulta.mensaje_error("Error", f"Error al cargar ventana: {e}")

    #------------------------------ creacion reporte --------------------------
    def Crear_Reporte(self, datos_meses, ruta_final):
        try:
            datos_reporte = self.consulta.Obtener_reporte_seleccionado()
            id_reporte = datos_reporte[0]
            nombre_reporte = ruta_final
        except Exception as e:
            self.consulta.mensaje_error("Error", f"datos_reporte: {e}")

        try: 
            nombre_dir = self.Obtener_jefe()
        except Exception as e:
            self.consulta.mensaje_error("Error", f"nombre_dir: {e}")

        try:
            fecha, listas_meses, listas_ponderaciones = self.Obtener_fechas_porcentajes(datos_meses)
        except Exception as e:
            self.consulta.mensaje_error("Error", f"fechas: {e}")

        try:
            datos_actividades = self.Obtener_actividades(id_reporte) 
        except Exception as e:
            self.consulta.mensaje_error("Error", f"actividades: {e}")

        try:
            datos_coordinador = self.Obtener_coodinador()
        except Exception as e:
            self.consulta.mensaje_error("Error", f"datos_coordinador: {e}")

        try:
            direccion = self.Obtener_direccion()
        except Exception as e:
            self.consulta.mensaje_error("Error", f"datos_direccion: {e}")

        #funcion para hacer reporte
        try:
            Reporte(nombre_reporte, nombre_dir, fecha, listas_meses, listas_ponderaciones, datos_actividades, datos_coordinador, direccion)
            self.consulta.mensaje_informativo("Informacion", "Reporte Guardado Exitosamente")
        except Exception as e:
            self.consulta.mensaje_error("Error", f"{e}")

    def abrir_modal_pdf(self, Nombre_reporte):
        """Abre el modal de selección de meses y luego pregunta dónde guardar el PDF.
        Genera un PPTX temporal, lo convierte a PDF en la ruta seleccionada y elimina temporales.
        """
        try:
            modal = Modal_exportar_Reporte(Nombre_reporte, self)
            if modal.exec_() == QDialog.Accepted:
                datos_meses = modal.obtener_lista_simple()

                # Obtener ruta de destino del PDF
                ruta_pdf, _ = QFileDialog.getSaveFileName(None, "Guardar PDF como", f"{Nombre_reporte}.pdf", "PDF Files (*.pdf)")
                if not ruta_pdf:
                    return

                # Crear carpeta temporal para generar PPTX
                tmp_dir = tempfile.mkdtemp()
                try:
                    base_tmp = Path(tmp_dir) / Nombre_reporte

                    # Crear el PPTX en tmp usando misma lógica que Crear_Reporte
                    try:
                        datos_reporte = self.consulta.Obtener_reporte_seleccionado()
                        id_reporte = datos_reporte[0]
                    except Exception as e:
                        self.consulta.mensaje_error("Error", f"datos_reporte: {e}")

                    try:
                        nombre_dir = self.Obtener_jefe()
                    except Exception as e:
                        self.consulta.mensaje_error("Error", f"nombre_dir: {e}")

                    try:
                        fecha, listas_meses, listas_ponderaciones = self.Obtener_fechas_porcentajes(datos_meses)
                    except Exception as e:
                        self.consulta.mensaje_error("Error", f"fechas: {e}")

                    try:
                        datos_actividades = self.Obtener_actividades(id_reporte)
                    except Exception as e:
                        self.consulta.mensaje_error("Error", f"actividades: {e}")

                    try:
                        datos_coordinador = self.Obtener_coodinador()
                    except Exception as e:
                        self.consulta.mensaje_error("Error", f"datos_coordinador: {e}")

                    try:
                        direccion = self.Obtener_direccion()
                    except Exception as e:
                        self.consulta.mensaje_error("Error", f"datos_direccion: {e}")

                    # Generar PPTX temporal
                    try:
                        # Reporte guarda como: <base> <año>.pptx
                        Reporte(str(base_tmp), nombre_dir, fecha, listas_meses, listas_ponderaciones, datos_actividades, datos_coordinador, direccion)
                        pptx_path = Path(f"{base_tmp} {fecha['año']}.pptx")
                        if not pptx_path.exists():
                            raise RuntimeError(f"No se encontró PPTX generado: {pptx_path}")
                    except Exception as e:
                        self.consulta.mensaje_error("Error", f"Error al generar PPTX: {e}")
                        return

                    # Convertir a PDF
                    try:
                        pptx_to_pdf(str(pptx_path), ruta_pdf)
                    except FileNotFoundError as e:
                        self.consulta.mensaje_advertencia("Advertencia", f"Archivo PPTX temporal no encontrado: {e}")
                        return
                    except Exception as e:
                        msg = str(e)
                        # Mensajes amigables según la causa
                        if 'soffice no encontrado' in msg or 'soffice no encontrado en PATH' in msg or 'soffice' in msg:
                            self.consulta.mensaje_advertencia(
                                "Advertencia",
                                "No se encontró LibreOffice (soffice).\n\nPara usar la conversión a PDF instala LibreOffice o asegúrate de que Microsoft PowerPoint esté instalado junto con pywin32/comtypes."
                            )
                        elif 'pywin32/PowerPoint' in msg or 'comtypes/PowerPoint' in msg or 'PowerPoint' in msg:
                            self.consulta.mensaje_advertencia(
                                "Advertencia",
                                "No se pudo usar PowerPoint vía COM.\n\nAsegúrate de tener Microsoft PowerPoint instalado y las librerías Python necesarias:\n`pip install pywin32 comtypes`\ny luego ejecuta `python -m pywin32_postinstall -install`"
                            )
                        else:
                            self.consulta.mensaje_error("Error", f"Error al convertir a PDF: {msg}")
                        return

                    # Informar y limpiar
                    self.consulta.mensaje_informativo("Informacion", "PDF generado correctamente")

                finally:
                    # eliminar carpeta temporal
                    try:
                        shutil.rmtree(tmp_dir)
                    except Exception:
                        pass
        except Exception as e:
            self.consulta.mensaje_error("Error", f"Error al cargar ventana: {e}")

    
    def Obtener_jefe(self):
        try:
            nombre = self.modelo.Obtener_jefe()
            datos_jefe = nombre[0]
            nombre_jefe = datos_jefe[0]
            apellido_jefe = datos_jefe[1]
            nombre_completo = f"{nombre_jefe} {apellido_jefe}"
        except:
            self.consulta.mensaje_error("Error", "Error al Obtener datos de de dir")

        return nombre_completo

    def Obtener_coodinador(self):
        try:
            datos_cor = self.modelo.Obtener_coordinador()
            datos = datos_cor[0]
        except:
            self.consulta.mensaje_error("Error", "Error al Obtener datos_coordinador")
        
        if datos != None:
            nombre_Apellido = f"{datos[0]} {datos[1]}"
            decreto = datos[2]
            f_publicacion = datos[3]

            datos_coordinador = {"nombre_apellido": nombre_Apellido, 
                                "decreto": decreto, 
                                "fecha_publicacion": f_publicacion
                            }
        else:
            self.consulta.mensaje_error("Error", "datos vacios")
        
        return datos_coordinador

    def Obtener_actividades(self, id_reporte):
        #actividades
        try:
            actividades = self.modelo.Obtener_actividades(id_reporte)
        except:
            self.consulta.mensaje_error("Error", "Error al Obtener actividades")    
        actividades_enviar = []
        
        if actividades != None:
            for datos in actividades:    
                datos_actividades = {
                    "titulo": datos[1],
                    "descripcion": datos[2],
                    "imagen1": datos[3],
                    "imagen2": datos[4],
                    "fecha": datos[5],
                    "tipo_actividad": datos[6]
                }
                actividades_enviar.append(datos_actividades)
        else:
            self.consulta.mensaje_error("Error", "datos de actividades vacios")
        
        return actividades_enviar
    
    def Obtener_fechas_porcentajes(self, datos_meses):
        #separando informacion de los meses    
        mes_1, mes_2, mes_3, porcentaje = datos_meses
        
        año = datetime.now().strftime("%Y")

        listas_meses = [mes_1["mes"], mes_2["mes"], mes_3["mes"]]
        listas_ponderaciones = [mes_1["valores"], mes_2["valores"], mes_3["valores"]]
        
        fecha = {
            "mes1": f"{listas_meses[0]}",
            "mes2": f"{listas_meses[1]}",
            "mes3": f"{listas_meses[2]}",
            "año": año,
            'porcentaje': porcentaje
        }

        return fecha, listas_meses, listas_ponderaciones
    
    def Obtener_direccion(self):
        Direccion_list = self.modelo.Obtener_direccion()
        Direccion = Direccion_list[0]
        dic_direccion = {
            'municipio': f'{Direccion[0]}',
            'parroquia': f'{Direccion[1]}',
            'instituto': f'{Direccion[2]}'
        }

        return dic_direccion

    def Eliminar_reporte(self, id_reporte):
        if id_reporte != None:
            try:
                self.modelo.Eliminar_reporte(id_reporte)
                self.consulta.mensaje_informativo("Informacion", f"Reporte Nro {id_reporte} Eliminado ")
                self.consulta.actulizar_tabla()
            except Exception as e:
                self.consulta.mensaje_error("Error", f"Error al Eliminar Reporte: {e}")
        else:
            self.consulta.mensaje_advertencia("Advertencia", "Por favor seleccione un Reporte")