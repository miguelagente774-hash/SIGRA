from models.conexion_db import ConexionDB

class Modelo_actualizar():
    
    def Actulizar_actividad(self, id_actividad, titulo, descripcion, ruta1, ruta2, fecha):
        conexion = ConexionDB()
        sql = f"""UPDATE Actividad
        SET titulo = '{titulo}', descripcion = '{descripcion}', ruta1 = '{ruta1}', ruta2 = '{ruta2}', fecha = '{fecha}'
        WHERE id_Actividad = {id_actividad};
        """
        conexion.cursor.execute(sql)
        conexion.Cerrar()