from models.conexion_db import ConexionDB

class Modelo_reporte():
    def __init__(self):
        pass
    
    def Obtener_actividades(self):
        conexion = ConexionDB()
        sql = """
        SELECT id_Actividad, titulo, fecha FROM Actividad"""
        conexion.cursor.execute(sql)
        datos = conexion.cursor.fetchall()
        conexion.Cerrar()
        return datos

    def Guardar_datos_reporte(self, nombre_reporte, actividades_ids):
        """Guarda un reporte con las actividades seleccionadas"""
        try:
            conexion = ConexionDB()
            
            # 1. Crear el reporte
            sql_reporte = """
            INSERT INTO Reporte (titulo) VALUES (?)
            """
            conexion.cursor.execute(sql_reporte, (nombre_reporte,))
            
            # 2. Obtener el ID del reporte recién creado
            reporte_id = conexion.cursor.lastrowid
            
            # 3. Insertar cada actividad seleccionada en la tabla intermedia
            sql_actividades = """
            INSERT INTO reporte_actividades (reporte_id, actividad_id, orden) 
            VALUES (?, ?, ?)
            """
            
            for orden, actividad_id in enumerate(actividades_ids, start=1):
                conexion.cursor.execute(sql_actividades, (reporte_id, actividad_id, orden))
            
            conexion.conexion.commit()
            conexion.Cerrar()
            
            return True, f"Reporte '{nombre_reporte}' creado con {len(actividades_ids)} actividades"
            
        except Exception as e:
            return False, f"Error al guardar reporte: {str(e)}"
