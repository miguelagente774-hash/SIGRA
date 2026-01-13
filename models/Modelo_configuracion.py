import hashlib
from typing import Optional, Tuple, Dict, Any
from .conexion_db import ConexionDB

class Model_Configuraciones:
    def __init__(self):
        self.db = ConexionDB()
    
    # ========== MÉTODOS PARA CONFIGURACIÓN DE INTERFAZ ==========
    
    def guardar_configuracion_interfaz(self, tema: str, fuente: str, tamaño: int, negrita: bool) -> bool:
        """Guarda la configuración de interfaz en la base de datos"""
        try:
            conn = self.db.conexion
            cursor = conn.cursor()
            
            # Guardar tema
            cursor.execute("INSERT OR REPLACE INTO Tema (id_tema, tema) VALUES (1, ?)", (tema,))
            
            # Guardar fuente
            cursor.execute("""
                INSERT OR REPLACE INTO Fuente (id_fuente, tamano, famila, font) 
                VALUES (1, ?, ?, ?)
            """, (tamaño, fuente, "bold" if negrita else "normal"))
            
            # Crear o actualizar configuración
            cursor.execute("""
                INSERT OR REPLACE INTO Configuracion 
                (id_configuracion, id_tema, id_fuente) 
                VALUES (1, 1, 1)
            """)
            
            conn.commit()
            print("✅ Configuración de interfaz guardada")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar interfaz: {e}")
            return False
    
    def cargar_configuracion_interfaz(self) -> Dict[str, Any]:
        """Carga la configuración de interfaz desde la BD"""
        try:
            cursor = self.db.conexion.cursor()
            
            cursor.execute("SELECT tema FROM Tema WHERE id_tema = 1")
            tema = cursor.fetchone()
            
            cursor.execute("SELECT tamano, famila, font FROM Fuente WHERE id_fuente = 1")
            fuente = cursor.fetchone()
            
            return {
                "tema": tema[0] if tema else "Claro",
                "fuente": fuente[1] if fuente else "Arial",
                "tamaño": fuente[0] if fuente else 12,
                "negrita": fuente[2] == "bold" if fuente else False
            }
            
        except Exception as e:
            print(f"❌ Error al cargar interfaz: {e}")
            return {"tema": "Claro", "fuente": "Arial", "tamaño": 12, "negrita": False}
    
    # ========== MÉTODOS PARA DATOS DE DIRECCIÓN ==========
    
    def guardar_datos_direccion(self, estado: str, municipio: str, parroquia: str, institucion: str) -> bool:
        """Guarda los datos de dirección en la BD"""
        try:
            cursor = self.db.conexion.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO Direccion 
                (id_comunidad, estado, municipio, parroquia, instituto) 
                VALUES (1, ?, ?, ?, ?)
            """, (estado, municipio, parroquia, institucion))
            
            self.db.conexion.commit()
            print("✅ Datos de dirección guardados")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar dirección: {e}")
            return False
    
    def cargar_datos_direccion(self) -> Dict[str, str]:
        """Carga los datos de dirección desde la BD"""
        try:
            cursor = self.db.conexion.cursor()
            
            cursor.execute("""
                SELECT estado, municipio, parroquia, instituto 
                FROM Direccion WHERE id_comunidad = 1
            """)
            datos = cursor.fetchone()
            
            if datos:
                return {
                    "estado": datos[0],
                    "municipio": datos[1],
                    "parroquia": datos[2],
                    "institucion": datos[3]
                }
            return {"estado": "", "municipio": "", "parroquia": "", "institucion": ""}
            
        except Exception as e:
            print(f"❌ Error al cargar dirección: {e}")
            return {"estado": "", "municipio": "", "parroquia": "", "institucion": ""}
    
    # ========== MÉTODOS PARA DATOS DE JEFATURAS ==========
    
    def guardar_datos_jefaturas(self, 
                               nombre_coordinacion: str, 
                               cedula_coordinacion: str,
                               nombre_gobernacion: str, 
                               cedula_gobernacion: str) -> bool:
        """Guarda los datos de jefaturas en la BD"""
        try:
            conn = self.db.conexion
            cursor = conn.cursor()
            
            # Guardar coordinación
            cursor.execute("""
                INSERT OR REPLACE INTO Coordinacion 
                (id_coordinador, nombres, apellidos) 
                VALUES (1, ?, ?)
            """, (nombre_coordinacion.split()[0], " ".join(nombre_coordinacion.split()[1:])))
            
            # Guardar gobernación
            cursor.execute("""
                INSERT OR REPLACE INTO Gobernacion 
                (id_jefe, nombres, apellidos) 
                VALUES (1, ?, ?)
            """, (nombre_gobernacion.split()[0], " ".join(nombre_gobernacion.split()[1:])))
            
            # Actualizar configuración
            cursor.execute("""
                UPDATE Configuracion 
                SET id_coordinacion = 1, id_gobernacion = 1 
                WHERE id_configuracion = 1
            """)
            
            conn.commit()
            print("✅ Datos de jefaturas guardados")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar jefaturas: {e}")
            return False
    
    def cargar_datos_jefaturas(self) -> Dict[str, str]:
        """Carga los datos de jefaturas desde la BD"""
        try:
            cursor = self.db.conexion.cursor()
            
            cursor.execute("""
                SELECT nombres, apellidos FROM Coordinacion WHERE id_coordinador = 1
            """)
            coord = cursor.fetchone()
            
            cursor.execute("""
                SELECT nombres, apellidos FROM Gobernacion WHERE id_jefe = 1
            """)
            gob = cursor.fetchone()
            
            return {
                "nombre_coordinacion": f"{coord[0]} {coord[1]}" if coord else "",
                "nombre_gobernacion": f"{gob[0]} {gob[1]}" if gob else ""
            }
            
        except Exception as e:
            print(f"❌ Error al cargar jefaturas: {e}")
            return {"nombre_coordinacion": "", "nombre_gobernacion": ""}
    
    # ========== MÉTODOS DE VALIDACIÓN ==========
    
    @staticmethod
    def validar_cedula(cedula: str) -> bool:
        """Valida formato de cédula venezolana"""
        if not cedula:
            return False
        
        # Formato: V-12345678 o E-12345678
        partes = cedula.split('-')
        if len(partes) != 2:
            return False
        
        tipo, numero = partes
        if tipo.upper() not in ['V', 'E']:
            return False
        
        if not numero.isdigit() or len(numero) < 6 or len(numero) > 8:
            return False
        
        return True
    
    @staticmethod
    def validar_texto(texto: str, min_len: int = 3, max_len: int = 100) -> bool:
        """Valida texto genérico"""
        if not texto:
            return False
        return min_len <= len(texto.strip()) <= max_len
    
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.db.Cerrar()