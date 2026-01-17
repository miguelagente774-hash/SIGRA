from view.ventana_login import Ventana_login
from models.Modelo_login import Model_Login
from PyQt5.QtWidgets import QMessageBox

class controlador_login():
    # Controlador simplificado para la estructura básica de Usuario.

    def __init__(self):
        # Inicializar vista
        self.login = Ventana_login()
        
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
        """Configura conexiones entre vista y controlador"""
        # Conectar botón de login
        if hasattr(self.login, 'boton_login'):
            try:
                self.login.boton_login.clicked.disconnect()
            except:
                pass
            self.login.boton_login.clicked.connect(self.verificar_login)
        
        # Conectar atajo de teclado (Enter)
        if hasattr(self.login, 'login_action'):
            try:
                self.login.login_action.triggered.disconnect()
            except:
                pass
            self.login.login_action.triggered.connect(self.verificar_login)
        
    
    def verificar_login(self):
        # --Método principal para la verificación del Logueo--
        
        # Obtener las credenciales previamente adquiridas de la vista
        username = self.login.input_usuario.text().strip()
        password = self.login.input_password.text().strip()
        
        # Validar campos no vacíos
        if not username:
            QMessageBox.warning(self.login, "Campo requerido", "Ingrese el nombre de usuario")
            self.login.input_usuario.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self.login, "Campo requerido", "Ingrese la contraseña")
            self.login.input_password.setFocus()
            return
        
        # Enviar al modelo para autenticación
        resultado, mensaje, datos_usuario = self.modelo.autenticar_usuario(username, password)
        
        if resultado:
            # Login exitoso
            self.usuario_actual = datos_usuario
            
            # Mostrar mensaje y emitir señal
            QMessageBox.information(self.login, "Éxito", mensaje)
            self.login.login_exitoso.emit()
        else:
            # Login fallido
            print(f"❌ {mensaje}")
            QMessageBox.critical(self.login, "Error", mensaje)
            self.login.input_password.clear()
            self.login.input_password.setFocus()
    
    
    def get_widget(self):
        # Retorna el widget de login
        return self.login
    
    def get_usuario_actual(self):
        # Obtiene usuario autenticado
        return self.usuario_actual
    
    def get_modelo(self):
        # Obtiene el modelo
        return self.modelo