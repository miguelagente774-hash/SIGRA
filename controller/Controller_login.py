from view.ventana_login import Ventana_login
from models.Modelo_login import Model_Login
from PyQt5.QtWidgets import QMessageBox

class controlador_login():
    # Controlador simplificado para la estructura básica de Usuario.

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
    
    def get_widget(self):
        # Retorna el widget de login
        return self.vista
    
    def get_usuario_actual(self):
        # Obtiene usuario autenticado
        return self.usuario_actual
    
    def get_modelo(self):
        # Obtiene el modelo
        return self.modelo