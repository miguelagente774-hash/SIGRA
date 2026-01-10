from models.conexion_db import ConexionDB

class Modelo_consulta():
    def __init__(self):
        pass

    def Obtener_reportes(self):
        Conexion = ConexionDB()
        sql = """
        SELECT * FROM Reporte;
        """
        Conexion.cursor.execute(sql)
        reportes = Conexion.cursor.fetchall()
        Conexion.Cerrar()

        return reportes

    def Obtener_jefe(self):
        Conexion = ConexionDB()
        sql = """SELECT nombres, apellidos FROM Gobernacion"""
        
        Conexion.cursor.execute(sql)
        datos_jefe = Conexion.cursor.fetchall()
        Conexion.Cerrar()

        return datos_jefe
    
    def Obtener_coordinador(self):
        Conexion = ConexionDB()
        sql1 = "PRAGMA foreign_keys = ON"
        Conexion.cursor.execute(sql1)

        sql = """SELECT nombres, apellidos, Gaceta.decreto, Gaceta.fecha_publicacion
                FROM Coordinacion
                INNER JOIN Gaceta ON Coordinacion.id_coordinador = Gaceta.id_coordinador"""
        
        Conexion.cursor.execute(sql)
        datos_coordinador = Conexion.cursor.fetchall()
        Conexion.Cerrar()

        return datos_coordinador


    def Obtener_actividades(self, id_reporte):
        Conexion = ConexionDB()
        sql = f"""SELECT 
        reporte_actividades.actividad_id, 
		Actividad.titulo, 
		Actividad.descripcion, 
		Actividad.ruta1, 
		Actividad.ruta2, 
		Actividad.fecha, 
		Actividad.tipo_Actividad
        FROM reporte_actividades
        INNER JOIN Actividad ON reporte_actividades.actividad_id = Actividad.id_Actividad
        WHERE reporte_id = {id_reporte};"""
        
        Conexion.cursor.execute(sql)
        Actividades = Conexion.cursor.fetchall()
        Conexion.Cerrar()

        return Actividades

    def Eliminar_reporte(self, id_reporte):
        Conexion = ConexionDB()
        #actividando las claves foraneas (necesario en python)
        sql1 = "PRAGMA foreign_keys = ON"
        Conexion.cursor.execute(sql1)
        #eliminado el reporte en Cascada todos sus datos relacionados se eliminaran tambien
        sql = f"""
        DELETE FROM Reporte WHERE id_reporte = ?;
        """
        Conexion.cursor.execute(sql, id_reporte)
        Conexion.Cerrar()