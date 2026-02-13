from view.ventana_login import Ventana_login
from view.ventanas_login.ventana_setup import Ventana_setup
from view.ventanas_login.ventana_recuperar import Ventana_recuperar
from models.Modelo_login import Model_Login
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject

# Clase Principal para el Login del Sistema:
class controlador_login():
    def __init__(self):
        # Inicializar vista
        self.vista = Ventana_login()
        
        # Inicializar modelo
        try:
            self.modelo = Model_Login()
        except Exception as e:
            QMessageBox(self,"Error", f"{e}")
            raise
        
        # Usuario actual
        self.usuario_actual = None
        
        # Configurar conexiones
        self._configurar_conexiones()
    
    def _configurar_conexiones(self):
        # ==Configura conexiones entre vista y controlador==
        # Conectar botón de login
        if hasattr(self.vista, 'boton_login'):
            try:
                self.vista.boton_login.clicked.disconnect()
            except:
                pass
            self.vista.boton_login.clicked.connect(self.verificar_login)
        
        # Conectar atajo de teclado (Enter)
        if hasattr(self.vista, 'login_action'):
            try:
                self.vista.login_action.triggered.disconnect()
            except:
                pass
            self.vista.login_action.triggered.connect(self.verificar_login)

        self.vista.btn_recuperar.clicked.connect(self.solicitar_recuperacion)
    
    def verificar_login(self):
        # --Método principal para la verificación del Logueo--
        
        # Obtener las credenciales previamente adquiridas de la vista
        username = self.vista.input_usuario.text().strip()
        password = self.vista.input_password.text().strip()
        
        # Validación básica
        if not username:
            self.mostrar_error("Campo Requerido, ingrese el nombre de usuario")
            self.vista.input_usuario.setFocus()
            return
        if not password:
            self.mostrar_error("Campo Requerido, ingrese la contraseña")
            self.vista.input_password.setFocus()
            return
        if not username or not password:
            self.mostrar_error("Por favor, complete todos los campos")
            return
        if len(username) < 3:
            self.mostrar_error("El usuario debe tener al menos 3 caracteres")
            return
            
        if len(password) < 5:
            self.mostrar_error("La contraseña debe tener al menos 5 caracteres")
            return
        
        # Enviar al modelo para autenticación
        resultado, mensaje, datos_usuario = self.modelo.autenticar_usuario(username, password)
        
        if resultado:
            # Login exitoso
            self.usuario_actual = datos_usuario
            
            # Mostrar mensaje y emitir señal
            QMessageBox.information(self.vista, "Éxito", mensaje)
            self.vista.login_exitoso.emit()
        else:
            # Login fallido
            print(f"❌ {mensaje}")
            QMessageBox.critical(self.vista, "Error", mensaje)
            self.vista.input_password.clear()
            self.vista.input_password.setFocus()
    
    def mostrar_error(self, mensaje):
        # Muestra un mensaje de error
        self.vista.label_error.setText(f"⚠ {mensaje}")
        self.vista.label_error.setVisible(True)
        
        # Aplicar estilo de error a los campos
        self.vista.input_usuario.setStyleSheet(self.vista.obtener_estilo_input(True))
        self.vista.input_password.setStyleSheet(self.vista.obtener_estilo_input(True))
        
    def limpiar_error(self):
        # Limpia los mensajes de error
        self.vista.label_error.setText("")
        self.vista.label_error.setVisible(False)
        
        # Restaurar estilos originales
        self.vista.input_usuario.setStyleSheet(self.vista.obtener_estilo_input(False))
        self.vista.input_password.setStyleSheet(self.vista.obtener_estilo_input(False))

    def solicitar_recuperacion(self):
        # Esta señal debe estar definida en tu Ventana_login o el controlador
        self.vista.recuperar_login.emit()
    
    def get_widget(self):
        # Retorna el widget de login
        return self.vista
    
    def get_usuario_actual(self):
        # Obtiene usuario autenticado
        return self.usuario_actual
    
    def get_modelo(self):
        # Obtiene el modelo
        return self.modelo
    
