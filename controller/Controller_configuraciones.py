from view.vista_configuracion import Ventana_configuracion

class controlador_configuraciones():
    def __init__(self):
        self.configuraciones = Ventana_configuracion()

    def get_widget(self):
        return self.configuraciones