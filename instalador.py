"""
setup.py - CONFIGURACIÓN BÁSICA UNIVERSAL
Funciona para cualquier tipo de programa
"""

from cx_Freeze import setup, Executable
import sys
import os

# ============================================
# 1. DETECCIÓN AUTOMÁTICA DEL SISTEMA
# ============================================
def detectar_configuracion():
    """Detecta automáticamente el sistema y tipo de app"""
    
    # Detectar si es aplicación GUI (sin consola)
    es_gui = False
    try:
        # Comprobar si importa módulos GUI comunes
        import PyQt5
        es_gui = True
    except:
        import PyQt5.QtWidgets
        es_gui = True

    
    # Configurar base según sistema y tipo
    if sys.platform == "win32":
        base = "gui" if es_gui else None
    else:
        base = None
    
    return base, es_gui

# ============================================
# 2. CONFIGURACIÓN PRINCIPAL
# ============================================
# Nombre de tu aplicación (CAMBIAR ESTO)
NOMBRE_APP = "SIGRA"
SCRIPT_PRINCIPAL = "main.py"  # Cambia esto por tu script principal
VERSION = "1.0.0"

# Obtener configuración automática
base, es_gui = detectar_configuracion()

# Opciones de construcción básicas
opciones_build = {
    # Paquetes que casi siempre se necesitan
    "packages": ["os", "sys"],
    
    # Archivos adicionales (cambiar según necesidad)
    "include_files": ["view/", "services/", "models/", "img/", "database/", "controller/", "components/", "comunicador.py"],
    
    # Excluir paquetes pesados innecesarios
    "excludes": ["tkinter", "unittest", "email", "http", "xml"] if not es_gui else [],
    
    # Optimizar tamaño
    "optimize": 2,
}

# Si detectamos GUI, agregamos paquetes comunes
if es_gui:
    try:
        import tkinter
        opciones_build["packages"].append("tkinter")
    except:
        pass

# ============================================
# 3. CONFIGURAR EJECUTABLE
# ============================================
# Buscar icono automáticamente
icono = None
iconos_posibles = ["img/icono.ico", "icon.png", "app.ico", "logo.ico"]
for icon in iconos_posibles:
    if os.path.exists(icon):
        icono = icon
        break

# Crear ejecutable
ejecutable = Executable(
    script=SCRIPT_PRINCIPAL,
    base=base,
    target_name=f"{NOMBRE_APP}.exe" if sys.platform == "win32" else NOMBRE_APP,
    icon=icono,
    shortcut_dir="DesktopFolder",
)

#acceso directo
options_acceso = {
        'data': {
            'Shortcut': [
                ("DesktopShortcut",        # Key
                 "DesktopFolder",          # Folder
                 "SIGRA",                  # Shortcut Name
                 "TARGETDIR",              # Component
                 "[TARGETDIR]SIGRA.exe", # Target
                 None,                     # Arguments
                 None,                     # Description
                 None,                     # Hotkey
                 None,   # Icon
                 None,                     # IconIndex
                 None,                     # ShowCmd
                 'TARGETDIR'               # WkDir
                )
            ],
        },
        "install_icon": "img/icono.ico"
    }



# ============================================
# 4. SETUP FINAL
# ============================================
setup(
    name=NOMBRE_APP,
    version=VERSION,
    description=f"Aplicación {NOMBRE_APP}",
    options={"build_exe": opciones_build,'bdist_msi': options_acceso},
    executables=[ejecutable]
)