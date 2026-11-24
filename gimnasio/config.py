"""
config.py
Valores de configuración del sistema. Si se quiere cambiar algo general
(nombre del gimnasio, carpeta de datos, tamaño de la ventana...) se cambia aquí
y no hay que tocar el resto del código.
"""

import os

# Datos generales del gimnasio
NOMBRE_GIMNASIO = "Gimnasio Udenar"

# Carpeta donde se guardan los archivos CSV (base de datos)
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")

# Ventana
TITULO_VENTANA = "Sistema de Gestión de Gimnasio"
TAMANO_VENTANA = "1000x700"
