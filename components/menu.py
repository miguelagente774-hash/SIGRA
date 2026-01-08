from PyQt5.QtWidgets import (QFrame, QPushButton, QLabel,
                             QVBoxLayout, QSizePolicy, QSpacerItem,
                             QGraphicsDropShadowEffect, QWidget)
from PyQt5.QtGui import (QPixmap, QFont)
from PyQt5.QtCore import Qt

# Estilos mejorados pero más sencillos
botones_estilos = """
        QPushButton{
        background: #005a6e;
        color: White;
        font-weight: bold;
        font-size: 13px;
        padding: 10px 20px;
        margin: 6px 15px;
        border-radius: 8px;
        text-align: left;
        border: none;
        }  
        QPushButton:hover{
        background: #007a94;
        
        }    
        QPushButton:pressed{
        background: #00485a;
        }"""

botones_estilos_submenu = """
        QPushButton{
        background: rgba(0, 90, 110, 0.8);
        color: White;
        font-size: 12px;
        padding: 5px 25px;
        margin: 3px 10px;
        border-radius: 6px;
        text-align: left;
        border-left: 3px solid transparent;
        }  
        QPushButton:hover{
        background: rgba(0, 122, 148, 0.9);
        border-left: 3px solid #00bcd4;
        }    
        QPushButton:pressed{
        background: rgba(0, 72, 90, 0.9);
        }"""

botones_estilos_submenu_activo = """
        QPushButton{
        background: #0086a3;
        color: White;
        font-size: 12px;
        font-weight: bold;
        padding: 5px 25px;
        margin: 3px 10px;
        border-radius: 6px;
        border-left: 3px solid #00e5ff;
        }  
        QPushButton:hover{
        background: #0099b8;
        }    
        QPushButton:pressed{
        background: #00738a;
        }"""

botones_estilos_activo = """
        QPushButton{
        background: #0086a3;
        color: White;
        font-weight: bold;
        font-size: 13px;
        padding: 10px 20px;
        margin: 6px 15px;
        border-radius: 8px;
        border: none;
        }  
        QPushButton:hover{
        background: #0099b8;
        }    
        QPushButton:pressed{
        background: #00738a;
        }"""

