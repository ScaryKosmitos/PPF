"""
main.py
Punto de entrada del Sistema de Gestión de Gimnasio.

Ejecutar desde esta carpeta con:
    python main.py
"""

import tkinter as tk

from config import CARPETA_DATOS, NOMBRE_GIMNASIO
from basedatos.repositorio_csv import RepositorioCSV
from interfaz.ventana_principal import VentanaPrincipal


def main():
    # 1. Base de datos: cargar los CSV y reconstruir los objetos
    repositorio = RepositorioCSV(CARPETA_DATOS)
    gimnasio = repositorio.cargar(NOMBRE_GIMNASIO)

    # 2. Interfaz: abrir la ventana con el gimnasio cargado
    root = tk.Tk()
    VentanaPrincipal(root, gimnasio, repositorio)
    root.mainloop()


if __name__ == "__main__":
    main()
