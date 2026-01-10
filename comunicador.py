from PySignal import Signal

class Comunicar():
    def __init__(self):
        self.actividad_agregada = Signal()
        self.Reporte_agregado = Signal()

Comunicador_global = Comunicar()