class Menu(QFrame):
    def __init__(self, ventana):
        super().__init__()
        self.ventana = ventana
        # Layout del frame
        self.layout_main = QVBoxLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        # Configurando menu 
        self.setMinimumWidth(220)
        self.setMaximumWidth(290)
        self.setStyleSheet("""
            QFrame {
                background: #003642;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }
        """)
        self.setLayout(self.layout_main)
        
        # Sombra suave
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(20)
        sombra.setColor(Qt.darkGray)
        sombra.setOffset(5, 2)
        self.setGraphicsEffect(sombra)

        self.imagen()
        self.Botones_menu()

    def imagen(self):
        # Logo de la App
        mover_arriba = QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout_main.addItem(mover_arriba)

        logo_container = QWidget()
        logo_container.setFixedSize(180, 180)
        logo_container.setStyleSheet("""
            QWidget {
                background: #005a6e;
                border-radius: 60px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(2, 2, 2, 2)
        
        logo = QLabel()
        ruta_imagen = QPixmap("img/logo.jpg")
        if not ruta_imagen.isNull():
            imagen_redimensionada = ruta_imagen.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(imagen_redimensionada)
        else:
            logo.setText("LOGO")
            logo.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("background: transparent; border-radius: 50%;")
        logo_layout.addWidget(logo)
        
        self.layout_main.addWidget(logo_container, 0, alignment=Qt.AlignCenter)
        
        # Título de la aplicación
        titulo = QLabel("Sistema Reportes")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 16px;
                font-family: Arial;
                margin: 12px 0px;
                background: transparent;
            }
        """)
        self.layout_main.addWidget(titulo)

    def Botones_menu(self):
        # Espacio entre la imagen y los botones
        margen_imagen_botones = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout_main.addItem(margen_imagen_botones)

        layout_botones = QVBoxLayout()
        layout_botones.setSpacing(4)
        layout_botones.setContentsMargins(8, 0, 8, 0)
        self.layout_main.addLayout(layout_botones)

        # Botones principales con íconos simples
        self.boton_v_Principal = QPushButton("📊 Estadísticas")
        self.boton_v_Principal.setStyleSheet(botones_estilos)
        self.boton_v_Principal.clicked.connect(lambda: self.Cambiar_ventana(0))
        layout_botones.addWidget(self.boton_v_Principal)

        # ------------------------- submenu --------------------------
        self.boton_reporte = QPushButton("📊 Actividades")
        self.boton_reporte.setCheckable(True)
        self.boton_reporte.setStyleSheet(botones_estilos)
        self.boton_reporte.clicked.connect(self.funcion_mostrar_submenu)
        layout_botones.addWidget(self.boton_reporte)

        # Contenedor del submenu
        layout_submenu_botones = QVBoxLayout()
        layout_submenu_botones.setContentsMargins(20, 8, 5, 8)
        layout_submenu_botones.setSpacing(2)
        
        self.contenedor_submenu = QWidget()
        self.contenedor_submenu.setVisible(False)
        self.contenedor_submenu.setStyleSheet("""
            QWidget {
                background: rgba(0, 40, 50, 0.7);
                border-radius: 6px;
                margin: 0px 12px 5px 12px;
            }
        """)
        self.contenedor_submenu.setLayout(layout_submenu_botones)

        # Botones del submenu
        self.boton_reporte_crear = QPushButton("➕ Crear Actividad")
        self.boton_reporte_crear.setStyleSheet(botones_estilos_submenu)
        self.boton_reporte_crear.clicked.connect(lambda: self.Cambiar_ventana(1))
        layout_submenu_botones.addWidget(self.boton_reporte_crear)

        self.boton_reporte_finalizado = QPushButton("✅ Activiades Finalizadas")
        self.boton_reporte_finalizado.setStyleSheet(botones_estilos_submenu)
        self.boton_reporte_finalizado.clicked.connect(lambda: self.Cambiar_ventana(2))
        layout_submenu_botones.addWidget(self.boton_reporte_finalizado)

        self.boton_reporte_eliminar = QPushButton("📋 convertir reporte")
        self.boton_reporte_eliminar.setStyleSheet(botones_estilos_submenu)
        self.boton_reporte_eliminar.clicked.connect(lambda: self.Cambiar_ventana(3))
        layout_submenu_botones.addWidget(self.boton_reporte_eliminar)


        
        layout_botones.addWidget(self.contenedor_submenu)

        # ----------------------------------------------------------------------
        self.boton_consulta = QPushButton("🔍 Consulta")
        self.boton_consulta.setStyleSheet(botones_estilos)
        self.boton_consulta.clicked.connect(lambda: self.Cambiar_ventana(4))
        layout_botones.addWidget(self.boton_consulta)

        self.boton_configuracion = QPushButton("⚙️ Configuración")
        self.boton_configuracion.setStyleSheet(botones_estilos)
        self.boton_configuracion.clicked.connect(lambda: self.Cambiar_ventana(5))
        layout_botones.addWidget(self.boton_configuracion)

        # Espacio antes del botón salir
        espacio_salir = QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout_botones.addItem(espacio_salir)

        boton_salir = QPushButton("🚪 Salir")
        boton_salir.setStyleSheet("""
        QPushButton{
        background: #8B0000;
        color: White;
        font-weight: bold;
        font-size: 13px;
        padding: 10px 20px;
        margin: 3px 15px;
        border-radius: 8px;
        text-align: left;
        border: none;
        }  
        QPushButton:hover{
        background: #A00000;
        }    
        QPushButton:pressed{
        background: #600000;
        }""")
        boton_salir.clicked.connect(self.ventana.close)
        layout_botones.addWidget(boton_salir)
  
        # Espacio para empujar los botones hacia arriba
        mover_arriba = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_botones.addItem(mover_arriba)

        # Label de versión
        version = QLabel("Versión 1.0")
        version.setStyleSheet("""
            QLabel{
                background: #005a6e;
                padding: 10px 15px;
                border-radius: 12px;
                margin: 5px 20px 15px -20px;
                color: White;
                font-weight: bold;
                font-size: 12px;
                font-family: Arial;
            }
        """)
        version.setAlignment(Qt.AlignCenter)
        #version.setFixedHeight(35)
        self.layout_main.addWidget(version)

    def funcion_mostrar_submenu(self, e):
        estado_visibilidad = self.contenedor_submenu.isVisible()
        self.contenedor_submenu.setVisible(not estado_visibilidad)
        
        if e:
            self.boton_reporte.setStyleSheet(botones_estilos_activo)
        else:
            self.boton_reporte.setStyleSheet(botones_estilos)

    # Función que integra al layout del main container las distintas ventanas
    def funcion_ventanas(self, layout_stacked, v0, v1, v2, v3, v4, v5):
       self.layout_v = layout_stacked
       self.layout_v.addWidget(v0)
       self.layout_v.addWidget(v1)
       self.layout_v.addWidget(v2)
       self.layout_v.addWidget(v3)
       self.layout_v.addWidget(v4)
       self.layout_v.addWidget(v5)
       self.Cambiar_ventana(0)
       
    def Cambiar_ventana(self, indice):
       self.layout_v.setCurrentIndex(indice)
          
       # Algoritmo para activar background en los botones del menu cuando es seleccionado
       if indice == 0:
             self.boton_v_Principal.setStyleSheet(botones_estilos_activo)
       else:
              self.boton_v_Principal.setStyleSheet(botones_estilos)

       # Submenu
       if indice == 1:
              self.boton_reporte_crear.setStyleSheet(botones_estilos_submenu_activo)
       else:
                 self.boton_reporte_crear.setStyleSheet(botones_estilos_submenu)

       if indice == 2:
              self.boton_reporte_finalizado.setStyleSheet(botones_estilos_submenu_activo)
              
       else:
              self.boton_reporte_finalizado.setStyleSheet(botones_estilos_submenu)

       if indice == 3:
              self.boton_reporte_eliminar.setStyleSheet(botones_estilos_submenu_activo)
       else:
              self.boton_reporte_eliminar.setStyleSheet(botones_estilos_submenu)

       if indice == 4:
              self.boton_consulta.setStyleSheet(botones_estilos_activo)
       else:
              self.boton_consulta.setStyleSheet(botones_estilos)

       if indice == 5:
              self.boton_configuracion.setStyleSheet(botones_estilos_activo)
       else:
              self.boton_configuracion.setStyleSheet(botones_estilos)

       if indice == 1 or indice == 2 or indice == 3:
             self.boton_reporte.setStyleSheet(botones_estilos_activo)
       else:
             self.boton_reporte.setStyleSheet(botones_estilos)
             self.contenedor_submenu.setVisible(False)
