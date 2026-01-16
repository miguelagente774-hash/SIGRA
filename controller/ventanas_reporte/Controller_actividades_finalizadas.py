from view.ventanas_reporte.vista_actividades_finalizadas import Ventana_reporte_finalizados
from models.models_reportes.Model_actividad_finalizadas import Modelo_actividades_finalizadas
from controller.ventanas_reporte.c_modal_actulizar_actividad import Controller_modal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt  # Añadir esta importación
from comunicador import Comunicador_global
import os
from pathlib import Path

class controlador_reporte_finalizados():
    def __init__(self):
        self.Controller_modal = Controller_modal()
        self.modelo = Modelo_actividades_finalizadas()
        self.actividades_finalizadas = Ventana_reporte_finalizados(self)
        Comunicador_global.actividad_agregada.connect(self.actualizar_tabla)

        # Conectar señales de la vista al controlador
        self.actividades_finalizadas.modificar_actividad.connect(self.Abrir_modal)
        self.actividades_finalizadas.eliminar_actividad.connect(self.Eliminar_actividad_signal_handler)  # Cambiado

    # Función para que se muestre la vista en el programa
    def get_widget(self):
        return self.actividades_finalizadas
    
    # Funciones del programa
    def Obtener_datos_tabla(self):
        try:
            datos = self.modelo.Obtener_datos()
            return datos
        except Exception as e:
            self.actividades_finalizadas.Mensaje_error("error", f"{e}")

    def actualizar_tabla(self):
        datos_nuevo = self.Obtener_datos_tabla()
        # Limpiar tabla
        self.actividades_finalizadas.tabla_actividades.setRowCount(0)

        self.actividades_finalizadas.tabla_actividades.setRowCount(len(datos_nuevo))
        # Insertamos los nuevos datos
        for indice_fila, fila_datos in enumerate(datos_nuevo):
            # Obteniendo columna y los valores
            for indice_columna, valores in enumerate(fila_datos):
                # Volviendo todos los valores en string
                item = QTableWidgetItem(str(valores))
                item.setTextAlignment(Qt.AlignCenter)
                # Insertando los datos en sus posiciones correspondiente
                self.actividades_finalizadas.tabla_actividades.setItem(indice_fila, indice_columna, item)

    def Obtener_indice_tabla(self):
        fila_seleccionada = self.actividades_finalizadas.tabla_actividades.currentRow()
        
        if fila_seleccionada >= 0:
            item = self.actividades_finalizadas.tabla_actividades.item(fila_seleccionada, 0)
            if item:  # Verificar que el item no sea None
                id_actividad = item.text()
                return id_actividad
        return None
    
    def Limpiar_seleccion_fila(self):
        # Deseleccionar fila en la tabla
        self.actividades_finalizadas.tabla_actividades.clearSelection()

    # Handler para la señal de eliminar actividad
    def Eliminar_actividad_signal_handler(self):
        """Manejador de la señal de eliminar actividad (sin parámetros)"""
        id_actividad = self.Obtener_indice_tabla()
        if id_actividad:
            # Preguntar confirmación antes de eliminar
            from PyQt5.QtWidgets import QMessageBox
            respuesta = QMessageBox.question(
                self.actividades_finalizadas,
                "Confirmar eliminación",
                f"¿Está seguro de eliminar la actividad con ID {id_actividad}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                self.Eliminar_actividad(id_actividad)
        else:
            self.actividades_finalizadas.Mensaje_Warning("Advertencia", "Por favor seleccione una actividad")

    # ==Método principal para eliminar actividad==
    def Eliminar_actividad(self, id_actividad):
            # Elimina una actividad por su ID
            if not id_actividad:
                self.actividades_finalizadas.Mensaje_Warning("Advertencia", "Por favor seleccione una fila")
                return
            
            try:
                # Intentar eliminar imágenes (opcional, no crítico)
                try:
                    imagenes = self.modelo.Obtener_url_imagenes(id_actividad)
                    if imagenes:
                        for ruta_lista in imagenes:
                            if isinstance(ruta_lista, (list, tuple)):
                                for ruta in ruta_lista:
                                    if ruta and os.path.exists(ruta):
                                        os.remove(ruta)
                except:
                    pass  # Ignorar errores al eliminar imágenes
                
                # Eliminar de la base de datos
                self.modelo.Eliminar_datos(id_actividad)
                
                # Siempre mostrar éxito si no hay excepción
                self.actividades_finalizadas.Mensaje_info("Éxito", "Actividad eliminada correctamente")
                self.actualizar_tabla()
                Comunicador_global.actividad_agregada.emit()
                
            except Exception as e:
                # Verificar si el error es porque ya no existe
                try:
                    # Intentar obtener los datos para ver si aún existe
                    existe = self.modelo.Obtener_datos_actividad(id_actividad)
                    if not existe:
                        # Si no existe, significa que fue eliminada exitosamente
                        self.actividades_finalizadas.Mensaje_informativo("Éxito", "Actividad eliminada")
                        self.actualizar_tabla()
                        Comunicador_global.actividad_agregada.emit()
                    else:
                        self.actividades_finalizadas.Mensaje_error("Error", f"No se pudo eliminar: {str(e)}")
                except:
                    self.actividades_finalizadas.Mensaje_error("Error", f"Error: {str(e)}")

    # Método para abrir modal de modificación
    def Abrir_modal(self):
        """Abre el modal para modificar una actividad"""
        id_actividad = None
        datos = None
        
        try:
            id_actividad = self.Obtener_indice_tabla()
        except Exception as e:
            self.actividades_finalizadas.Mensaje_Warning("Advertencia", f"Error al cargar el índice: {str(e)}")

        if id_actividad:
            try:
                datos = self.modelo.Obtener_datos_actividad(id_actividad)
            except Exception as e:
                self.actividades_finalizadas.Mensaje_error("Error", f"Error al obtener datos: {str(e)}")
                
            if datos:
                try:
                    self.Controller_modal.Abrir_modal(datos)
                    self.Limpiar_seleccion_fila()
                except Exception as e:
                    self.actividades_finalizadas.Mensaje_error("Error", f"No se pudo abrir la ventana: {str(e)}")
            else:
                self.actividades_finalizadas.Mensaje_Warning("Advertencia", "No se encontraron datos de la actividad")
        else:
            self.actividades_finalizadas.Mensaje_Warning("Advertencia", "Por favor seleccione una actividad")