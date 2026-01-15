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
        self._crear_usuario_admin()

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
                columnas_requeridas = ['id_usuario', 'user', 'password']
                for col in columnas_requeridas:
                    if col not in columnas_nombres:
                        return False
                return True

        except Exception as e:
            print(f"❌ Error verificando tabla Usuario: {e}")
            return False
        
    def _hash_password(self, password: str) -> str:
        # Genera hash SHA-256 de la contraseña, encriptando la contraseña
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _crear_tablas(self):
        self.database.crear_tablas
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
        
    def _crear_usuario_admin(self):
        """Crea un usuario administrador por defecto si no existe"""
        try:
            cursor = self.conexion_db.cursor
            # Verificar si ya existe el usuario admin
            cursor.execute("SELECT COUNT(*) FROM Usuario WHERE user = 'admin'")
            existe = cursor.fetchone()[0]
            
            if existe == 0:
                # Crear la contraseña para el usuario
                password_hash = self._hash_password("admin")
                
                # Insertar los valores en la base de dato
                cursor.execute('''
                    INSERT INTO Usuario (user, password)
                    VALUES (?, ?)
                ''', ('admin', password_hash))
                
                self.conexion_db.conexion.commit()
                print("Usuario admin creado")
                print("Usuario: admin")
                print("Contraseña: admin")
            else:
                print("Usuario admin ya existe")
                
        except Exception as e:
            print(f"❌ Error al crear usuario admin: {e}")
    
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
    
    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual"""
        self.usuario_actual = None
    
    def verificar_usuario_existe(self, username: str) -> bool:
        """Verifica si un usuario existe en la base de datos"""
        try:
            cursor = self.conexion_db.cursor
            cursor.execute("SELECT id_usuario FROM Usuario WHERE user = ?", (username,))
            return cursor.fetchone() is not None
        except:
            return False
        
    def __del__(self):
        """Destructor: cierra la conexión al eliminar el objeto"""
        try:
            self.conexion_db.Cerrar()
        except:
            pass

    def inicializar_configuracion(self):
        db = ConexionDB()
        
        # Insertar tema por defecto
        db.cursor.execute("INSERT OR IGNORE INTO Tema (tema) VALUES ('claro')")
        db.cursor.execute("INSERT OR IGNORE INTO Tema (tema) VALUES ('oscuro')")
        
        # Insertar configuración de fuente por defecto
        db.cursor.execute("""
            INSERT OR IGNORE INTO Fuente (tamano, famila, font) 
            VALUES (12, 'Arial', 'normal')
        """)
        
        # Insertar configuración por defecto
        db.cursor.execute("""
            INSERT OR IGNORE INTO Configuracion (id_tema, id_fuente) 
            VALUES (1, 1)
        """)
    