from view.vista_estadistica import Ventana_principal

class controlador_estadistica():
    def __init__(self):
        self.vista = Ventana_principal()

    def get_widget(self):
        return self.vista