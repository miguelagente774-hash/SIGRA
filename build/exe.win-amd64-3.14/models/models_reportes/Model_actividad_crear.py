import sqlite3 as sql
from models.conexion_db import ConexionDB

class Actividad:
    def __init__(self, titulo, imagen1, imagen2, descripcion, fecha, tipo_actividad):
        self.titulo = titulo
        self.imagen1 = imagen1
        self.imagen2 = imagen2
        self.descripcion = descripcion
        self.fecha = fecha
        self.tipo_actividad = tipo_actividad


    def Validar_datos(self):
        if not self.titulo or str(self.titulo).strip() == "":
            mensaje = "Por favor inserte el titulo"
            return mensaje
        
        elif not self.imagen1 or str(self.imagen1).strip() == "":
            mensaje = "Por favor inserte la imagen 1"
            return mensaje
        
        elif not self.imagen2 or str(self.imagen2).strip() == "":
            mensaje = "Por favor inserte la imagen 2"
            return mensaje
        
        elif not self.descripcion or str(self.descripcion).strip() == "":
            mensaje = "Por favor inserte la descripcion"
            return mensaje
        
        else:
            return None


class Guardar_actividad:
    def __init__(self):
        self.db = ConexionDB()


    def Guardar_datos(self, actividad):
        conexion = self.db
        sql = f'''
        INSERT INTO Actividad (titulo, descripcion, ruta1, ruta2, fecha, tipo_Actividad)
        VALUES ('{actividad.titulo}', '{actividad.descripcion}', '{actividad.imagen1}', '{actividad.imagen2}', '{actividad.fecha}', '{actividad.tipo_actividad}')
        '''
        conexion.cursor.execute(sql)
        conexion.Cerrar()