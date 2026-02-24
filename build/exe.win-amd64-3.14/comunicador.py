from PyQt5.QtCore import QObject, pyqtSignal

class ComunicadorGlobal(QObject):
    actividad_agregada = pyqtSignal()
    Reporte_agregado = pyqtSignal()
    
    def __init__(self):
        super().__init__()

Comunicador_global = ComunicadorGlobal()