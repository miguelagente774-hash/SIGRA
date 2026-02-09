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
    
    def guardar_datos_objetivos(self, 
                               objetivo_semanal: str,
                               objetivo_mensual: str,
                               objetivo_trimestral: str,
                               objetivo_anual: str) -> bool:
        """Guarda los datos de objetivos en la BD"""
        try:
            conn = self.db.conexion
            cursor = conn.cursor()
            
            # Insertar o actualizar los objetivos en la tabla Objetivos_Reportes
            cursor.execute("""
                INSERT OR REPLACE INTO Objetivos_Reportes 
                (id_objetivo, objetivo_semanal, objetivo_mensual, 
                 objetivo_trimestral, objetivo_anual) 
                VALUES (1, ?, ?, ?, ?)
            """, (objetivo_semanal, objetivo_mensual, 
                  objetivo_trimestral, objetivo_anual))
            
            self.db.conexion.commit()
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar dirección: {e}")
            return False
    
    def cargar_datos_objetivos(self) -> Dict[str, str]:
        """Carga los datos de objetivos desde la BD"""
        try:
            cursor = self.db.conexion.cursor()
            
            # Obtener los objetivos desde la tabla Objetivos_Reportes
            cursor.execute("""
                SELECT objetivo_semanal, objetivo_mensual, 
                       objetivo_trimestral, objetivo_anual 
                FROM Objetivos_Reportes WHERE id_objetivo = 1
            """)
            datos = cursor.fetchone()
            
            if datos:
                return {
                    "objetivo_semanal": datos[0] if datos else "5",
                    "objetivo_mensual": datos[1] if datos else "10",
                    "objetivo_trimestral": datos[2] if datos else "30",
                    "objetivo_anual": datos[3] if datos else "90"
                }
            else:
            # Si no hay datos, retornar valores por defecto
                return {
                    "objetivo_semanal": "5",
                    "objetivo_mensual": "10", 
                    "objetivo_trimestral": "30",
                    "objetivo_anual": "90"
                }
            
        except Exception as e:
            print(f"❌ Error al cargar objetivos: {e}")
            return {
                "objetivo_semanal": "5",
                "objetivo_mensual": "10",
                "objetivo_trimestral": "30",
                "objetivo_anual": "90"
            }
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
        # ==Guarda los datos de jefaturas en la BD==
        try:
            conn = self.db.conexion
            cursor = conn.cursor()
            
            # Separar nombres y apellidos para coordinación
            if nombre_coordinacion:
                partes_nombre = nombre_coordinacion.split()
                nombres_coord = partes_nombre[0] if len(partes_nombre) > 0 else ""
                apellidos_coord = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ""
            else:
                nombres_coord = ""
                apellidos_coord = ""
            
            # Guardar coordinación
            cursor.execute("""
                INSERT OR REPLACE INTO Coordinacion 
                (id_coordinador, nombres, apellidos, cedula) 
                VALUES (1, ?, ?, ?)
            """, (nombres_coord, apellidos_coord, cedula_coordinacion))
            
            # Separar nombres y apellidos para gobernación
            if nombre_gobernacion:
                partes_nombre = nombre_gobernacion.split()
                nombres_gob = partes_nombre[0] if len(partes_nombre) > 0 else ""
                apellidos_gob = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ""
            else:
                nombres_gob = ""
                apellidos_gob = ""
            
            # Guardar gobernación
            cursor.execute("""
                INSERT OR REPLACE INTO Gobernacion 
                (id_jefe, nombres, apellidos, cedula) 
                VALUES (1, ?, ?, ?)
            """, (nombres_gob, apellidos_gob, cedula_gobernacion))
            
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
            import traceback
            traceback.print_exc()
            return False

    def cargar_datos_jefaturas(self) -> Dict[str, str]:
        # ==Carga los datos de las Jefaturas desde la Base de Datos==
        try:
            cursor = self.db.conexion.cursor()

            cursor.execute("""
                SELECT nombres, apellidos, cedula FROM Coordinacion WHERE id_coordinador = 1
            """)
            coord = cursor.fetchone()

            cursor.execute("""
                           SELECT nombres, apellidos, cedula FROM Gobernacion WHERE id_jefe = 1
            """)
            
            gob = cursor.fetchone()

            # Construir nombres completos y cédulas
            nombre_completo_coord = ""
            cedula_coord = ""
            if coord and coord[0] and coord[1]:
                nombre_completo_coord = f"{coord[0]} {coord[1]}"
            elif coord and coord[0]:
                nombre_completo_coord = coord[0]

            if coord and coord[2]:
                cedula_coord = coord[2]

            nombre_completo_gob = ""
            cedula_gob = ""
            if gob and gob[0] and gob[1]:
                nombre_completo_gob = f"{gob[0]} {gob[1]}"
            elif gob and gob[0]:
                nombre_completo_gob = gob[0]

            if gob and gob[2]:
                cedula_gob = gob[2]

            return {
                "nombre_coordinacion": nombre_completo_coord,
                "cedula_coordinacion": cedula_coord,
                "nombre_gobernacion": nombre_completo_gob,
                "cedula_gobernacion": cedula_gob
            }
        
        except Exception as e:
            print("Ha ocurrido un error a cargar la base de datos: {e}")
            return {
                "nombre_coordinacion": "",
                "nombre_cedula": "",
                "nombre_gobernacion": "",
                "nombre_cedula": ""
            }

    # == MÉTODOS PARA DATOS DE GACETA==
            
    def guardar_datos_gaceta(self,
                             decreto: str,
                             fecha_publicacion: str) -> bool:
        # ==Guardar los datos en la Base de Dato==
        try: 
            conn = self.db.conexion
            cursor = conn.cursor()

            # Guardar Datos de la Gaceta
            cursor.execute("""
                INSERT OR REPLACE INTO Gaceta
                (id_coordinador, decreto, fecha_publicacion)
                VALUES (1, ?, ?)
            """, (decreto, fecha_publicacion))

            conn.commit()
            print("Datos de la Gaceta Guardados")
            return True
        
        except Exception as e:
            print(f"Error al guaradr Gacetas: {e}")
            import traceback
            traceback.print_exc()
            return False

        
    def cargar_datos_gaceta(self) -> Dict[str, str]:
        try:
            cursor = self.db.conexion.cursor()

            cursor.execute("""
                SELECT decreto, fecha_publicacion 
                FROM Gaceta WHERE id_coordinador = 1
            """)
            datos = cursor.fetchone()
            
            if datos:
                return {
                    "decreto": datos[0],
                    "fecha_publicacion": datos[1]
                }
            return {"decreto": "", "fecha_publicacion": ""}
        
        except Exception as e:
            print(f"Error al cargar Gaceta: {e}")
            return {"decreto": "", "fecha_publicacion": ""}

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