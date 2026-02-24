import sys
import os
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QAction
from PyQt5.QtCore import pyqtSignal, QRegExp, QPropertyAnimation, QEasingCurve
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
        self.vista.guardar_clicked.connect(self.guardar_datos)
        self.vista.tecla_guardar.triggered.connect(self.guardar_datos)
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
        self.cargar_preguntas_iniciales()
    
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
        
        # Validadores para Objetivos
        regex_objetivos = QRegExp(r'^\d+$')
        validador_objetivos = QRegExpValidator(regex_objetivos, self)

        # Aplicar en Objetivos
        self.vista.entry_semanal.setValidator(validador_objetivos)
        self.vista.entry_mensual.setValidator(validador_objetivos)
        self.vista.entry_trimestral.setValidator(validador_objetivos)
        self.vista.entry_anual.setValidator(validador_objetivos)

        # Validador para tamaño de fuente (solo números)
        regex_numeros = QRegExp(r'^\d+$')
        validador_numeros = QRegExpValidator(regex_numeros, self)
        
        # Aplicar al spin de tamaño
        self.vista.spin_tamano.lineEdit().setValidator(validador_numeros)
        
        # Validadores para respuestas de seguridad (solo letras, espacios y algunos caracteres)
        regex_respuesta = QRegExp(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ\s\.\-]+$')
        validador_respuesta = QRegExpValidator(regex_respuesta, self)
        
        # Aplicar a campos de respuesta de seguridad
        self.vista.entry_respuesta1.setValidator(validador_respuesta)
        self.vista.entry_respuesta2.setValidator(validador_respuesta)
        self.vista.entry_respuesta3.setValidator(validador_respuesta)

        # Configurar placeholder y tooltips para ayudar al usuario
        self.configurar_placeholders_y_tooltips()
    
    def configurar_placeholders_y_tooltips(self):
        # == Configura placeholders y tooltips para los campos== 

        # Campos de Objetivos
        self.vista.entry_semanal.setPlaceholderText("Ingrese la cantidad de actividades semanales")
        self.vista.entry_semanal.setToolTip("Solo números")

        self.vista.entry_mensual.setPlaceholderText("Ingrese la cantidad de actividades mensuales")
        self.vista.entry_mensual.setToolTip("Solo números")

        self.vista.entry_trimestral.setPlaceholderText("Ingrese la cantidad de actividades trimestrales")
        self.vista.entry_trimestral.setToolTip("Solo números")

        self.vista.entry_anual.setPlaceholderText("Ingrese la cantidad de actividades anuales")
        self.vista.entry_anual.setToolTip("Solo números")
        
        # Campos de dirección
        self.vista.entry_estado.setPlaceholderText("Ej: Monagas")
        self.vista.entry_estado.setToolTip("Solo letras, espacios y caracteres .-()")
        
        self.vista.entry_municipio.setPlaceholderText("Ej: Maturín")
        self.vista.entry_municipio.setToolTip("Solo letras, espacios y caracteres .-()")
        
        self.vista.entry_parroquia.setPlaceholderText("Ej: San Simón")
        self.vista.entry_parroquia.setToolTip("Solo letras, espacios y caracteres .-()")
        
        self.vista.entry_institucion.setPlaceholderText("Ej: Gobernación")
        self.vista.entry_institucion.setToolTip("Solo letras, espacios y caracteres .-()")
        
        # Campos de nombres de jefaturas
        self.vista.entry_nombre_coord.setPlaceholderText("Ej: María Pérez")
        self.vista.entry_nombre_coord.setToolTip("Solo letras, espacios y caracteres .-(),'")
        
        self.vista.entry_nombre_gob.setPlaceholderText("Ej: Juan Rodríguez")
        self.vista.entry_nombre_gob.setToolTip("Solo letras, espacios y caracteres .-(),'")
        
        # Campos de cédulas
        self.vista.entry_cedula_coord.setPlaceholderText("Ej: V-12345678")
        self.vista.entry_cedula_coord.setToolTip("Formato: V-12345678 o E-12345678")
        
        self.vista.entry_cedula_gob.setPlaceholderText("Ej: V-87654321")
        self.vista.entry_cedula_gob.setToolTip("Formato: V-12345678 o E-12345678")

        # Campos de Gaceta
        self.vista.entry_decreto.setPlaceholderText("Ingrese el Decreto de la Gaceta Coordinador")
        self.vista.entry_decreto.setToolTip("Ingrese los datos necesarios")
        self.vista.entry_fechaPublicacion.setPlaceholderText("Ingrese un dato Válido")
        self.vista.entry_fechaPublicacion.setToolTip("Ingrese los datos de la efcha de publicacion")

        # Campos de seguridad
        self.vista.entry_respuesta1.setPlaceholderText("Ingrese su respuesta")
        self.vista.entry_respuesta1.setToolTip("Solo letras, espacios y caracteres .-")
        
        self.vista.entry_respuesta2.setPlaceholderText("Ingrese su respuesta")
        self.vista.entry_respuesta2.setToolTip("Solo letras, espacios y caracteres .-")
        
        self.vista.entry_respuesta3.setPlaceholderText("Ingrese su respuesta")
        self.vista.entry_respuesta3.setToolTip("Solo letras, espacios y caracteres .-")
    
    def cargar_datos_iniciales(self):
    # == Carga los datos desde la base de datos al iniciar== 
        try:
            # Obtener datos del modelo
            datos_interfaz = self.modelo.cargar_configuracion_interfaz()
            datos_objetivos = self.modelo.cargar_datos_objetivos()
            datos_direccion = self.modelo.cargar_datos_direccion()
            datos_jefaturas = self.modelo.cargar_datos_jefaturas()
            datos_gaceta = self.modelo.cargar_datos_gaceta()
            datos_seguridad = self.modelo.cargar_datos_seguridad()
            
            # Preparar datos para la vista
            datos = {
                "interfaz": datos_interfaz,
                "objetivos": datos_objetivos,
                "direccion": datos_direccion,
                "jefaturas": datos_jefaturas,
                "gaceta": datos_gaceta,
                "seguridad": datos_seguridad
            }
            
            # Establecer en vista
            self.establecer_valores(datos)
            
        except Exception as e:
            self.mostrar_mensaje("Error", f"No se pudieron cargar los datos: {str(e)}", "error")
    
    def guardar_datos(self):
        # == Maneja el evento de clic en guardar== 
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
            self.mostrar_mensaje("Error", f"Ocurrió un error: {str(e)}", "error")

    
    def validar_datos(self, datos):
        # == Valida todos los datos antes de guardar== 
        self.limpiar_errores()
        
        # Validar interfaz
        if not self.validar_interfaz(datos.get("interfaz", {})):
            return False
        
        # Validar objetivo - CORREGIDO: llamar a validar_objetivos
        if not self.validar_objetivos(datos.get("objetivos", {})):
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
        
        if not self.validar_seguridad(datos.get("seguridad", {})):
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
    
    def validar_objetivos(self, datos_objetivos):
        # ==Validar objetivos==

        # Definir los Widgets y nombres para la validación de campos
        objetivos = [
            ("objetivo_semanal", self.vista.entry_semanal, "Semanal"),
            ("objetivo_mensual", self.vista.entry_mensual, "Mensual"),
            ("objetivo_trimestral", self.vista.entry_trimestral, "Trimestral"),
            ("objetivo_anual", self.vista.entry_anual, "Anual")
        ]
        # Validar que no estén vacíos
        for campo_key, widget, campo_nombre in objetivos:
            valor = datos_objetivos.get(campo_key, "").strip()
            if not valor:
                self.mostrar_error(widget, f"{campo_nombre} es requerida")
                return False

        try:
            # 1. Obtener el texto y convertir a entero (usamos 0 si está vacío)
            semanal = int(self.vista.entry_semanal.text() or 0)
            mensual = int(self.vista.entry_mensual.text() or 0)
            trimestral = int(self.vista.entry_trimestral.text() or 0)
            anual = int(self.vista.entry_anual.text() or 0)

            # 2. Verificar la jerarquía lógica
            # Semanal no puede ser mayor a Mensual
            if semanal > mensual:
                self.mostrar_error(self.vista.entry_semanal, "El objetivo Semanal no puede superar al Mensual")
                return False

            # Mensual no puede ser mayor a Trimestral
            if mensual > trimestral:
                self.mostrar_error(self.vista.entry_mensual, "El objetivo Mensual no puede superar al Trimestral")
                return False

            # Trimestral no puede ser mayor a Anual
            if trimestral > anual:
                self.mostrar_error(self.vista.entry_trimestral, "El objetivo Trimestral no puede superar al Anual")
                return False

            # Si llegó aquí, todo es válido
            return True

        except ValueError:
            # Si alguno no es número, el error se captura aquí de forma general
            self.mostrar_error(self, "Ingrese solo números enteros")
            return False
        
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
            
            if not valor:
                self.mostrar_error(widget, f"{campo_nombre} es requerida")
                return False
            
            regex_texto = QRegExp(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ\s\.\-\(\)]+$')
            if not regex_texto.exactMatch(valor):
                self.mostrar_error(widget, f"{campo_nombre} contiene caracteres no válidos")
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

    def validar_seguridad(self, datos_seguridad):
            """Valida las preguntas y respuestas de seguridad"""
            # Validar que las respuestas no estén vacías
            respuestas = [
                ("respuesta_1", self.vista.entry_respuesta1, "Respuesta 1"),
                ("respuesta_2", self.vista.entry_respuesta2, "Respuesta 2"),
                ("respuesta_3", self.vista.entry_respuesta3, "Respuesta 3")
            ]
            
            for campo_key, widget, campo_nombre in respuestas:
                valor = datos_seguridad.get(campo_key, "").strip()
                if not valor:
                    self.mostrar_error(widget, f"{campo_nombre} es requerida")
                    return False
                if len(valor) < 3:
                    self.mostrar_error(widget, f"{campo_nombre} debe tener al menos 3 caracteres")
                    return False
            
            # Validar que las preguntas sean diferentes
            preguntas = [
                datos_seguridad.get("pregunta_1", ""),
                datos_seguridad.get("pregunta_2", ""),
                datos_seguridad.get("pregunta_3", "")
            ]
            
            if len(set(preguntas)) < 3:
                self.mostrar_mensaje("Error", "Las preguntas de seguridad deben ser diferentes", "error")
                return False
            
            return True

    def preparar_datos_para_guardar(self, datos_crudos):
        # == Prepara y limpia los datos para guardar en BD== 
        return {
            "interfaz": {
                "tema": datos_crudos["interfaz"]["tema"].strip().lower(),
                "fuente": datos_crudos["interfaz"]["fuente"].strip(),
                "tamaño": datos_crudos["interfaz"]["tamaño"],
                "negrita": datos_crudos["interfaz"]["negrita"]
            },
            "objetivos": {
                "objetivo_semanal": datos_crudos["objetivos"]["objetivo_semanal"].strip(),
                "objetivo_mensual": datos_crudos["objetivos"]["objetivo_mensual"].strip(),
                "objetivo_trimestral": datos_crudos["objetivos"]["objetivo_trimestral"].strip(),
                "objetivo_anual": datos_crudos["objetivos"]["objetivo_anual"].strip(),
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
            },
            "seguridad": {
                "pregunta_1": datos_crudos["seguridad"]["pregunta_1"].strip(),
                "respuesta_1": datos_crudos["seguridad"]["respuesta_1"].strip(),
                "pregunta_2": datos_crudos["seguridad"]["pregunta_2"].strip(),
                "respuesta_2": datos_crudos["seguridad"]["respuesta_2"].strip(),
                "pregunta_3": datos_crudos["seguridad"]["pregunta_3"].strip(),
                "respuesta_3": datos_crudos["seguridad"]["respuesta_3"].strip()
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

            # Guardar Objetivosd

            exito_objetivos = self.modelo.guardar_datos_objetivos(
                datos["objetivos"]["objetivo_semanal"],
                datos["objetivos"]["objetivo_mensual"],
                datos["objetivos"]["objetivo_trimestral"],
                datos["objetivos"]["objetivo_anual"]
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

            # Guardar preguntas de seguridad
            exito_seguridad = self.modelo.guardar_datos_seguridad(
            datos["seguridad"]["pregunta_1"],
            datos["seguridad"]["respuesta_1"],
            datos["seguridad"]["pregunta_2"],
            datos["seguridad"]["respuesta_2"],
            datos["seguridad"]["pregunta_3"],
            datos["seguridad"]["respuesta_3"]
        )
            
            return exito_interfaz and exito_objetivos and exito_direccion and exito_jefaturas and exito_gaceta and exito_seguridad
            
        except Exception as e:
            print(f"❌ Error al guardar en BD: {e}")
            return False
    
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
            "objetivos": {
                "objetivo_semanal": self.vista.entry_semanal.text(),
                "objetivo_mensual": self.vista.entry_mensual.text(),
                "objetivo_trimestral": self.vista.entry_trimestral.text(),
                "objetivo_anual": self.vista.entry_anual.text()
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
            },
            "seguridad": {
            "pregunta_1": self.vista.combo_pregunta1.currentText(),
            "respuesta_1": self.vista.entry_respuesta1.text(),
            "pregunta_2": self.vista.combo_pregunta2.currentText(),
            "respuesta_2": self.vista.entry_respuesta2.text(),
            "pregunta_3": self.vista.combo_pregunta3.currentText(),
            "respuesta_3": self.vista.entry_respuesta3.text()
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

        # Objetivos
        if datos.get("objetivos"):
            objetivos = datos["objetivos"]

            # Definir variable de los datos obtenidos
            semanal = objetivos.get("objetivo_semanal", "")
            mensual = objetivos.get("objetivo_mensual", "")
            trimestral = objetivos.get("objetivo_trimestral", "")
            anual = objetivos.get("objetivo_anual", "")
    
            # Se ingresan valores por defecto si no hay en la Base de Datos
            self.vista.entry_semanal.setText(str(semanal if semanal else "5"))
            self.vista.entry_mensual.setText(str(mensual if mensual else "10"))
            self.vista.entry_trimestral.setText(str(trimestral if trimestral else "30"))
            self.vista.entry_anual.setText(str(anual if anual else "90"))
        
        # Dirección
        if datos.get("direccion"):
            direccion = datos["direccion"]

            # Definir variable de los datos obtenidos
            estado = direccion.get("estado", "")
            municipio = direccion.get("municipio", "")
            parroquia = direccion.get("parroquia", "")
            institucion = direccion.get("institucion", "")
            
            # Se ingresan valores por defecto si no hay en la Base de Datos
            self.vista.entry_estado.setText(estado if estado else "Monagas")
            self.vista.entry_municipio.setText(municipio if municipio else "Maturín")
            self.vista.entry_parroquia.setText(parroquia if parroquia else "San Simón")
            self.vista.entry_institucion.setText(institucion if institucion else "Gobernación Institución")

        # Jefaturas
        if datos.get("jefaturas"):
            jefaturas = datos["jefaturas"]
            
            # Definir variable de los datos obtenidos
            nombre_coord = jefaturas.get("nombre_coordinacion", "")
            cedula_coord = jefaturas.get("cedula_coordinacion", "")
            nombre_gob = jefaturas.get("nombre_gobernacion", "")
            cedula_gob = jefaturas.get("cedula_gobernacion", "")
            
            # Se ingresan valores por defecto si no hay en la Base de Datos
            self.vista.entry_nombre_coord.setText(nombre_coord if nombre_coord else "Coordinacion")
            self.vista.entry_cedula_coord.setText(cedula_coord.upper() if cedula_coord else "V-12346789")
            self.vista.entry_nombre_gob.setText(nombre_gob if nombre_gob else "Gobernador")
            self.vista.entry_cedula_gob.setText(cedula_gob.upper() if cedula_gob else "V-12346789")

        # Gaceta
        if datos.get("gaceta"):
            gaceta = datos["gaceta"]

            # Definir variable de los datos obtenidos
            decreto = gaceta.get("decreto", "")
            fecha = gaceta.get("fecha_publicacion", "")
            # Se ingresan valores por defecto si no hay en la Base de Datos
            self.vista.entry_decreto.setText(decreto if decreto else "Ingrese el Decreto")
            self.vista.entry_fechaPublicacion.setText(fecha if fecha else "Ingrese la Fecha de Publicación")

        # Seguridad
        if datos.get("seguridad"):
            seguridad = datos["seguridad"]
            
            # Establecer preguntas - buscar el índice correcto
            pregunta_1 = seguridad.get("pregunta_1", "¿Nombre de tu mascota?")
            index = self.vista.combo_pregunta1.findText(pregunta_1)
            if index >= 0:
                self.vista.combo_pregunta1.setCurrentIndex(index)
            else:
                # Si no encuentra la pregunta, establecer la primera
                self.vista.combo_pregunta1.setCurrentIndex(0)
            
            pregunta_2 = seguridad.get("pregunta_2", "¿Ciudad de nacimiento?")
            index = self.vista.combo_pregunta2.findText(pregunta_2)
            if index >= 0:
                self.vista.combo_pregunta2.setCurrentIndex(index)
            else:
                self.vista.combo_pregunta2.setCurrentIndex(1)  # Segunda opción por defecto
            
            pregunta_3 = seguridad.get("pregunta_3", "¿Nombre de tu abuela?")
            index = self.vista.combo_pregunta3.findText(pregunta_3)
            if index >= 0:
                self.vista.combo_pregunta3.setCurrentIndex(index)
            else:
                self.vista.combo_pregunta3.setCurrentIndex(2)  # Tercera opción por defecto
            
            # Establecer respuestas
            self.vista.entry_respuesta1.setText(seguridad.get("respuesta_1", ""))
            self.vista.entry_respuesta2.setText(seguridad.get("respuesta_2", ""))
            self.vista.entry_respuesta3.setText(seguridad.get("respuesta_3", ""))

    
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
            "objetivos": {
                "objetivo_semanal": "5",
                "objetivo_mensual": "10",
                "objetivo_trimestral": "30",
                "objetivo_anual": "90"
            },
            "direccion": {
                "estado": "Monagas",
                "municipio": "Maturín",
                "parroquia": "San Simón",
                "institucion": "Gobernación/Institución"
            },
            "jefaturas": {
                "nombre_coordinacion": "Coordinador",
                "cedula_coordinacion": "V-123456789",
                "nombre_gobernacion": "Gobernador",
                "cedula_gobernacion": "V-12346789"
            },
            "gaceta": {
                "decreto": "Ingrese los Datos",
                "fecha_publicacion": "Ingrese la Fecha"
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
        # Objetivos
        self.vista.entry_semanal.clear()
        self.vista.entry_mensual.clear()
        self.vista.entry_trimestral.clear()
        self.vista.entry_anual.clear()
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
            
            # Cambiar color de fondo a rojo claro cuando haya un error
            palette = widget.palette()
            palette.setColor(QPalette.Base, QColor(255, 240, 240))
            widget.setPalette(palette)
            
            # Desplazar hacia el widget
            self.desplazar_error(widget, 500)

            # Enfocar el widget
            widget.setFocus()


    def desplazar_error(self, widget, duration=400):
        # ==Desplazar  hacia el error==
        try:
            # Acceder al scroll_area de la vista
            scroll_area = self.vista.scroll_area
            
            if not scroll_area or not scroll_area.isVisible():
                print(f"⚠️ ScrollArea no disponible o no visible")
                return
            
            # Obtener el scrollbar vertical
            vscroll = scroll_area.verticalScrollBar()
            
            if not vscroll or not vscroll.isVisible():
                print(f"⚠️ Scrollbar vertical no disponible")
                # Intentar método alternativo
                scroll_area.ensureWidgetVisible(widget)
                return
            
            scroll_area.ensureWidgetVisible(widget, 0, 100)
            viewport = scroll_area.viewport()
            scroll_widget = self.vista.scroll_widget

            widget_pos = widget.mapTo(viewport, widget.rect().topLeft())
            widget_y = widget_pos.y()
            
            # Calcular posición objetivo
            target_y = max(0, widget_y - 100)
            
            # Limitar al rango máximo del scrollbar
            target_y = min(target_y, vscroll.maximum())
            
            # Verificar si ya está en la posición correcta
            current_y = vscroll.value()
            
            # 3. TERCERO: Crear animación suave
            animation = QPropertyAnimation(vscroll, b"value")
            animation.setDuration(duration)
            animation.setStartValue(current_y)
            animation.setEndValue(target_y)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Conectar señales para debug
            animation.finished.connect(lambda: print(f"✅ Animación completada"))
            
            # Iniciar animación
            animation.start()
            
            # Forzar actualización inmediata
            scroll_area.repaint()
            viewport.update()
            
        except Exception as e:
            print(f"❌ Error crítico en desplazamiento: {e}")
            import traceback
            traceback.print_exc()
            
            # Último recurso: intentar método simple
            try:
                if hasattr(self.vista, 'scroll_area'):
                    self.vista.scroll_area.ensureWidgetVisible(widget)
                    print(f"🔄 Usando ensureWidgetVisible como fallback")
            except Exception as fallback_error:
                print(f"❌ Fallback también falló: {fallback_error}")
    
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
            self.vista.spin_tamano,
            self.vista.entry_respuesta1,
            self.vista.entry_respuesta2,
            self.vista.entry_respuesta3,
            self.vista.combo_pregunta1,
            self.vista.combo_pregunta2,
            self.vista.combo_pregunta3
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

    def cargar_preguntas_iniciales(self):
        """Carga las preguntas de seguridad desde la base de datos"""
        try:
            # Obtener preguntas del usuario admin
            preguntas = self.modelo.obtener_preguntas_usuario("admin")
            
            if preguntas and len(preguntas) >= 3:
                print(f"✅ Cargando preguntas: {preguntas}")
                
                # Verificar que los combos existen
                if hasattr(self.vista, 'preguntas_seguridad') and len(self.vista.preguntas_seguridad) >= 3:
                    
                    # Para cada pregunta, establecer el texto en el combo correspondiente
                    for i, texto_pregunta in enumerate(preguntas):
                        if i < len(self.vista.preguntas_seguridad):
                            combo = self.vista.preguntas_seguridad[i]
                            
                            # Buscar el índice del texto en el combo
                            index = combo.findText(texto_pregunta)
                            if index >= 0:
                                combo.setCurrentIndex(index)
                                print(f"✅ Pregunta {i+1} cargada: {texto_pregunta}")
                            else:
                                print(f"⚠️ No se encontró '{texto_pregunta}' en las opciones")
                                # Si no se encuentra, dejar el valor por defecto
                                combo.setCurrentIndex(i if i < combo.count() else 0)
                
                # También cargar las respuestas si existen
                if hasattr(self, 'cargar_respuestas_seguridad'):
                    self.cargar_respuestas_seguridad()
            else:
                print("⚠️ No se encontraron preguntas en la base de datos")
                
        except Exception as e:
            print(f"❌ Error al cargar preguntas iniciales: {e}")
            import traceback
            traceback.print_exc()

    def obtener_datos_seguridad(self):
        # Retorna una lista de diccionarios con la pregunta y respuesta de cada campo.
        datos = []
        for i in range(3):
            pregunta = self.vista.preguntas_seguridad[i].currentText()
            respuesta = self.vista.respuestas_seguridad[i].text().strip()
            datos.append({
                "pregunta": pregunta,
                "respuesta": respuesta
            })
        return datos

    def cerrar(self):
        # == Cierra conexiones== 
        self.modelo.cerrar_conexion()