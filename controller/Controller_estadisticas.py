# controlador_estadistica.py
from models.Modelo_estadistica import Modelo_estadistica
from view.vista_estadistica import Ventana_principal
from typing import Dict, List, Any


class ControladorEstadistica:
    def __init__(self):
        self.modelo = Modelo_estadistica()

    def get_widget(self):
        self.estadistica = Ventana_principal()
        return self.estadistica