class controlador_setup(QObject):
    def __init__(self):
        super().__init__()
        # Inicializar vista y Modelo
        self.vista = Ventana_setup()
        self.modelo = Model_Login()
        
        # Conectar botón de la vista
        self.vista.boton_registro.clicked.connect(self.procesar_registro)

        self.conexiones()

    def conexiones(self):
        self.vista.registro_action.triggered.connect(self.procesar_registro)

    def procesar_registro(self):
        self.limpiar_error()
        # == Procesar el Registro del Usuario Admin==
        # Se Obtiene los Datos de la Vista
        password = self.vista.input_password.text().strip()
        password_confirmacion = self.vista.input_password_confirmation.text().strip()
        datos_seguridad = self.obtener_datos_seguridad()
        
        # Las 3 Preguntas de Seguridad
        pregunta_1 = datos_seguridad[0]['pregunta']
        pregunta_2 = datos_seguridad[1]['pregunta']
        pregunta_3 = datos_seguridad[2]['pregunta']
        
        # Las 3 Respuestas de Seguridad
        respuesta_1 = datos_seguridad[0]['respuesta']
        respuesta_2 = datos_seguridad[1]['respuesta']
        respuesta_3 = datos_seguridad[2]['respuesta']
        
        # Validaciones
        preguntas_seleccionadas = [d['pregunta'] for d in datos_seguridad]
        if len(set(preguntas_seleccionadas)) < 3:
            self.mostrar_error("No puedes seleccionar la misma pregunta más de una vez.")
            return
        
        respuestas_ingresadas = [d['respuesta'].lower() for d in datos_seguridad if d['respuesta']]
        if len(set(respuestas_ingresadas)) < 3:
            # Solo validamos si todas están llenas, si no, saltará el error de "obligatorias"
            if len(respuestas_ingresadas) == 3:
                self.mostrar_error("Las respuestas de seguridad deben ser diferentes entre sí.")
                return

        if len(password) < 5:
            self.mostrar_error("La contraseña debe tener al menos 5 caracteres")
            return
        
        if password != password_confirmacion:
            self.mostrar_error("Las contraseñas no coinciden")
            return
        
        # Verificar que no haya respuestas vacías
        if any(not d['respuesta'] for d in datos_seguridad):
            self.mostrar_error("Todas las respuestas de seguridad son obligatorias")
            return
        
        # Guardar en DB (El usuario inicial suele ser 'admin')
        exito = self.modelo._crear_usuario_admin("admin", password, datos_seguridad)
        
        if exito:
            QMessageBox.information(self.vista, "Éxito", "Administrador registrado correctamente.")
            self.vista.registro_exitoso.emit()
        else:
            # Login fallido
            QMessageBox.critical(self.vista, "Error", "Error crítico al guardar en la base de datos")
            self.vista.input_password.setFocus()
            self.vista.input_password.clear()
            self.vista.input_password_confirmation.clear()
            

    def mostrar_error(self, mensaje):
        # Muestra un mensaje de error
        self.vista.label_error.setText(f"⚠ {mensaje}")
        self.vista.label_error.setVisible(True)
        
        # Aplicar estilo de error a los campos
        estilo_error = self.vista.obtener_estilo_input(True)
        self.vista.input_password.setStyleSheet(self.vista.obtener_estilo_input(True))
        self.vista.input_password_confirmation.setStyleSheet(self.vista.obtener_estilo_input(True))
        
        for input_seg in self.vista.inputs_seguridad:
            input_seg.setStyleSheet(estilo_error)

    def limpiar_error(self):
        # Limpia los mensajes de error
        self.vista.label_error.setText("")
        self.vista.label_error.setVisible(False)
        
        # Restaurar estilos originales
        estilo_error = self.vista.obtener_estilo_input(False)
        self.vista.input_password.setStyleSheet(self.vista.obtener_estilo_input(False))
        self.vista.input_password_confirmation.setStyleSheet(self.vista.obtener_estilo_input(False))

        for input_seg in self.vista.inputs_seguridad:
            input_seg.setStyleSheet(estilo_error)

    def obtener_datos_seguridad(self):
        # Retorna una lista de diccionarios con la pregunta y respuesta de cada campo.
        datos = []
        for i in range(3):
            pregunta = self.vista.combos_seguridad[i].currentText()
            respuesta = self.vista.inputs_seguridad[i].text().strip()
            datos.append({
                "pregunta": pregunta,
                "respuesta": respuesta
            })
        return datos
    
    def get_widget(self):
        # Retorna el widget del Setup del Login
        return self.vista
    
    def get_modelo(self):
        # Obtiene el modelo
        return self.modelo

class controlador_recuperar():
    def __init__(self):
        # Inicializar vista
        self.vista = Ventana_recuperar()
        self.modelo = Model_Login()
        
        # Usuario actual
        self.usuario_actual = "admin"

        self.cargar_preguntas_iniciales()
        self.vista.boton_recuperar.clicked.connect(self.gestionar_boton_principal)

    def cargar_preguntas_iniciales(self):
        preguntas = self.modelo.obtener_preguntas_usuario(self.usuario_actual)
        if preguntas:
            for i, texto_pregunta in enumerate(preguntas):
                self.vista.combos_seguridad[i].clear()
                self.vista.combos_seguridad[i].addItem(texto_pregunta)
                self.vista.combos_seguridad[i].setEnabled(False) # No editable

    def gestionar_boton_principal(self):
        # Si los campos de password no son visibles, primero validamos preguntas
        if not self.vista.input_nueva_pass.isVisible():
            respuestas = [inp.text() for inp in self.vista.inputs_seguridad]
            if self.modelo.validar_respuestas_sistema(self.usuario_actual, respuestas):
                self.vista.toggle_campos_password(True)
                self.vista.boton_recuperar.setText("Cambiar Contraseña")
            else:
                QMessageBox.warning(self.vista, "Error", "Las respuestas no coinciden.")
        else:
            # Si ya son visibles, procedemos a cambiar la contraseña
            pass1 = self.vista.input_nueva_pass.text()
            pass2 = self.vista.input_conf_pass.text()
            
            if pass1 == pass2 and len(pass1) > 0:
                if self.modelo.actualizar_password(self.usuario_actual, pass1):
                    QMessageBox.information(self.vista, "Éxito", "Contraseña actualizada.")
                    self.vista.recuperacion_exitoso.emit() # Regresa al login
            else:
                QMessageBox.warning(self.vista, "Error", "Las contraseñas no coinciden.")

    

    def get_widget(self):
        # Retorna el widget del Setup de Recuperar Contraseña
        return self.vista
    
    def get_modelo(self):
        # Obtiene el modelo
        return self.modelo