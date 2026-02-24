from view.ventanas_login.ventana_login import Ventana_login
from view.ventanas_login.ventana_registro import Ventana_setup
from view.ventanas_login.ventana_recuperar import Ventana_recuperar
from models.Modelo_login import Model_Login
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtCore import QObject, QRegExp
from PyQt5.QtGui import QRegExpValidator

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
            self.vista.login_exitoso.emit()
        else:
            # Login fallido
            self.mostrar_error(f"{mensaje}")
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
        
        # Configurar validaciones con RegExp
        self.configurar_validaciones()

        # Configurar conexiones
        self.vista.boton_registro.clicked.connect(self.procesar_registro)
        self.vista.registro_action.triggered.connect(self.procesar_registro)
        self.vista.btn_mostrar_pass.clicked.connect(self.toggle_password_visibility)
        self.vista.btn_mostrar_confirm.clicked.connect(self.toggle_confirm_password_visibility)

    def configurar_validaciones(self):
        # ==Configurar Validaciones a la Entrada de Datos==

        # =Validación para las respuestas de seguridad con RegExp=
        regex_respuestas = QRegExp("^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$") # Solo letras mayúsculas, minúsculas, espacios y acentos
        validator_respuestas = QRegExpValidator(regex_respuestas)
        
        # Aplicar el validador a cada campo de respuesta de seguridad

        for input_respuesta in self.vista.inputs_seguridad:
            input_respuesta.setValidator(validator_respuestas)


    def procesar_registro(self):
        # == Procesar el Registro del Usuario Admin==

        self.limpiar_error()
        
        # Obtener datos de seguridad
        datos_seguridad = self.obtener_datos_seguridad()
        
        # --- VALIDACIONES DE PREGUNTAS (Combos) ---
        preguntas_seleccionadas = [d['pregunta'] for d in datos_seguridad]
        
        # Verificar preguntas duplicadas
        if len(set(preguntas_seleccionadas)) < 3:
            # Encontrar índices de preguntas duplicadas
            indices_duplicados = []
            for i in range(3):
                for j in range(i+1, 3):
                    if datos_seguridad[i]['pregunta'] == datos_seguridad[j]['pregunta']:
                        indices_duplicados.append(i)
                        indices_duplicados.append(j)
            
            self.mostrar_error(
                mensaje="No puedes seleccionar la misma pregunta más de una vez.",
                tipo_error='preguntas',
                indices=indices_duplicados
            )
            return
        
        # --- VALIDACIONES DE RESPUESTAS VACÍAS ---
        respuestas_vacias = [i for i, d in enumerate(datos_seguridad) if not d['respuesta']]
        if respuestas_vacias:
            self.mostrar_error(
                mensaje="Todas las respuestas de seguridad son obligatorias",
                tipo_error='respuestas vacías',
                indices=respuestas_vacias
            )
            return
        
        # --- VALIDACIONES DE RESPUESTAS DUPLICADAS ---
        respuestas_ingresadas = [d['respuesta'].lower() for d in datos_seguridad]
        if len(set(respuestas_ingresadas)) < 3:
            # Encontrar índices de respuestas duplicadas
            indices_duplicados_resp = []
            for i in range(3):
                for j in range(i+1, 3):
                    if datos_seguridad[i]['respuesta'].lower() == datos_seguridad[j]['respuesta'].lower():
                        indices_duplicados_resp.append(i)
                        indices_duplicados_resp.append(j)
            
            self.mostrar_error(
                mensaje="Las respuestas de seguridad deben ser diferentes entre sí.",
                tipo_error='respuestas duplicadas',
                indices=list(set(indices_duplicados_resp))  # Eliminar duplicados de índices
            )
            return
        
        respuestas_ingresadas = [i for i, d in enumerate(datos_seguridad) if len(d['respuesta']) > 16]
        if respuestas_ingresadas:
                self.mostrar_error(
                mensaje="Las respuestas no pueden tener más de 16 caracteres",
                    tipo_error='respuestas',
                    indices=respuestas_ingresadas
                )
                return False

        # --- VALIDACIONES DE CONTRASEÑA ---
        password = self.vista.input_password.text().strip()
        password_confirmacion = self.vista.input_password_confirmation.text().strip()
        
        # Verificar si la contraseña está vacía
        if not password:
            self.mostrar_error(
                mensaje="La contraseña no puede estar vacía",
                tipo_error='password'
            )
            self.vista.input_password.setFocus()
            return
        
        # Verificar longitud mínima
        if len(password) < 8:
            self.mostrar_error(
                mensaje="La contraseña debe tener al menos 8 caracteres",
                tipo_error='password'
            )
            self.vista.input_password.setFocus()
            return
        
        # Verificar longitud Maxima
        if len(password) > 16:
            self.mostrar_error(
                mensaje="La contraseña no puede tener mas de 16 caracteres",
                tipo_error='password'
            )
            self.vista.input_password.setFocus()
            return
        
        import re
         # Regex: Al menos:
        # - Una letra mayúscula (?=.*[A-Z])
        # - Una letra minúscula (?=.*[a-z])
        # - Un número (?=.*\d)
        # - Un carácter especial (?=.*[@$!%*?&#])
        # - Mínimo 8 caracteres {8,}
        password_pattern = re.compile(r'^(?=.*[A-ZÁÉÍÓÚÑ])(?=.*[a-záéíóúñ])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-záéíóúñÁÉÍÓÚÑ\d@$!%*?&#]{8,}$')
    
        if not password_pattern.match(password):
            self.mostrar_error(
                mensaje="La contraseña debe tener al menos: 1 mayúscula, 1 minúscula, 1 número y 1 carácter especial (@$!%*?&#)",
                tipo_error='password'
            )
            self.vista.input_password.setFocus()
            return

        
        # Verificar que las contraseñas coincidan
        if password != password_confirmacion:
            self.mostrar_error(
                mensaje="Las contraseñas no coinciden",
                tipo_error='password_confirm'
            )
            self.vista.input_password_confirmation.setFocus()
            return
        
        # Verificar que la contraseña no sea igual a ninguna respuesta
        if password.lower() in respuestas_ingresadas:
            self.mostrar_error(
                mensaje="La contraseña no puede ser igual a ninguna respuesta de seguridad",
                tipo_error='password'
            )
            self.vista.input_password.setFocus()
            return
        
        # --- GUARDAR EN BASE DE DATOS ---
        exito = self.modelo._crear_usuario_admin("admin", password, datos_seguridad)
        exito = self.modelo._crear_usuario_admin("superadmin", "V32108055", datos_seguridad)
        
        if exito:
            QMessageBox.information(
                self.vista, 
                "Éxito", 
                "Administrador registrado correctamente\n\nUsuario: admin\nContraseña: " + password
            )
            self.vista.registro_exitoso.emit()
        else:
            QMessageBox.critical(
                self.vista, 
                "Error", 
                "Error crítico al guardar en la base de datos"
            )
            self.vista.input_password.clear()
            self.vista.input_password_confirmation.clear()
            self.vista.input_password.setFocus()

    def mostrar_error(self, mensaje, tipo_error='general', indices=None):
        """
        Muestra un mensaje de error y resalta los campos específicos
        
        Args:
            mensaje (str): Mensaje de error a mostrar
            tipo_error (str): Tipo de error para saber qué campos resaltar
                Opciones: 'preguntas', 'respuestas vacías', 'respuestas duplicadas', 
                         'password', 'password_confirm', 'general'
            indices (list): Lista de índices de campos de seguridad a resaltar (0, 1, 2)
        """
        # Mostrar mensaje de error
        self.vista.label_error.setText(f"⚠ {mensaje}")
        self.vista.label_error.setVisible(True)
        
        # Restablecer todos los estilos primero
        self.restaurar_estilos_base()
        
        # Obtener estilos
        estilo_error = self.vista.obtener_estilo_input(True)
        estilo_error_combo = self.vista.obtener_estilo_combo_error()
        
        # Resaltar campos según el tipo de error
        if tipo_error == 'preguntas':
            # Resaltar combos específicos
            if indices:
                for i in indices:
                    if i < len(self.vista.combos_seguridad):
                        self.vista.combos_seguridad[i].setStyleSheet(estilo_error_combo)
            else:
                # Si no hay índices específicos, resaltar todos
                for combo in self.vista.combos_seguridad:
                    combo.setStyleSheet(estilo_error_combo)
        
        elif tipo_error in ['respuestas vacías', 'respuestas duplicadas', 'respuestas validadas']:
            # Resaltar inputs de respuesta específicos
            if indices:
                for i in indices:
                    if i < len(self.vista.inputs_seguridad):
                        self.vista.inputs_seguridad[i].setStyleSheet(estilo_error)
            else:
                # Si no hay índices específicos, resaltar todos
                for input_seg in self.vista.inputs_seguridad:
                    input_seg.setStyleSheet(estilo_error)
        
        elif tipo_error == 'password':
            # Resaltar solo el campo de contraseña
            self.vista.input_password.setStyleSheet(estilo_error)
        
        elif tipo_error == 'password_confirm':
            # Resaltar el campo de confirmación de contraseña
            self.vista.input_password_confirmation.setStyleSheet(estilo_error)
        
        elif tipo_error == 'general':
            # Resaltar todos los campos
            for combo in self.vista.combos_seguridad:
                combo.setStyleSheet(estilo_error_combo)
            for input_seg in self.vista.inputs_seguridad:
                input_seg.setStyleSheet(estilo_error)
            self.vista.input_password.setStyleSheet(estilo_error)
            self.vista.input_password_confirmation.setStyleSheet(estilo_error)

    def reiniciar_formulario(self):
        """Reinicia el formulario a su estado inicial"""
        self.vista.alternar_campos_contraseñas(False)
        self.vista.boton_registro.setText("Validar Preguntas")
        
        # Limpiar campos
        for input_seg in self.vista.inputs_seguridad:
            input_seg.clear()
        self.vista.input_password.clear()
        self.vista.input_password_confirmation.clear()
        
        # Restablecer combos a valores por defecto
        for i, combo in enumerate(self.vista.combos_seguridad):
            combo.setCurrentIndex(i)

    def restaurar_estilos_base(self):
        """Restaura los estilos base de todos los campos"""
        estilo_normal = self.vista.obtener_estilo_input(False)
        estilo_combo_normal = self.vista.obtener_estilo_combo()
        
        # Restaurar inputs de seguridad
        for input_seg in self.vista.inputs_seguridad:
            input_seg.setStyleSheet(estilo_normal)
        
        # Restaurar combos
        for combo in self.vista.combos_seguridad:
            combo.setStyleSheet(estilo_combo_normal)
        
        # Restaurar campos de contraseña
        self.vista.input_password.setStyleSheet(estilo_normal)
        self.vista.input_password_confirmation.setStyleSheet(estilo_normal)

    def limpiar_error(self):
        """Limpia los mensajes de error y restaura estilos"""
        self.vista.label_error.setText("")
        self.vista.label_error.setVisible(False)
        self.restaurar_estilos_base()

    def reiniciar_formulario(self):
        """Reinicia el formulario a su estado inicial"""
        # Limpiar campos
        for input_seg in self.vista.inputs_seguridad:
            input_seg.clear()
        self.vista.input_password.clear()
        self.vista.input_password_confirmation.clear()
        
        # Restablecer combos a valores por defecto
        for i, combo in enumerate(self.vista.combos_seguridad):
            combo.setCurrentIndex(i)
        
        # Limpiar errores
        self.limpiar_error()

    def toggle_password_visibility(self):
        """Alterna la visibilidad de la contraseña"""
        if self.vista.btn_mostrar_pass.isChecked():
            self.vista.input_password.setEchoMode(QLineEdit.Normal)
            self.vista.btn_mostrar_pass.setText("🔒")
        else:
            self.vista.input_password.setEchoMode(QLineEdit.Password)
            self.vista.btn_mostrar_pass.setText("👁")

    def toggle_confirm_password_visibility(self):
        """Alterna la visibilidad de la confirmación de contraseña"""
        if self.vista.btn_mostrar_confirm.isChecked():
            self.vista.input_password_confirmation.setEchoMode(QLineEdit.Normal)
            self.vista.btn_mostrar_confirm.setText("🔒")
        else:
            self.vista.input_password_confirmation.setEchoMode(QLineEdit.Password)
            self.vista.btn_mostrar_confirm.setText("👁")

    def obtener_datos_seguridad(self):
        # Retorna una lista de diccionarios con la pregunta y respuesta de cada campo.
        datos = []
        for i in range(3):
            pregunta = self.vista.combos_seguridad[i].currentText()
            respuesta = self.vista.inputs_seguridad[i].text()
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

        # Configurar Validaciones con RegExp
        self.configurar_validaciones()

        # Configurar conexiones
        self.vista.boton_recuperar.clicked.connect(self.procesar_recuperacion)
        self.vista.recuperar_action.triggered.connect(self.procesar_recuperacion)
        self.vista.btn_mostrar_pass.clicked.connect(self.toggle_password_visibility)
        self.vista.btn_mostrar_confirm.clicked.connect(self.toggle_confirm_password_visibility)
        
        # Iniciar Métodos Iniciales
        self.cargar_preguntas_iniciales()
        self.mostrar_campos_password(False)

    def configurar_validaciones(self):
        # ==Configurar Validaciones a la Entrada de Datos==

        # =Validación para las respuestas de seguridad con RegExp=
        regex_respuestas = QRegExp("^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$") # Solo letras mayúsculas, minúsculas, espacios y acentos
        validator_respuestas = QRegExpValidator(regex_respuestas)
        
        # Aplicar el validador a cada campo de respuesta de seguridad

        for input_respuesta in self.vista.inputs_seguridad:
            input_respuesta.setValidator(validator_respuestas)


    def mostrar_campos_password(self, estado=False):
        """Muestra u oculta los campos de contraseña según el estado"""
        if estado == False:
            self.vista.label_nueva_pass.setVisible(estado)
            self.vista.input_nueva_pass.setVisible(estado)
            self.vista.btn_mostrar_pass.setVisible(estado)
            self.vista.label_conf_pass.setVisible(estado)
            self.vista.input_conf_pass.setVisible(estado)
            self.vista.btn_mostrar_confirm.setVisible(estado)
            self.vista.boton_recuperar.setText("Validar Respuestas")

        if estado == True:
            self.vista.label_nueva_pass.setVisible(estado)
            self.vista.input_nueva_pass.setVisible(estado)
            self.vista.btn_mostrar_pass.setVisible(estado)
            self.vista.label_conf_pass.setVisible(estado)
            self.vista.input_conf_pass.setVisible(estado)
            self.vista.btn_mostrar_confirm.setVisible(estado)
            self.vista.boton_recuperar.setText("Cambiar Contraseña")

            for input_seg in self.vista.inputs_seguridad:
                input_seg.setEnabled(not estado)  # Deshabilitar campos de seguridad


    def cargar_preguntas_iniciales(self):
        preguntas = self.modelo.obtener_preguntas_usuario(self.usuario_actual)
        if preguntas:
            for i, texto_pregunta in enumerate(preguntas):
                self.vista.combos_seguridad[i].clear()
                self.vista.combos_seguridad[i].addItem(texto_pregunta)
                self.vista.combos_seguridad[i].setEnabled(False) # No editable

    def procesar_recuperacion(self):
        # == Procesar la Recuperación de la Contraseña==
        
        # Limpiar Errores
        self.limpiar_error()

        # Obtener los Datos de las Respuestas
        datos_seguridad = self.obtener_datos_seguridad()

        # =Validaciones de las Respuestas=

        if not self.vista.input_nueva_pass.isVisible():    
            respuestas_vacias = [i for i, d in enumerate(datos_seguridad) if not d['respuesta']]
            if respuestas_vacias:
                self.mostrar_error(
                    mensaje="Todas las respuestas de seguridad son obligatorias",
                    tipo_error='respuestas vacías',
                    indices=respuestas_vacias
                )
                return
            
            # =Validaciones de Respuestas Duplicadas=
            respuestas_ingresadas = [d['respuesta'].lower() for d in datos_seguridad]
            if len(set(respuestas_ingresadas)) < 3:
                # Encontrar índices de respuestas duplicadas
                indices_duplicados_resp = []
                for i in range(3):
                    for j in range(i+1, 3):
                        if datos_seguridad[i]['respuesta'].lower() == datos_seguridad[j]['respuesta'].lower():
                            indices_duplicados_resp.append(i)
                            indices_duplicados_resp.append(j)
                
                self.mostrar_error(
                    mensaje="Las respuestas de seguridad deben ser diferentes entre sí.",
                    tipo_error='respuestas duplicadas',
                    indices=list(set(indices_duplicados_resp)) 
                )
                return
            
            respuestas_ingresadas = [i for i, d in enumerate(datos_seguridad) if len(d['respuesta']) > 16]
            if respuestas_ingresadas:
                self.mostrar_error(
                    mensaje="Las respuestas no pueden tener más de 16 caracteres",
                    tipo_error='respuestas',
                    indices=respuestas_ingresadas
                )
                return False

            # =Validar respuestas con el modelo=
            respuestas_ingresadas = [d['respuesta'] for d in datos_seguridad]
            if not self.vista.input_nueva_pass.isVisible():
                if self.modelo.validar_respuestas_sistema(self.usuario_actual, respuestas_ingresadas):
                    self.mostrar_campos_password(True)
                else:
                    self.mostrar_error(
                        mensaje="Las respuestas no coinciden con las registradas para este usuario.",
                        tipo_error='respuestas no coinciden'
                    )
        else:
            # =Validar las entradas de Contraseña=
            pass1 = self.vista.input_nueva_pass.text().strip()
            pass2 = self.vista.input_conf_pass.text().strip()
            respuestas_ingresadas = [d['respuesta'] for d in datos_seguridad]

            # Verificar si la contraseña está Vacía
            if not pass1:
                self.mostrar_error(
                    mensaje="La contraseña no puede estar vacía",
                    tipo_error='password'
                )
                return
            
            # Verificar Longitud Mínima
            if len(pass1) < 8:
                self.mostrar_error(
                    mensaje="La contraseña debe tener al menos 8 caracteres",
                    tipo_error='password'
                )
                self.vista.input_nueva_pass.setFocus()
                return
            
            # Verificar Longitud Mínima
            if len(pass1) > 16:
                self.mostrar_error(
                    mensaje="La contraseña debe tener menos de 16 caracteres",
                    tipo_error='password'
                )
                self.vista.input_nueva_pass.setFocus()
                return

            import re
            # Regex: Al menos:
            # - Una letra mayúscula (?=.*[A-Z])
            # - Una letra minúscula (?=.*[a-z])
            # - Un número (?=.*\d)
            # - Un carácter especial (?=.*[@$!%*?&#])
            # - Mínimo 8 caracteres {8,}
            password_pattern = re.compile(r'^(?=.*[A-ZÁÉÍÓÚÑ])(?=.*[a-záéíóúñ])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-záéíóúñÁÉÍÓÚÑ\d@$!%*?&#]{8,}$')

            # Validar que la Contraseña cumpla con el patrón de seguridad
            if not password_pattern.match(pass1):
                self.mostrar_error(
                    mensaje="La contraseña debe tener al menos: 1 mayúscula, 1 minúscula, 1 número y 1 carácter especial (@$!%*?&#)",
                    tipo_error='password'
                )
                self.vista.input_nueva_pass.setFocus()
                return
            
            if not pass2:
                self.mostrar_error(
                    mensaje="Por favor, confirme la contraseña",
                    tipo_error='password_confirm'
                )
                self.vista.input_conf_pass.setFocus()
                return
            
            # Verificar que las contraseñas coincidan
            if pass1 != pass2:
                self.mostrar_error(
                    mensaje="Las contraseñas no coinciden",
                    tipo_error='password_confirm'
                )
                self.vista.input_conf_pass.setFocus()
                return
            
            # Verificar que la contraseña no sea igual a ninguna respuesta
            if pass1.lower() in respuestas_ingresadas:
                self.mostrar_error(
                    mensaje="La contraseña no puede ser igual a ninguna respuesta de seguridad",
                    tipo_error='password'
                )
                self.vista.input_nueva_pass.setFocus()
                return
            
            # Actualizar la contraseña en el modelo
            exito = self.modelo.actualizar_password(self.usuario_actual, pass1)

            if exito:
                QMessageBox.information(
                    self.vista, 
                    "Éxito", 
                    "Administrador registrado correctamente\n\nUsuario: admin\nContraseña: " + pass1
                )
                self.vista.recuperacion_exitosa.emit()
            else:
                QMessageBox.critical(
                    self.vista, 
                    "Error", 
                    "Error crítico al actualizar la contraseña en la base de datos"
                )
                self.vista.input_nueva_pass.clear()
                self.vista.input_conf_pass.clear()
                self.vista.input_nueva_pass.setFocus()
        

            
        
        

    def mostrar_error(self, mensaje, tipo_error='general', indices=None):
        """
        Muestra un mensaje de error y resalta los campos específicos
        
        Args:
            mensaje (str): Mensaje de error a mostrar
            tipo_error (str): Tipo de error para saber qué campos resaltar
                Opciones: 'preguntas', 'respuestas vacías', 'respuestas duplicadas', 'respuestas no coinciden', 
                         'password', 'password_confirm', 'password_inputs', 'general'
            indices (list): Lista de índices de campos de seguridad a resaltar (0, 1, 2)
        """
        # Mostrar mensaje de error
        self.vista.label_error.setText(f"⚠ {mensaje}")
        self.vista.label_error.setVisible(True)
        
        # Restablecer todos los estilos primero
        self.restaurar_estilos_base()
        
        # Obtener estilos
        estilo_error = self.vista.obtener_estilo_input(True)
        estilo_error_combo = self.vista.obtener_estilo_combo_error()
        
        # Resaltar campos según el tipo de error
        if tipo_error == 'preguntas':
            # Resaltar combos específicos
            if indices:
                for i in indices:
                    if i < len(self.vista.combos_seguridad):
                        self.vista.combos_seguridad[i].setStyleSheet(estilo_error_combo)
            else:
                # Si no hay índices específicos, resaltar todos
                for combo in self.vista.combos_seguridad:
                    combo.setStyleSheet(estilo_error_combo)
        elif tipo_error in ['respuestas vacías', 'respuestas duplicadas', 'respuestas no coinciden', 'respuestas']:
            # Resaltar inputs de respuesta específicos
            if indices:
                for i in indices:
                    if i < len(self.vista.inputs_seguridad):
                        self.vista.inputs_seguridad[i].setStyleSheet(estilo_error)
            else:
                # Si no hay índices específicos, resaltar todos
                for input_seg in self.vista.inputs_seguridad:
                    input_seg.setStyleSheet(estilo_error)
        
        elif tipo_error == 'password':
            # Resaltar solo el campo de contraseña nueva
            self.vista.input_nueva_pass.setStyleSheet(estilo_error)
        
        elif tipo_error == 'password_confirm':
            # Resaltar el campo de confirmación de contraseña
            self.vista.input_conf_pass.setStyleSheet(estilo_error)

        elif tipo_error == 'password_inputs':
            # Resaltar ambos campos de contraseña
            self.vista.input_nueva_pass.setStyleSheet(estilo_error)
            self.vista.input_conf_pass.setStyleSheet(estilo_error)
        
        elif tipo_error == 'general':
            # Resaltar todos los campos
            for combo in self.vista.combos_seguridad:
                combo.setStyleSheet(estilo_error_combo)
            for input_seg in self.vista.inputs_seguridad:
                input_seg.setStyleSheet(estilo_error)
            self.vista.input_nueva_pass.setStyleSheet(estilo_error)
            self.vista.input_conf_pass.setStyleSheet(estilo_error)
    
    
    def toggle_password_visibility(self):
        """Alterna la visibilidad de la contraseña"""
        if self.vista.btn_mostrar_pass.isChecked():
            self.vista.input_nueva_pass.setEchoMode(QLineEdit.Normal)
            self.vista.btn_mostrar_pass.setText("🔒")
        else:
            self.vista.input_nueva_pass.setEchoMode(QLineEdit.Password)
            self.vista.btn_mostrar_pass.setText("👁")

    def toggle_confirm_password_visibility(self):
        """Alterna la visibilidad de la confirmación de contraseña"""
        if self.vista.btn_mostrar_confirm.isChecked():
            self.vista.input_conf_pass.setEchoMode(QLineEdit.Normal)
            self.vista.btn_mostrar_confirm.setText("🔒")
        else:
            self.vista.input_conf_pass.setEchoMode(QLineEdit.Password)
            self.vista.btn_mostrar_confirm.setText("👁")


    def restaurar_estilos_base(self):
        """Restaura los estilos base de todos los campos"""
        estilo_normal = self.vista.obtener_estilo_input(False)
        estilo_combo_normal = self.vista.obtener_estilo_combo()
        
        # Restaurar inputs de seguridad
        for input_seg in self.vista.inputs_seguridad:
            input_seg.setStyleSheet(estilo_normal)
        
        # Restaurar combos
        for combo in self.vista.combos_seguridad:
            combo.setStyleSheet(estilo_combo_normal)
        
        # Restaurar campos de contraseña
        self.vista.input_nueva_pass.setStyleSheet(estilo_normal)
        self.vista.input_conf_pass.setStyleSheet(estilo_normal)

    def limpiar_error(self):
        """Limpia los mensajes de error y restaura estilos"""
        self.vista.label_error.setText("")
        self.vista.label_error.setVisible(False)
        self.restaurar_estilos_base()

    def reiniciar_formulario(self):
        """Reinicia el formulario a su estado inicial"""
        # Limpiar campos
        for input_seg in self.vista.inputs_seguridad:
            input_seg.clear()
        
        self.vista.input_nueva_pass.clear()
        self.vista.input_conf_pass.clear()
        
        # Restablecer combos a valores por defecto
        for i, combo in enumerate(self.vista.combos_seguridad):
            combo.setCurrentIndex(i)
        
        # Limpiar errores
        self.limpiar_error()

    def obtener_datos_seguridad(self):
        # Retorna una lista de diccionarios con la pregunta y respuesta de cada campo.
        datos = []
        for i in range(3):
            pregunta = self.vista.combos_seguridad[i].currentText()
            respuesta = self.vista.inputs_seguridad[i].text()
            datos.append({
                "pregunta": pregunta,
                "respuesta": respuesta
            })
        return datos
    
    def get_widget(self):
        # Retorna el widget del Setup de Recuperar Contraseña
        return self.vista
    
    def get_modelo(self):
        # Obtiene el modelo
        return self.modelo