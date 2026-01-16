from models.conexion_db import ConexionDB

class Modelo_actualizar():
    def Actualizar_actividad(self, id_actividad, titulo, descripcion, ruta1, ruta2, fecha):
        conexion = ConexionDB()

        sql = """UPDATE Actividad
        SET titulo = ?, descripcion = ?, ruta1 = ?, ruta2 = ?, fecha = ?
        WHERE id_Actividad = ?;
        """
        
        conexion.cursor.execute(sql, (titulo, descripcion, ruta1, ruta2, fecha, id_actividad))
        conexion.conexion.commit()  
        conexion.Cerrar()