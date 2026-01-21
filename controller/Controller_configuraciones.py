import sys
import os
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator, QPalette, QColor
from components.app_style import estilo_app

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from view.vista_configuracion import Ventana_configuracion
from models.Modelo_configuracion import Model_Configuraciones

class controlador_configuraciones(QWidget):
    # == Controlador que maneja TODA la lógica de configuraciones== 
    Actualizar_Vista = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        # Inicializar modelo y vista
        self.modelo = Model_Configuraciones()
        self.vista = Ventana_configuracion()
        
        # Configurar layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.vista)
        
        # Configurar validadores con expresiones regulares
        self.configurar_validadores()
        
        # Conectar señales
        self.vista.guardar_clicked.connect(self.on_guardar_clicked)
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
    
    def configurar_validadores(self):
        # == Configura validadores con expresiones regulares para todos los campos== 
        
        # Validadores para campos de dirección (solo letras, espacios y algunos caracteres especiales)
        regex_solo_texto = QRegExp(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ\s\.\-\(\)]+$')
        validador_texto = QRegExpValidator(regex_solo_texto, self)
        
        # Aplicar a campos de dirección
        self.vista.entry_estado.setValidator(validador_texto)
        self.vista.entry_municipio.setValidator(validador_texto)
        self.vista.entry_parroquia.setValidator(validador_texto)
        self.vista.entry_institucion.setValidator(validador_texto)
        
        # Validadores para nombres de jefaturas (similar a dirección pero puede incluir comas)
        regex_nombres = QRegExp(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ\s\.\-\(\)\,\']+$')
        validador_nombres = QRegExpValidator(regex_nombres, self)
        
        # Aplicar a nombres de jefaturas
        self.vista.entry_nombre_coord.setValidator(validador_nombres)
        self.vista.entry_nombre_gob.setValidator(validador_nombres)
        
        # Validadores para cédulas (formato V/E-12345678)
        regex_cedula = QRegExp(r'^[VE]-\d{5,9}$')
        validador_cedula = QRegExpValidator(regex_cedula, self)
        
        # Aplicar a cédulas
        self.vista.entry_cedula_coord.setValidator(validador_cedula)
        self.vista.entry_cedula_gob.setValidator(validador_cedula)
        
        # Validador para tamaño de fuente (solo números)
        regex_numeros = QRegExp(r'^\d+$')
        validador_numeros = QRegExpValidator(regex_numeros, self)
        
        # Aplicar al spin de tamaño
        self.vista.spin_tamano.lineEdit().setValidator(validador_numeros)
        
        # Configurar placeholder y tooltips para ayudar al usuario
        self.configurar_placeholders_y_tooltips()
    
    def configurar_placeholders_y_tooltips(self):
        # == Configura placeholders y tooltips para los campos== 
        
        # Campos de dirección
        self.vista.entry_estado.setPlaceholderText("Ej: Miranda")
        self.vista.entry_estado.setToolTip("Solo letras, espacios y caracteres .-()")
        
        self.vista.entry_municipio.setPlaceholderText("Ej: Sucre")
        self.vista.entry_municipio.setToolTip("Solo letras, espacios y caracteres .-()")
        
        self.vista.entry_parroquia.setPlaceholderText("Ej: Petare")
        self.vista.entry_parroquia.setToolTip("Solo letras, espacios y caracteres .-()")
        
        self.vista.entry_institucion.setPlaceholderText("Ej: Instituto Nacional de...")
        self.vista.entry_institucion.setToolTip("Solo letras, espacios y caracteres .-()")
        
        # Campos de nombres de jefaturas
        self.vista.entry_nombre_coord.setPlaceholderText("Ej: María Pérez")
        self.vista.entry_nombre_coord.setToolTip("Solo letras, espacios y caracteres .-(),'")
        
        self.vista.entry_nombre_gob.setPlaceholderText("Ej: Juan Rodríguez")
        self.vista.entry_nombre_gob.setToolTip("Solo letras, espacios y caracteres .-(),'")
        
        # Campos de cédulas
        self.vista.entry_cedula_coord.setPlaceholderText("Ej: V-12345678")
        self.vista.entry_cedula_coord.setToolTip("Formato: V-12345678 o E-12345678")
        
        self.vista.entry_cedula_gob.setPlaceholderText("Ej: E-87654321")
        self.vista.entry_cedula_gob.setToolTip("Formato: V-12345678 o E-12345678")

        # Campos de Gaceta
        self.vista.entry_decreto.setPlaceholderText("Ingrese el Decreto de la Gaceta Coordinador")
        self.vista.entry_decreto.setToolTip("Ingrese los datos necesarios")
        self.vista.entry_fechaPublicacion.setPlaceholderText("Ingrese un dato Válido")
        self.vista.entry_fechaPublicacion.setToolTip("Ingrese los datos de la efcha de publicacion")
    
    def cargar_datos_iniciales(self):
        # == Carga los datos desde la base de datos al iniciar== 
        try:
            # Obtener datos del modelo
            datos_interfaz = self.modelo.cargar_configuracion_interfaz()
            datos_direccion = self.modelo.cargar_datos_direccion()
            datos_jefaturas = self.modelo.cargar_datos_jefaturas()
            datos_gaceta = self.modelo.cargar_datos_gaceta()
            
            # Preparar datos para la vista
            datos = {
                "interfaz": datos_interfaz,
                "direccion": datos_direccion,
                "jefaturas": datos_jefaturas,
                "gaceta": datos_gaceta
            }
            
            # Establecer en vista
            self.establecer_valores(datos)
            
        except Exception as e:
            print(f"❌ Error al cargar datos iniciales: {e}")
            self.mostrar_mensaje("Error", f"No se pudieron cargar los datos: {str(e)}", "error")
    
    def on_guardar_clicked(self):
        # == Maneja el evento de clic en guardar== 
        print("Se ha ejecutado el botón")
        try:
            # 1. Obtener datos de la vista
            datos_crudos = self.obtener_valores()
            
            # 2. Validar datos
            if not self.validar_datos(datos_crudos):
                return

            # 3. Preparar datos para guardar
            datos_validados = self.preparar_datos_para_guardar(datos_crudos)
            
            # 4. Guardar en base de datos
            exito = self.guardar_en_bd(datos_validados)

            # 5. Actualizar configuración de estilo_app SI SE GUARDÓ BIEN
            if exito:
                # Obtener datos de interfaz para actualizar estilo_app
                tema = datos_validados["interfaz"]["tema"].lower()
                fuente_familia = datos_validados["interfaz"]["fuente"]
                fuente_tamano = datos_validados["interfaz"]["tamaño"]
                fuente_negrita = datos_validados["interfaz"]["negrita"]
                
                # Actualizar estilo_app (esto también notificará a las vistas)
                estilo_app.actualizar_y_notificar(
                    tema=tema,
                    fuente_familia=fuente_familia,
                    fuente_tamano=fuente_tamano,
                    fuente_negrita=fuente_negrita
                )
                
                # 6. Emitir señal para otras partes de la aplicación
                self.Actualizar_Vista.emit()
                
                # 7. Mostrar resultado
                self.mostrar_mensaje("Éxito", "Los cambios se guardaron correctamente", "success")
                # Limpiar errores después de guardar exitosamente
                self.limpiar_errores()
            else:
                self.mostrar_mensaje("Error", "No se pudieron guardar los cambios", "error")
                
        except Exception as e:
            print(f"❌ Error en on_guardar_clicked: {e}")
            self.mostrar_mensaje("Error", f"Ocurrió un error: {str(e)}", "error")

    
    def validar_datos(self, datos):
        # == Valida todos los datos antes de guardar== 
        self.limpiar_errores()
        
        # Validar interfaz
        if not self.validar_interfaz(datos.get("interfaz", {})):
            return False
        
        # Validar dirección
        if not self.validar_direccion(datos.get("direccion", {})):
            return False
        
        # Validar jefaturas
        if not self.validar_jefaturas(datos.get("jefaturas", {})):
            return False
        
        # Validar Gaceta
        if not self.validar_gaceta(datos.get("gaceta", {})):
            return False
        
        return True
    
    def validar_interfaz(self, datos_interfaz):
        # == Valida datos de interfaz== 
        # Validar tema
        tema = datos_interfaz.get("tema", "").lower()
        if tema not in ["claro", "oscuro"]:
            # Para radios, mostramos un mensaje general
            self.mostrar_mensaje("Error", "Seleccione un tema válido (Claro u Oscuro)", "error")
            return False
        
        # Validar fuente
        fuente = datos_interfaz.get("fuente", "").strip()
        if len(fuente) < 3:
            self.mostrar_error(self.vista.combo_fuente, "La fuente es requerida")
            return False
        
        # Validar tamaño
        tamaño = datos_interfaz.get("tamaño", 0)
        if not (8 <= tamaño <= 24):
            self.mostrar_error(self.vista.spin_tamano, "Tamaño debe estar entre 8 y 24")
            return False
        
        return True
    
    def validar_direccion(self, datos_direccion):
        # == Valida datos de dirección== 
        campos = [
            ("estado", self.vista.entry_estado, "Estado"),
            ("municipio", self.vista.entry_municipio, "Municipio"),
            ("parroquia", self.vista.entry_parroquia, "Parroquia"),
            ("institucion", self.vista.entry_institucion, "Institución")
        ]
        
        for campo_key, widget, campo_nombre in campos:
            valor = datos_direccion.get(campo_key, "").strip()
            
            # Validar requerido
            if not valor:
                self.mostrar_error(widget, f"{campo_nombre} es requerido")
                return False
            
            # Validar longitud mínima
            if len(valor) < 3:
                self.mostrar_error(widget, f"{campo_nombre} debe tener al menos 3 caracteres")
                return False
        
        return True
    
    def validar_jefaturas(self, datos_jefaturas):
        # == Valida datos de jefaturas== 
        # Validar nombres
        nombres = [
            ("nombre_coordinacion", self.vista.entry_nombre_coord, "Nombre de Coordinación"),
            ("nombre_gobernacion", self.vista.entry_nombre_gob, "Nombre de Gobernación")
        ]
        
        for campo_key, widget, campo_nombre in nombres:
            valor = datos_jefaturas.get(campo_key, "").strip()
            
            if not valor or len(valor) < 5:
                self.mostrar_error(widget, f"{campo_nombre} es requerido (mínimo 5 caracteres)")
                return False
        
        # Validar cédulas
        cedulas = [
            ("cedula_coordinacion", self.vista.entry_cedula_coord, "Cédula de Coordinación"),
            ("cedula_gobernacion", self.vista.entry_cedula_gob, "Cédula de Gobernación")
        ]
        
        for campo_key, widget, campo_nombre in cedulas:
            valor = datos_jefaturas.get(campo_key, "").strip()
            
            if not valor:
                self.mostrar_error(widget, f"{campo_nombre} es requerida")
                return False
            
            # Validar formato con regex (usando QRegExp)
            regex_cedula = QRegExp(r'^[VE]-\d{5,9}$')
            if not regex_cedula.exactMatch(valor):
                self.mostrar_error(widget, f"{campo_nombre} inválida. Formato: V-12345678 o E-12345678")
                return False
        
        return True

    def validar_gaceta(self, datos_gaceta):
         # Validar nombres
        entradas = [
            ("decreto", self.vista.entry_decreto, "Decreto"),
            ("fecha_publicacion", self.vista.entry_fechaPublicacion, "Fecha de Publicacion")
        ]

        for campo_key, widget, campo_nombre in entradas:
            valor = datos_gaceta.get(campo_key, "").strip()

            if not valor or len(valor) < 5:
                self.mostrar_error(widget, f"{campo_nombre} es requerido (mínimo 5 caracteres)")
                return False
        return True
        
            
        # Validar Fecha de Publicacion

    def preparar_datos_para_guardar(self, datos_crudos):
        # == Prepara y limpia los datos para guardar en BD== 
        return {
            "interfaz": {
                "tema": datos_crudos["interfaz"]["tema"].strip().lower(),
                "fuente": datos_crudos["interfaz"]["fuente"].strip(),
                "tamaño": datos_crudos["interfaz"]["tamaño"],
                "negrita": datos_crudos["interfaz"]["negrita"]
            },
            "direccion": {
                "estado": datos_crudos["direccion"]["estado"].strip(),
                "municipio": datos_crudos["direccion"]["municipio"].strip(),
                "parroquia": datos_crudos["direccion"]["parroquia"].strip(),
                "institucion": datos_crudos["direccion"]["institucion"].strip()
            },
            "jefaturas": {
                "nombre_coordinacion": datos_crudos["jefaturas"]["nombre_coordinacion"].strip(),
                "cedula_coordinacion": datos_crudos["jefaturas"]["cedula_coordinacion"].strip().upper(),
                "nombre_gobernacion": datos_crudos["jefaturas"]["nombre_gobernacion"].strip(),
                "cedula_gobernacion": datos_crudos["jefaturas"]["cedula_gobernacion"].strip().upper()
            },
            "gaceta": {
                "decreto": datos_crudos["gaceta"]["decreto"].strip(),
                "fecha_publicacion": datos_crudos["gaceta"]["fecha_publicacion"].strip()
            }
        }
    
    def guardar_en_bd(self, datos):
        # == Guarda los datos en la base de datos== 
        try:
            # Guardar interfaz
            exito_interfaz = self.modelo.guardar_configuracion_interfaz(
                datos["interfaz"]["tema"],
                datos["interfaz"]["fuente"],
                datos["interfaz"]["tamaño"],
                datos["interfaz"]["negrita"]
            )
            
            # Guardar dirección
            exito_direccion = self.modelo.guardar_datos_direccion(
                datos["direccion"]["estado"],
                datos["direccion"]["municipio"],
                datos["direccion"]["parroquia"],
                datos["direccion"]["institucion"]
            )
            
            # Guardar jefaturas
            exito_jefaturas = self.modelo.guardar_datos_jefaturas(
                datos["jefaturas"]["nombre_coordinacion"],
                datos["jefaturas"]["cedula_coordinacion"],
                datos["jefaturas"]["nombre_gobernacion"],
                datos["jefaturas"]["cedula_gobernacion"]
            )

            # Guardar Gaceta
            exito_gaceta = self.modelo.guardar_datos_gaceta(
                datos["gaceta"]["decreto"],
                datos["gaceta"]["fecha_publicacion"]
            )
            
            return exito_interfaz and exito_direccion and exito_jefaturas and exito_gaceta
            
        except Exception as e:
            print(f"❌ Error al guardar en BD: {e}")
            return False
    
    # ========== MÉTODOS GENERALES ==========
    
    def obtener_valores(self):
        # == Retorna todos los valores actuales a los widgets== 
        tema_vista = "claro" if self.vista.radio_tema_claro.isChecked() else "oscuro"
        return {
            "interfaz": {
                "tema": tema_vista,
                "fuente": self.vista.combo_fuente.currentText(),
                "tamaño": self.vista.spin_tamano.value(),
                "negrita": self.vista.check_negrita.isChecked()
            },
            "direccion": {
                "estado": self.vista.entry_estado.text(),
                "municipio": self.vista.entry_municipio.text(),
                "parroquia": self.vista.entry_parroquia.text(),
                "institucion": self.vista.entry_institucion.text()
            },
            "jefaturas": {
                "nombre_coordinacion": self.vista.entry_nombre_coord.text(),
                "cedula_coordinacion": self.vista.entry_cedula_coord.text(),
                "nombre_gobernacion": self.vista.entry_nombre_gob.text(),
                "cedula_gobernacion": self.vista.entry_cedula_gob.text()
            },
            "gaceta": {
                "decreto": self.vista.entry_decreto.text(),
                "fecha_publicacion": self.vista.entry_fechaPublicacion.text()
            }
        }
    
    def establecer_valores(self, datos):
        # == Establece los Valores de la Interfaz== 
        # Interfaz
        if datos.get("interfaz"):
            interfaz = datos["interfaz"]
            # Tema
            if interfaz.get("tema") == "claro":
                self.vista.radio_tema_claro.setChecked(True)
            elif interfaz.get("tema") == "oscuro":
                self.vista.radio_tema_oscuro.setChecked(True)
            else:
                # Por Defecto, Claro
                self.vista.radio_tema_claro.setChecked(True)

            # Fuente
            index = self.vista.combo_fuente.findText(interfaz.get("fuente", "Arial"))
            if index >= 0:
                self.vista.combo_fuente.setCurrentIndex(index)
            
            # Tamaño de Fuente
            self.vista.spin_tamano.setValue(interfaz.get("tamaño", 12))
            # Negrita
            self.vista.check_negrita.setChecked(interfaz.get("negrita", False))
        
        # Dirección
        if datos.get("direccion"):
            direccion = datos["direccion"]
            self.vista.entry_estado.setText(direccion.get("estado", ""))
            self.vista.entry_municipio.setText(direccion.get("municipio", ""))
            self.vista.entry_parroquia.setText(direccion.get("parroquia", ""))
            self.vista.entry_institucion.setText(direccion.get("institucion", ""))
        
        # Jefaturas
        if datos.get("jefaturas"):
            jefaturas = datos["jefaturas"]
            # Asegurar que las cédulas se carguen (convertir a mayúsculas si vienen de BD)
            cedula_coord = jefaturas.get("cedula_coordinacion", "")
            cedula_gob = jefaturas.get("cedula_gobernacion", "")
            
            self.vista.entry_nombre_coord.setText(jefaturas.get("nombre_coordinacion", ""))
            self.vista.entry_cedula_coord.setText(cedula_coord.upper() if cedula_coord else "")
            self.vista.entry_nombre_gob.setText(jefaturas.get("nombre_gobernacion", ""))
            self.vista.entry_cedula_gob.setText(cedula_gob.upper() if cedula_gob else "")

        # Gaceta
        if datos.get("gaceta"):
            gaceta = datos["gaceta"]
            self.vista.entry_decreto.setText(gaceta.get("decreto", ""))
            self.vista.entry_fechaPublicacion.setText(gaceta.get("fecha_publicacion", ""))

    
    def get_widget(self):
        # ==Retorna el widget para integrar en la aplicación==
        return self
    
    def cargar_datos_por_defecto(self):
        # ==Carga valores por defecto==
        datos_default = {
            "interfaz": {
                "tema": "Claro",
                "fuente": "Arial",
                "tamaño": 12,
                "negrita": False
            },
            "direccion": {
                "estado": "Monagas",
                "municipio": "Maturín",
                "parroquia": "",
                "institucion": ""
            },
            "jefaturas": {
                "nombre_coordinacion": "",
                "cedula_coordinacion": "",
                "nombre_gobernacion": "",
                "cedula_gobernacion": ""
            },
            "gaceta": {
                "decreto": "",
                "fecha_publicacion": ""
            }
        }
        self.establecer_valores(datos_default)
    
    def limpiar_campos(self):
        # ==Limpia todos los campos==
        # Interfaz
        self.vista.radio_tema_claro.setChecked(True)
        self.vista.combo_fuente.setCurrentIndex(0)
        self.vista.spin_tamano.setValue(12)
        self.vista.check_negrita.setChecked(False)
        # Dirección
        self.vista.entry_estado.clear()
        self.vista.entry_municipio.clear()
        self.vista.entry_parroquia.clear()
        self.vista.entry_institucion.clear()
        # Jefaturas
        self.vista.entry_nombre_coord.clear()
        self.vista.entry_cedula_coord.clear()
        self.vista.entry_nombre_gob.clear()
        self.vista.entry_cedula_gob.clear()
        # Gaceta
        self.vista.entry_decreto.clear()
        self.vista.entry_fechaPublicacion.clear()
        # Limpiar errores
        self.limpiar_errores()
    
    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        # == Muestra un mensaje al usuario== 
        if tipo == "error":
            QMessageBox.critical(self, titulo, mensaje)
        elif tipo == "warning":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "success":
            QMessageBox.information(self, titulo, mensaje)
        else:
            QMessageBox.information(self, titulo, mensaje)
    
    def mostrar_error(self, widget, mensaje):
        # ==Resalta un campo con error en rojo y muestra tooltip== 
        if widget:
            # Mantenemos el estilo original y añadimos un borde rojo
            estilo_actual = widget.styleSheet()
            
            # Separar las reglas CSS existentes
            lineas = estilo_actual.split('}')
            nuevo_estilo = ""
            
            # Buscar y modificar la regla QLineEdit (o QComboBox/QSpinBox)
            encontrado = False
            for linea in lineas:
                if linea.strip():
                    # Si encontramos el selector del widget
                    if 'QLineEdit' in linea or 'QComboBox' in linea or 'QSpinBox' in linea:
                        # Añadir borde rojo al estilo
                        if 'border:' not in linea:
                            linea += ' border: 2px solid #ff0000;'
                        else:
                            # Reemplazar el borde existente
                            linea = re.sub(r'border:\s*[^;]+;', 'border: 2px solid #ff0000 !important;', linea)
                        encontrado = True
                    nuevo_estilo += linea + '}'
            
            # Si no se encontró regla específica, crear una nueva
            if not encontrado:
                tipo_widget = 'QLineEdit'
                if hasattr(widget, 'clear'):  # Es QLineEdit
                    tipo_widget = 'QLineEdit'
                elif hasattr(widget, 'clearEditText'):  # Es QComboBox
                    tipo_widget = 'QComboBox'
                elif hasattr(widget, 'setMaximum'):  # Es QSpinBox
                    tipo_widget = 'QSpinBox'
                
                nuevo_estilo = f"{tipo_widget} {{ border: 2px solid #ff0000 !important; }}"
            
            widget.setStyleSheet(nuevo_estilo)
            
            # Establecer tooltip con mensaje de error
            widget.setToolTip(f"ERROR: {mensaje}")
            
            # Cambiar color de fondo a rojo claro usando QPalette (no CSS)
            palette = widget.palette()
            palette.setColor(QPalette.Base, QColor(255, 240, 240))
            widget.setPalette(palette)
            
            # Enfocar el widget
            widget.setFocus()
    
    def limpiar_errores(self):
        # == Limpia todos los marcadores de error== 
        # NO restauramos los estilos CSS completos
        # Solo eliminamos el borde rojo y restauramos el color de fondo
        
        widgets_entrada = [
            self.vista.entry_estado,
            self.vista.entry_municipio,
            self.vista.entry_parroquia,
            self.vista.entry_institucion,
            self.vista.entry_nombre_coord,
            self.vista.entry_cedula_coord,
            self.vista.entry_nombre_gob,
            self.vista.entry_cedula_gob,
            self.vista.combo_fuente,
            self.vista.spin_tamano
        ]
        
        # Restaurar solo color de fondo y tooltips, NO los estilos CSS
        for widget in widgets_entrada:
            if widget:
                # Restaurar color de fondo
                palette = widget.palette()
                palette.setColor(QPalette.Base, QColor(255, 255, 255))
                widget.setPalette(palette)
                
                # Regresar los widgets a como eran
                estilo_actual = widget.styleSheet()
                if 'border: 2px solid #ff0000' in estilo_actual:
                    # Volver a aplicar el estilo original llamando a configurar_estilos
                    if widget in [self.vista.entry_estado, self.vista.entry_municipio, 
                                 self.vista.entry_parroquia, self.vista.entry_institucion,
                                 self.vista.entry_nombre_coord, self.vista.entry_cedula_coord,
                                 self.vista.entry_nombre_gob, self.vista.entry_cedula_gob]:
                        
                        widget.setStyleSheet(f"""
                            {self.vista.estilo["styles"]["label"]}
                            {self.vista.estilo["styles"]["input"]}
                            {self.vista.estilo["styles"]["boton"]}
                            """)
        
        # Restaurar tooltips originales
        self.configurar_placeholders_y_tooltips()

    def cerrar(self):
        # == Cierra conexiones== 
        self.modelo.cerrar_conexion()