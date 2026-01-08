from models.conexion_db import ConexionDB

class Modelo_actividades_finalizadas():            

        def Obtener_datos(self):
                conexion = ConexionDB()
                sql = """
                SELECT id_actividad, titulo, descripcion, fecha
                FROM Actividad
                ORDER BY id_actividad ASC;
                """
                conexion.cursor.execute(sql)
                datos = conexion.cursor.fetchall()
                conexion.Cerrar()

                return datos

        def Obtener_datos_actividad(self, id_actividad):
                conexion = ConexionDB()
                sql = f"""SELECT * FROM Actividad WHERE id_Actividad = {id_actividad};"""
                conexion.cursor.execute(sql)
                datos = conexion.cursor.fetchall()
                conexion.Cerrar()

                return datos
        
        def Obtener_url_imagenes(self, id_actividad):
                conexion = ConexionDB()
                sql = f"""SELECT ruta1, ruta2 FROM Actividad WHERE id_Actividad = {id_actividad};"""
                conexion.cursor.execute(sql)
                imagenes = conexion.cursor.fetchall()
                conexion.Cerrar()

                return imagenes

        def Eliminar_datos(self, id_Actividad):
                conexion = ConexionDB()
                sql = f"""DELETE FROM Actividad
                        WHERE id_Actividad = {id_Actividad}"""
                conexion.cursor.execute(sql)
                conexion.Cerrar()