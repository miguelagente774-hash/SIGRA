# controller/ventanas_reporte/Controller_actividad_crear.py

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
from view.ventanas_reporte.vista_actividad_crear import Ventana_actividad_crear
from models.conexion_db import ConexionDB
from comunicador import Comunicador_global
import os

class controlador_reporte_crear(QObject):
    # Señal para cuando se crea una actividad
    actividad_creada = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.db = ConexionDB()
        self.vista = None
        
    def get_widget(self):
        if not self.vista:
            self.vista = Ventana_actividad_crear(self)
        return self.vista
    
    def guardar_actividad(self, titulo, descripcion, tipo_actividad, 
                          fecha, ruta_imagen1, ruta_imagen2):
        """Guarda una nueva actividad en la base de datos"""
        
        # Validar campos obligatorios
        if not titulo or not titulo.strip():
            self.vista.mensaje_error("Error", "El título es obligatorio")
            return False
            
        if not tipo_actividad:
            self.vista.mensaje_error("Error", "El tipo de actividad es obligatorio")
            return False
            
        if not fecha:
            self.vista.mensaje_error("Error", "La fecha es obligatoria")
            return False
        
        try:
            cursor = self.db.conexion.cursor()
            
            # Insertar actividad en la tabla Actividad
            sql = """
                INSERT INTO Actividad 
                (titulo, descripcion, ruta1, ruta2, fecha, tipo_Actividad) 
                VALUES (?, ?, ?, ?, ?, ?)
            """
            
            valores = (
                titulo.strip(),
                descripcion.strip() if descripcion else "",
                ruta_imagen1 if ruta_imagen1 else "",
                ruta_imagen2 if ruta_imagen2 else "",
                fecha,
                tipo_actividad
            )
            
            cursor.execute(sql, valores)
            self.db.conexion.commit()
            
            # ✅ EMITIR SEÑAL POR EL COMUNICADOR GLOBAL
            Comunicador_global.actividad_agregada.emit()
            print("✅ Actividad guardada y señal emitida")
            
            self.vista.mensaje_informativo("Éxito", "Actividad guardada correctamente")
            
            # Limpiar formulario
            self.vista.limpiar_campos()
            return True
                
        except Exception as e:
            print(f"❌ Error al guardar actividad: {e}")
            self.vista.mensaje_error("Error", f"Error al guardar: {str(e)}")
            return False
    
    def obtener_tipos_actividad(self):
        """Obtiene los tipos de actividad disponibles"""
        try:
            cursor = self.db.conexion.cursor()
            cursor.execute("SELECT DISTINCT tipo_Actividad FROM Actividad")
            resultados = cursor.fetchall()
            
            # Si hay resultados, devolver lista de tipos
            if resultados:
                return [r[0] for r in resultados if r[0]]
            else:
                # Valores por defecto
                return ["Actividad Regular", "Actividad Especial", "Capacitación", "Reunión"]
                
        except Exception as e:
            print(f"❌ Error al obtener tipos: {e}")
            return ["Actividad Regular", "Actividad Especial", "Capacitación", "Reunión"]
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if hasattr(self, 'db'):
            self.db.Cerrar()