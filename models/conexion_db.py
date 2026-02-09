import sqlite3

class ConexionDB:
    def __init__(self, nombre_db="database/SIGRAG.db"):
        self.base_datos = nombre_db
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        """Crea todas las tablas de la base de datos"""
        try:
            conn = self.conexion
            cursor = conn.cursor()
            
            # Tabla Reporte
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Reporte (
                    id_reporte INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabla Actividad
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Actividad (
                    id_Actividad INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descripcion TEXT,
                    ruta1 TEXT,
                    ruta2 TEXT,
                    fecha DATE,
                    tipo_Actividad TEXT
                )
            ''')

            # Tabla intermedia reporte_actividades
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS reporte_actividades (
                reporte_id INTEGER,
                actividad_id INTEGER,
                orden INTEGER DEFAULT 0,
                PRIMARY KEY (reporte_id, actividad_id),
                FOREIGN KEY (reporte_id) REFERENCES Reporte(id_reporte) ON DELETE CASCADE,
                FOREIGN KEY (actividad_id) REFERENCES Actividad(id_Actividad) ON DELETE CASCADE
            )
            """)

            # Tabla Usuario
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Usuario (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            
            # Tabla Coordinación
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Coordinacion (
                    id_coordinador INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    cedula INTENGER UNIQUE
                )
            ''')
            
            # Tabla Gobernación
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Gobernacion (
                    id_jefe INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    cedula INTENGER UNIQUE
                )
            ''')
            
            # Tabla Tema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Tema (
                    id_tema INTEGER PRIMARY KEY AUTOINCREMENT,
                    tema TEXT NOT NULL
                )
            ''')
            
            # Tabla Fuente
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Fuente (
                    id_fuente INTEGER PRIMARY KEY AUTOINCREMENT,
                    tamano INTEGER,
                    famila TEXT,
                    font TEXT
                )
            ''')
            
            # Tabla Dirección
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Direccion (
                    id_comunidad INTEGER PRIMARY KEY AUTOINCREMENT,
                    estado TEXT NOT NULL,
                    municipio TEXT NOT NULL,
                    parroquia TEXT,
                    instituto TEXT
                )
            ''')

            # Tabla de Objetivos de Reporte
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Objetivos_Reportes (
                id_objetivo INTEGER PRIMARY KEY AUTOINCREMENT,
                objetivo_semanal INTEGER,
                objetivo_mensual INTEGER,
                objetivo_trimestral INTEGER,
                objetivo_anual INTEGER
                )
            ''')

            # Tabla Gaceta
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Gaceta (
                    id_coordinador INTEGER,
                    decreto TEXT,
                    fecha_publicacion TEXT,
                    PRIMARY KEY(id_coordinador),
                    FOREIGN KEY (id_coordinador) REFERENCES Coordinacion(id_coordinador) ON DELETE CASCADE
                )
            ''')
            
            # Tabla Configuración
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Configuracion (
                    id_configuracion INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_tema INTEGER,
                    id_fuente INTEGER,
                    id_Direccion INTEGER,
                    id_coordinacion INTEGER,
                    id_gobernacion INTEGER,
                    id_objetivo INTEGER,
                    FOREIGN KEY (id_tema) REFERENCES Tema (id_tema),
                    FOREIGN KEY (id_fuente) REFERENCES Fuente (id_fuente),
                    FOREIGN KEY (id_coordinacion) REFERENCES Coordinacion (id_coordinacion),
                    FOREIGN KEY (id_gobernacion) REFERENCES Gobernacion (id_gobernacion),
                    FOREIGN KEY (id_objetivo) REFERENCES Objetivos_Reportes (id_objetivo)
                )
            ''')
            
        except sqlite3.Error as e:
            print(f"❌ Error al crear tablas: {e}")

    def Cerrar(self):
        self.conexion.commit()
        self.conexion.close()