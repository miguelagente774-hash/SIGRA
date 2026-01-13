import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from view.vista_configuracion import Ventana_configuracion
from models.Modelo_configuracion import Model_Configuraciones

class controlador_configuraciones(QWidget):
    """Controlador que maneja TODA la lógica de configuraciones"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar modelo y vista
        self.modelo = Model_Configuraciones()
        self.vista = Ventana_configuracion()
        
        # Configurar layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.vista)
        
        # Conectar señales
        self.vista.guardar_clicked.connect(self.on_guardar_clicked)
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
    
    def cargar_datos_iniciales(self):
        """Carga los datos desde la base de datos al iniciar"""
        try:
            # Obtener datos del modelo
            datos_interfaz = self.modelo.cargar_configuracion_interfaz()
            datos_direccion = self.modelo.cargar_datos_direccion()
            datos_jefaturas = self.modelo.cargar_datos_jefaturas()
            
            # Preparar datos para la vista
            datos = {
                "interfaz": datos_interfaz,
                "direccion": datos_direccion,
                "jefaturas": datos_jefaturas
            }
            
            # Establecer en vista
            self.establecer_valores(datos)
            
            print("✅ Datos cargados desde la base de datos")
            
        except Exception as e:
            print(f"❌ Error al cargar datos iniciales: {e}")
            self.mostrar_mensaje("Error", f"No se pudieron cargar los datos: {str(e)}", "error")
    
    def on_guardar_clicked(self):
        """Maneja el evento de clic en guardar"""
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
            
            # 5. Mostrar resultado
            if exito:
                self.mostrar_mensaje("Éxito", "Los cambios se guardaron correctamente", "success")
            else:
                self.mostrar_mensaje("Error", "No se pudieron guardar los cambios", "error")
                
        except Exception as e:
            print(f"❌ Error en on_guardar_clicked: {e}")
            self.mostrar_mensaje("Error", f"Ocurrió un error: {str(e)}", "error")
    
    def validar_datos(self, datos):
        """Valida todos los datos antes de guardar"""
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
        
        return True
    
    def validar_interfaz(self, datos_interfaz):
        """Valida datos de interfaz"""
        # Validar tema
        tema = datos_interfaz.get("tema", "").lower()
        if tema not in ["claro", "oscuro"]:
            self.vista.mostrar_error("tema", "Seleccione un tema válido")
            return False
        
        # Validar fuente
        fuente = datos_interfaz.get("fuente", "").strip()
        if len(fuente) < 3:
            self.vista.mostrar_error("fuente", "La fuente es requerida")
            return False
        
        # Validar tamaño
        tamaño = datos_interfaz.get("tamaño", 0)
        if not (8 <= tamaño <= 24):
            self.vista.mostrar_error("tamaño", "Tamaño debe estar entre 8 y 24")
            return False
        
        return True
    
    def validar_direccion(self, datos_direccion):
        """Valida datos de dirección"""
        campos = [
            ("estado", "Estado"),
            ("municipio", "Municipio"),
            ("parroquia", "Parroquia"),
            ("institucion", "Institución")
        ]
        
        for campo_key, campo_nombre in campos:
            valor = datos_direccion.get(campo_key, "").strip()
            
            # Validar requerido
            if not valor:
                self.vista.mostrar_error(campo_key, f"{campo_nombre} es requerido")
                return False
            
            # Validar longitud mínima
            if len(valor) < 3:
                self.vista.mostrar_error(campo_key, f"{campo_nombre} debe tener al menos 3 caracteres")
                return False
            
            # Validar solo letras y espacios
            if not all(c.isalpha() or c.isspace() or c in ".-()" for c in valor):
                self.vista.mostrar_error(campo_key, f"{campo_nombre} contiene caracteres inválidos")
                return False
        
        return True
    
    def validar_jefaturas(self, datos_jefaturas):
        """Valida datos de jefaturas"""
        # Validar nombres
        nombres = [
            ("nombre_coordinacion", "Nombre de Coordinación"),
            ("nombre_gobernacion", "Nombre de Gobernación")
        ]
        
        for campo_key, campo_nombre in nombres:
            valor = datos_jefaturas.get(campo_key, "").strip()
            
            if not valor or len(valor) < 5:
                self.vista.mostrar_error(campo_key, f"{campo_nombre} es requerido (mínimo 5 caracteres)")
                return False
        
        # Validar cédulas
        cedulas = [
            ("cedula_coordinacion", "Cédula de Coordinación"),
            ("cedula_gobernacion", "Cédula de Gobernación")
        ]
        
        for campo_key, campo_nombre in cedulas:
            valor = datos_jefaturas.get(campo_key, "").strip()
            
            if not self.modelo.validar_cedula(valor):
                self.vista.mostrar_error(campo_key, f"{campo_nombre} inválida. Formato: V-12345678")
                return False
        
        return True
    
    def preparar_datos_para_guardar(self, datos_crudos):
        """Prepara y limpia los datos para guardar en BD"""
        return {
            "interfaz": {
                "tema": datos_crudos["interfaz"]["tema"],
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
                "cedula_coordinacion": datos_crudos["jefaturas"]["cedula_coordinacion"].strip(),
                "nombre_gobernacion": datos_crudos["jefaturas"]["nombre_gobernacion"].strip(),
                "cedula_gobernacion": datos_crudos["jefaturas"]["cedula_gobernacion"].strip()
            }
        }
    
    def guardar_en_bd(self, datos):
        """Guarda los datos en la base de datos"""
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
            
            return exito_interfaz and exito_direccion and exito_jefaturas
            
        except Exception as e:
            print(f"❌ Error al guardar en BD: {e}")
            return False
    
    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """Muestra un mensaje al usuario"""
        if tipo == "error":
            QMessageBox.critical(self, titulo, mensaje)
        elif tipo == "warning":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "success":
            QMessageBox.information(self, titulo, mensaje)
        else:
            QMessageBox.information(self, titulo, mensaje)
    
    # ========== MÉTODOS PÚBLICOS ==========

    

    def obtener_valores(self):
        # Retorna todos los valores actuales a los widgets
        return {
            "interfaz": {
                "tema": "Claro" if self.vista.radio_tema_claro.isChecked() else "Oscuro",
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
            }
        }
    
    

    def establecer_valores(self, datos):
        # -Establece los Valores de la Interfaz-
        # Interfaz
        if datos.get("interfaz"):
            interfaz = datos["interfaz"]
            if interfaz.get("tema") == "Claro":
                self.vista.radio_tema_claro.setChecked(True)
            else:
                self.vista.radio_tema_oscuro.setChecked(True)
            
            index = self.vista.combo_fuente.findText(interfaz.get("fuente", "Arial"))
            if index >= 0:
                self.vista.combo_fuente.setCurrentIndex(index)
            
            self.vista.spin_tamano.setValue(interfaz.get("tamaño", 12))
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
            self.vista.entry_nombre_coord.setText(jefaturas.get("nombre_coordinacion", ""))
            self.vista.entry_cedula_coord.setText(jefaturas.get("cedula_coordinacion", ""))
            self.vista.entry_nombre_gob.setText(jefaturas.get("nombre_gobernacion", ""))
            self.vista.entry_cedula_gob.setText(jefaturas.get("cedula_gobernacion", ""))
    
    def get_widget(self):
        """Retorna el widget para integrar en la aplicación"""
        return self
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.limpiar_campos()
    
    def cargar_datos_por_defecto(self):
        """Carga valores por defecto"""
        datos_default = {
            "interfaz": {
                "tema": "Claro",
                "fuente": "Arial",
                "tamaño": 12,
                "negrita": False
            },
            "direccion": {
                "estado": "",
                "municipio": "",
                "parroquia": "",
                "institucion": ""
            },
            "jefaturas": {
                "nombre_coordinacion": "",
                "cedula_coordinacion": "",
                "nombre_gobernacion": "",
                "cedula_gobernacion": ""
            }
        }
        self.establecer_valores(datos_default)
    

    def limpiar_campos(self):
        """Limpia todos los campos"""
        self.vista.radio_tema_claro.setChecked(True)
        self.vista.combo_fuente.setCurrentIndex(0)
        self.vista.spin_tamano.setValue(12)
        self.vista.check_negrita.setChecked(False)
        
        self.vista.entry_estado.clear()
        self.vista.entry_municipio.clear()
        self.vista.entry_parroquia.clear()
        self.vista.entry_institucion.clear()
        
        self.vista.entry_nombre_coord.clear()
        self.vista.entry_cedula_coord.clear()
        self.vista.entry_nombre_gob.clear()
        self.vista.entry_cedula_gob.clear()
    

    def mostrar_error(self, campo, mensaje):
        """Marca un campo con error"""
        # Puedes implementar marcado visual de errores aquí
        print(f"Error en {campo}: {mensaje}")
    
    def limpiar_errores(self):
        """Limpia todos los marcadores de error"""
        pass

    def cerrar(self):
        """Cierra conexiones"""
        self.modelo.cerrar_conexion()
