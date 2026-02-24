from models.conexion_db import ConexionDB
from datetime import datetime, timedelta
from typing import Dict

class Modelo_estadistica():
    def __init__(self):
        self.db = ConexionDB()

    def obtener_todas_actividades(self):
        conexion = ConexionDB()
        sql = "SELECT id_Actividad, fecha FROM Actividad;"
        conexion.cursor.execute(sql)
        filas = conexion.cursor.fetchall()
        conexion.Cerrar()

        actividades = []
        for fila in filas:
            try:
                id_actividad, fecha_str = fila
            except Exception:
                continue

            fecha_dt = None
            if fecha_str:
                for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"):
                    try:
                        fecha_dt = datetime.strptime(fecha_str, fmt)
                        break
                    except Exception:
                        continue

            if fecha_dt:
                actividades.append({"id": id_actividad, "fecha": fecha_dt})

        return actividades

    def contar_actividades_ultimos_dias(self, dias: int) -> int:
        actividades = self.obtener_todas_actividades()
        ahora = datetime.now()
        limite = ahora - timedelta(days=dias)
        contador = sum(1 for a in actividades if a["fecha"] >= limite)
        return contador

    def obtener_contadores_periodos(self) -> dict:
        return {
            "semanal": self.contar_actividades_ultimos_dias(7),
            "mensual": self.contar_actividades_ultimos_dias(30),
            "trimestral": self.contar_actividades_ultimos_dias(90),
            "anual": self.contar_actividades_ultimos_dias(365),
        }
    
    def cargar_datos_objetivos(self) -> Dict[str, str]:
        try:
            cursor = self.db.conexion.cursor()
            cursor.execute("""
                SELECT objetivo_semanal, objetivo_mensual, 
                       objetivo_trimestral, objetivo_anual 
                FROM Objetivos_Reportes WHERE id_objetivo = 1
            """)
            datos = cursor.fetchone()
            
            if datos and any(datos):
                return {
                    "objetivo_semanal": str(datos[0]) if datos[0] is not None else "8",
                    "objetivo_mensual": str(datos[1]) if datos[1] is not None else "20",
                    "objetivo_trimestral": str(datos[2]) if datos[2] is not None else "30",
                    "objetivo_anual": str(datos[3]) if datos[3] is not None else "120"
                }
            else:
                return {
                    "objetivo_semanal": "8",
                    "objetivo_mensual": "20", 
                    "objetivo_trimestral": "30",
                    "objetivo_anual": "120"
                }
        except Exception as e:
            print(f"❌ Error al cargar objetivos: {e}")
            return {
                "objetivo_semanal": "8",
                "objetivo_mensual": "20",
                "objetivo_trimestral": "30",
                "objetivo_anual": "120"
            }