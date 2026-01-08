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

    def Obtener_actividades(self):
        pass

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