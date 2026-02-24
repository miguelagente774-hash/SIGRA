import hashlib
from typing import Optional, Tuple, Dict, Any
from .conexion_db import ConexionDB
class Model_Login:
    """Modelo para manejar la autenticación de usuarios usando la tabla Usuario básica."""
    
    def __init__(self):
        # Inicializar conexión a la base de datos SIGRA.db
        self.conexion_db = ConexionDB()
        self.usuario_actual: Optional[Dict[str, Any]] = None
    
        # Verificar que la tabla Usuario exista con la estructura básica
        self._verificar_tabla_usuario()
        self._crear_tabla()

    def _hash_password(self, password: str) -> str:
        # Genera hash SHA-256 de la contraseña, encriptando la contraseña
        return hashlib.sha256(password.encode()).hexdigest()

    
    def _crear_tabla(self):
        cursor = self.conexion_db.cursor

        # Verificar la tabla de datos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
    def _crear_usuario_admin(self, usuario, password, datos_seguridad):
        # Crea un usuario administrador por defecto si no existe
        try:
            cursor = self.conexion_db.cursor
            # Verificar si ya existe el usuario admin
        
            # Crear la contraseña para el usuario
            password_hash = self._hash_password(str(password))
            respuesta_seguridad_1 = str(datos_seguridad[0]['respuesta']).strip()
            respuesta_seguridad_2 = str(datos_seguridad[1]['respuesta']).strip()
            respuesta_seguridad_3 = str(datos_seguridad[2]['respuesta']).strip()

            sql = """
                INSERT INTO Usuario (user, password, 
                            pregunta_seguridad_1, respuesta_seguridad_1,
                            pregunta_seguridad_2, respuesta_seguridad_2,
                            pregunta_seguridad_3, respuesta_seguridad_3)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            valores = (
                usuario, 
                password_hash,
                datos_seguridad[0]['pregunta'], respuesta_seguridad_1,
                datos_seguridad[1]['pregunta'], respuesta_seguridad_2,
                datos_seguridad[2]['pregunta'], respuesta_seguridad_3
            )
            cursor.execute(sql, valores)
            self.conexion_db.conexion.commit()
            return True
        except Exception as e:
            print(f"❌ Error al crear usuario admin: {e}")
            return False
    
    def autenticar_usuario(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        # Validaciones básicas
        if not username or not username.strip():
            return False, "El nombre de usuario es requerido", None
        
        if not password or not password.strip():
            return False, "La contraseña es requerida", None
        
        try:
            cursor = self.conexion_db.cursor
            
            # Buscar usuario por username
            cursor.execute('''
                SELECT id_usuario, user, password
                FROM Usuario 
                WHERE user = ?
            ''', (username,))
            
            usuario_data = cursor.fetchone()
            
            # Verificar si el usuario existe
            if not usuario_data:
                return False, "Usuario no encontrado", None
            
            # Convertir a diccionario
            usuario_dict = {
                'id_usuario': usuario_data[0],
                'user': usuario_data[1],
                'password': usuario_data[2]
            }
            
            # Verificar contraseña
            password_hash = self._hash_password(password)
            
            if usuario_dict['password'] != password_hash:
                return False, "Contraseña incorrecta", None
            
            # Limpiar datos sensibles antes de devolver
            usuario_dict.pop('password', None)
            usuario_dict['autenticado'] = True
            
            # Guardar usuario actual
            self.usuario_actual = usuario_dict
            
            return True, f"¡Bienvenido, {username}!", usuario_dict
            
        except Exception as e:
            error_msg = str(e)
            return False, f"Error del sistema: {error_msg}", None
    
    def obtener_usuario_actual(self) -> Optional[Dict[str, Any]]:
        """Obtiene los datos del usuario actualmente autenticado"""
        return self.usuario_actual
    
    def _verificar_tabla_usuario(self):
        #Verifica que la tabla Usuario exista
        try:
            cursor = self.conexion_db.cursor
            
            # Verificar si la tabla Usuario existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuario'")
            tabla_existe = cursor.fetchone()
            
            if tabla_existe:
                # Verificar estructura de la tabla
                cursor.execute("PRAGMA table_info(Usuario)")
                columnas = cursor.fetchall()
                columnas_nombres = [col[1] for col in columnas]
                
                # Verificar columnas mínimas requeridas
                columnas_requeridas = ['id_usuario', 'user', 'password', 'pregunta_seguridad_1', 'respuesta_seguridad_1']
                for col in columnas_requeridas:
                    if col not in columnas_nombres:
                        return False
                return True
            return True

        except Exception as e:
            print(f"❌ Error verificando tabla Usuario: {e}")
            return False
      
    def verificar_usuarios_existentes(self) -> bool:
        """Retorna True si existe al menos un usuario en la base de datos."""
        try:
            cursor = self.conexion_db.cursor
            cursor.execute("SELECT COUNT(*) FROM Usuario")
            resultado = cursor.fetchone()
            return resultado[0] > 0 if resultado else False
        except Exception:
            return False

    def obtener_preguntas_usuario(self, username):
        """Retorna las 3 preguntas de seguridad de un usuario específico."""
        try:
            cursor = self.conexion_db.cursor
            cursor.execute("""
                SELECT pregunta_seguridad_1, pregunta_seguridad_2, pregunta_seguridad_3 
                FROM Usuario WHERE user = ?""", (username,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener preguntas: {e}")
            return None

    def validar_respuestas_sistema(self, username: str, respuestas: list) -> bool:
        """Compara las respuestas ingresadas con las de la base de datos."""
        try:
            cursor = self.conexion_db.cursor
            cursor.execute("""
                SELECT respuesta_seguridad_1, respuesta_seguridad_2, respuesta_seguridad_3 
                FROM Usuario WHERE user = ?""", (username,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Comparamos ignorando espacios
                valido = all((r_user.strip() == r_db.strip()) for r_user, r_db in zip(respuestas, resultado))
                return valido
            return False
        except Exception:
            return False

    def actualizar_password(self, username, nueva_password):
        """Actualiza la contraseña con el nuevo hash."""
        try:
            cursor = self.conexion_db.cursor
            password_hash = self._hash_password(nueva_password)
            cursor.execute("UPDATE Usuario SET password = ? WHERE user = ?", (password_hash, username))
            self.conexion_db.conexion.commit()
            return True
        except Exception:
            return False
        

    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual"""
        self.usuario_actual = None
    

    def __del__(self):
        # Destructor: cierra la conexión al eliminar el objeto
        try:
            self.conexion_db.Cerrar()
        except:
            pass