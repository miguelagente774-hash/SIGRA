# controlador_estadistica.py
from models.Modelo_estadistica import ModeloEstadistica 
from view.vista_estadistica import Ventana_principal
from typing import Dict, List, Any


class ControladorEstadistica:
    def __init__(self, db_path="database/SIGRAG.db"):
        self.modelo = ModeloEstadistica(db_path)

    def get_widget(self):
        self.consulta = Ventana_principal(self)
        return self.consulta