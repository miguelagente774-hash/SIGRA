from models.conexion_db import ConexionDB
from datetime import datetime, timedelta


class Modelo_estadistica():
    """Modelo para obtener estadísticas de actividades.

    Las fechas de las actividades se guardan como texto en formato
    'dd-MM-yyyy' (según la UI). Este modelo carga las fechas,
    las parsea y cuenta actividades en rangos de días.
    """
    def __init__(self):
        pass

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
        """Devuelve contadores para: semanal, mensual, trimestral, anual."""
        return {
            "semanal": self.contar_actividades_ultimos_dias(7),
            "mensual": self.contar_actividades_ultimos_dias(30),
            "trimestral": self.contar_actividades_ultimos_dias(90),
            "anual": self.contar_actividades_ultimos_dias(365),
        }